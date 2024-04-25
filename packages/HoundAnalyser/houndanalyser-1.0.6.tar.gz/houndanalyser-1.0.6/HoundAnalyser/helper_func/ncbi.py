import os, csv
from Bio import SeqIO, Seq
from .sundry import _find_tool, _cleanup_path


# Define constants
SEQS_FNAME = '/genes_found.fa'
SEQS_DN_FNAME = '/genes_found_denovo_assembly.fa'


def convert_to_db(assembly: str, N_THREADS: int,
                  MERGED_CONTIGS: bool = False) -> str:
    """
        Converts assembly into BLAST database locally to accelerate
        finding genes of interest inside the assembly. Creating this
        with the list of genes makes the process substantially inefficient.
    """
    # Convert assembly from BAM to FASTA. *NOTE* It must be a consensus
    # sequence! Otherwise there will be multiple identical seq_ids
    # and confuse BLAST
    if assembly.find('.bam') > -1 and assembly.find('.fa') == -1:
        db_path = assembly.replace('.bam', '.fa')
        samtools = _find_tool('samtools')
        convert_args = list(['consensus', '--verbosity 0',
                             '--threads ' + str(N_THREADS)])
        convert_args.extend([assembly, '-o ' + db_path])
        os.system(samtools + str(' ').join(convert_args))
    elif assembly.find('.fa') > -1:
        db_path = assembly  # De novo assembly is already in FASTA

    # Create BLAST (generate once to save time in multiple searches)
    if db_path.find('.fasta') > -1:
        assembly_idx = db_path.replace('.fasta', '.fasta.ndb')
    else:
        assembly_idx = db_path.replace('.fa', '.fa.ndb')

    if os.path.exists(assembly_idx) is False or MERGED_CONTIGS is True:
        makedb = _find_tool('makeblastdb')
        makedb_args = tuple(['-in ' + db_path, '-parse_seqids',
                            '-blastdb_version 5', '-dbtype nucl'])
        os.system(makedb + str(' ').join(makedb_args))


def _return_init_locus(loci_hit: list) -> int:
    """
        Given multiple hits for the same gene in the same contig, return
        the coordinates for that covering the START codon
    """
    init_locus = [hit for hit in loci_hit if int(hit[2]) == 1]
    if len(init_locus) == 0:
        # If no contig includes the START codon, return the longest
        init_locus = list([loci_hit[0]])
    elif len(init_locus) > 1:
        # If multiple hits cover the START codon and have same identity,
        # return the one with the highest score
        init_locus = list([loci_hit[0]])
    assert len(init_locus) == 1
    return int(init_locus[0][3]), int(init_locus[0][4])


def _structur_variations(HIT_GENE: str, HIT_CONTIG: str, MIN_THRS: float,
                         MAX_THRS: float, target_genes: str,
                         match_list: str) -> list:
    """
        Find if multiple hits belong to the same gene in the same contig,
        and adjust start/end coordinates accordingly.
    """
    blast_output = csv.reader(open(match_list, 'r'), delimiter='\t')
    QUERY = [q for q in SeqIO.parse(target_genes, 'fasta') if q.id == HIT_GENE]
    # Metadata already arranged by size (1st entry == longest hit) by (t)blastn
    # Isolate sequence metadata
    loci_hits = list()
    if len(QUERY) == 1:
        for entry in blast_output:
            hit_seqid = entry[0]
            query_seqid = entry[1]
            hit_identity = float(entry[2])
            if hit_seqid == HIT_GENE and query_seqid == HIT_CONTIG:  # Same gene & contig
                if MAX_THRS * 100 >= hit_identity >= MIN_THRS * 100:
                    hit_length = int(entry[3])
                    hit_querystart = int(entry[6])
                    hit_seqstart = int(entry[8])
                    hit_seqend = int(entry[9])
                    hit_score = float(entry[11])
                    # Is it a different loci or a genuine structural variation?
                    if hit_length >= len(QUERY[0].seq):  # QUERY covered by first hit
                        return False, None, None      # so this is a different locus
                    else:
                        # Store
                        loci_hits.append([hit_identity, hit_length,
                                          hit_querystart, hit_seqstart,
                                          hit_seqend, hit_score, query_seqid])

        # Check if 'loci_hits' cover all query and do not overlap.
        for lociN in range(0, len(loci_hits)):
            if loci_hits[lociN][1] < len(QUERY[0].seq) and lociN == 0:
                reference_hit = loci_hits[lociN]
            else:
                if reference_hit[3] > reference_hit[4]:
                    reference_start = reference_hit[4]
                    reference_end = reference_hit[3]
                else:
                    reference_start = reference_hit[3]
                    reference_end = reference_hit[4]

                if loci_hits[lociN][3] > loci_hits[lociN][4]:
                    hit_start = loci_hits[lociN][4]
                    hit_end = loci_hits[lociN][3]
                else:
                    hit_start = loci_hits[lociN][3]
                    hit_end = loci_hits[lociN][4]

                # Check overlap. If there is, it means likely truncated ORF
                # Return the hit covering the beginning of QUERY
                if hit_start <= reference_end or hit_end >= reference_start:
                    new_seqstart, new_seqend = _return_init_locus(loci_hits)
                    return True, new_seqstart, new_seqend
                else:  # No overlap, likely insertion that maintains ORF...?
                    print("(Hound **BARKED**) THERE IS **NO** OVERLAP!")
                    new_seqstart = min(reference_hit[2], loci_hits[lociN][2])
                    new_seqend = max(reference_hit[3], loci_hits[lociN][3])
                    return True, new_seqstart, new_seqend
    return False, None, None


def _parse_blast_output(SEQ_ID: str, target_genes: str, match_list: str,
                        THRESHOLD_RANGE: tuple) -> str:
    """
        Retrieves a tab-separated match list from BLAST, and process
        it to make it human-friendly. Fields:

        0: query acc.ver, 1: subject acc.ver, 2: % identity, 3: alignment length,
        4: mismatches, 5: gap opens, 6: q. start, 7: q. end, 8: s. start,
        9: s. end, 10: evalue, 11: bit score.
    """
    file_stats = os.lstat(match_list)
    min_threshold, max_threshold = THRESHOLD_RANGE
    if file_stats.st_size == 0:
        if str('mlst') in match_list.lower():
            msg = str("(MLST) No matches found in assembly ") + SEQ_ID + str(".")
        else:
            msg = str("No matches found in assembly ") + SEQ_ID + str(".")
        print(msg)
        return None
    else:
        initial_list = csv.reader(open(match_list, 'r'), delimiter='\t')
        hits_dict = dict()
        entry_seen = set()
        n_copies = dict()
        entries_skipped = None
        for entry in initial_list:
            # Retrieve fields of interest
            hit_seqid = entry[0]
            query_seqid = entry[1]
            hit_identity = float(entry[2])
            hit_length = int(entry[3])
            hit_seqstart = int(entry[8])
            hit_seqend = int(entry[9])
            hit_score = float(entry[11])
            # Store information in dictionary
            if max_threshold * 100 >= hit_identity >= min_threshold * 100:
                # Entries with multiple copies are not exported properly.
                # Adding number of copies to the name helps.
                if hit_seqid in entry_seen:
                    STRUCT_VAR, \
                        new_seqstart, \
                            new_seqend = _structur_variations(hit_seqid,
                                                              query_seqid,
                                                              min_threshold,
                                                              max_threshold,
                                                              target_genes,
                                                              match_list)
                    if STRUCT_VAR is False:
                        if hit_seqid in n_copies.keys():
                            n_copies[hit_seqid] += 1
                        else:
                            n_copies[hit_seqid] = 2
                        hit_seqid = hit_seqid + str('_L') + str(n_copies[hit_seqid])
                    else:
                        hit_seqstart = new_seqstart
                        hit_seqend = new_seqend
                hits_dict[hit_seqid] = [hit_identity, hit_length, hit_seqstart,
                                        hit_seqend, hit_score, query_seqid]
                # Update duplicated_entries to keep track of entries with
                # identical SeqID (...bypassing how BLAST outputs stuff...)
                entry_seen.add(hit_seqid)
            elif hit_identity < min_threshold * 100:
                # Warn about other genes below detection threshold.
                # It is a given that more genes exist above the max_threshold.
                entries_skipped = True
        if len(hits_dict) == 0:
            if str('mlst') in match_list.lower():
                msg = str("(MLST) ***WARNING*** Detection window is too " \
                          "restrictive: Hits found in ") + SEQ_ID + \
                          str(" but NONE added.")
            else:
                msg = str("***WARNING*** Detection window is too " \
                          "restrictive: Hits found in ") + SEQ_ID + \
                          str(" but NONE added.")
            print(msg)
            return None
        elif entries_skipped is True:
            if str('mlst') in match_list.lower():
                msg = str("(MLST) ID_THRESHOLD: Hits added from ") + SEQ_ID + \
                      str(", some were left behind with low identity.")
            else:
                msg = str("ID_THRESHOLD: Hits added from ") + SEQ_ID + \
                      str(", some were left behind with low identity.")
            print(msg)
            return hits_dict
        else:
            return hits_dict


def _sanitise_gene_metadata(gene_metadata: dict, hk_genes: bool = False) -> dict:
    """
        Remove from the metadata dictionary blast hits that have a
        low score and short length caused by partial homologies. Note
        this method is independent of % of identity with query sequence,
        so it can still be used to fish for new genes.
    """
    LENGTH_ID = 1
    SCORE_ID = 4

    # Note BLAST annotates first the hit with highest homology to query
    # sequence. Then the second hit with highest score, and so on.
    if gene_metadata is None or gene_metadata is False:
        return None
    else:
        REF_MATCH = tuple(gene_metadata.keys())[0]
        REF_SCORE = float(gene_metadata[REF_MATCH][SCORE_ID])

        sanitised_metadata = dict()
        for locus in gene_metadata:
            if gene_metadata[locus][SCORE_ID] >= REF_SCORE / 4:
                sanitised_metadata[locus] = gene_metadata[locus]
                # Leave one instance per hk_gene
                if hk_genes is True and str('_L') in locus:
                    sanitised_metadata.pop(locus)
                # Update references, so new locus is compared to previous locus
                REF_SCORE = float(gene_metadata[locus][SCORE_ID])
        return sanitised_metadata


def _extract_assembly_ID(assembly: str, dir_depth: int, de_novo: bool) -> str:
    """
        Extract assembly ID from absolute assembly path.
    """
    fName = assembly.split('/')[-1]
    prj_path = assembly.split('/')[:-2]
    # Correct path in case of denovo alignment of unmapped reads
    if prj_path[-1] == 'assemblies':
        prj_path = prj_path[:-dir_depth]

    if de_novo is False:
        return fName.removesuffix('_Assembly.bam').removesuffix('_'), \
               str('/').join(prj_path)
    else:
        return fName.removesuffix('_assembly.fa').removesuffix('_'), \
               str('/').join(prj_path)


def _process_handle(ncbi_code: str) -> str:
    """
        Replace NCBI alphanumeric codes by the human-readable gene/protein
        name provided by the correspondings fasta files.
    """
    return ncbi_code.split(' [')[0].split(' (')[0].split(' ')[-1]


def _extract_gene_data(db_seq: SeqIO, PREFIX: str, TARGET_GENES: str,
                       gene_metadata: dict, SEQ_ID: str, SEQ_CUTOFF: int,
                       PRJ_PATH: str) -> str:
    """
        Extract gene-related data from de novo assembly using BLAST output as
        a guide, and write it to file defined by SEQS_DN_FNAME.
    """
    global SEQS_DN_FNAME  # FIX: Assumes is always de novo. Use 'assembly' to find whether de novo or not.

    # Insert FASTA file used in filename
    QUERY_NAME = TARGET_GENES.split('/')[-1].split('.')[0]
    if QUERY_NAME not in SEQS_DN_FNAME:
        SEQS_DN_FNAME = SEQS_DN_FNAME.split('.')[0] + str('_') + QUERY_NAME + \
                        str('.') + SEQS_DN_FNAME.split('.')[1]

    # Include PREFIX in output files
    if PREFIX is not None:
        if PREFIX not in SEQS_DN_FNAME:  # ERRs if NoneType, hence two ifs.
            SEQS_DN_FNAME = SEQS_DN_FNAME.split('.')[0] + str('_') + PREFIX  + \
                            str('.') + SEQS_DN_FNAME.split('.')[1]

    END_POS_ID = 3
    START_POS_ID = 2
    ID_POS_ID = 0
    TARGET_SEQID = 5

    if gene_metadata is None:
        # Write in FASTA format assembly that was screened but no hit
        with open(PRJ_PATH + SEQS_DN_FNAME, 'a') as fOut:
            fOut.write('>' + SEQ_ID.split('_assembly.fa')[0] +
                       str('__[NO HITS OR BELOW ID THRESHOLD]\n'))
    else:
        for handle in db_seq:
            for gene in gene_metadata:
                handle_id = gene_metadata[gene][TARGET_SEQID]
                START_POS = gene_metadata[gene][START_POS_ID]
                END_POS = gene_metadata[gene][END_POS_ID]
                ID = gene_metadata[gene][ID_POS_ID]
                if handle.id == handle_id:  # TODO: Simplify detection of handle.id
                    MAX_LENGTH = len(handle.seq)
                    gene_readable = _process_handle(gene)
                    if START_POS < END_POS:  # gene is in forward strand
                        LOW_BOUNDARY = max([0, START_POS-SEQ_CUTOFF-1])
                        UP_BOUNDARY = min([END_POS+3, MAX_LENGTH])
                        Extd_ORF = handle.seq[LOW_BOUNDARY:UP_BOUNDARY]
                        if Extd_ORF[-3:] != 'TAA':  # If STOP not next codon, find it
                            NEW_END_POS = handle.seq.rfind('TAA', start=END_POS)
                            if NEW_END_POS != -1:
                                # Re-define gene boundaries and sequence
                                gene_metadata[gene][END_POS_ID] = NEW_END_POS
                                LOW_BOUNDARY = max([0, START_POS-SEQ_CUTOFF-1])
                            UP_BOUNDARY = min([END_POS+3, MAX_LENGTH])
                            Extd_ORF = handle.seq[LOW_BOUNDARY:UP_BOUNDARY]
                    elif START_POS > END_POS:  # gene is in reverse strand
                        LOW_BOUNDARY = max([0, END_POS-4])
                        UP_BOUNDARY = min([START_POS+SEQ_CUTOFF, MAX_LENGTH])
                        Extd_ORF = handle.seq.complement()[LOW_BOUNDARY:UP_BOUNDARY]
                        # Flip ORF so I can friggin understand things
                        Extd_ORF = Extd_ORF[::-1]
                        if Extd_ORF[-3:] != 'TAA':  # If STOP not next codon, find it
                            NEW_END_POS = handle.seq.rfind('AAT', end=END_POS)
                            if NEW_END_POS != -1:
                                # Re-define gene boundaries and sequence
                                gene_metadata[gene][START_POS_ID] = NEW_END_POS
                                LOW_BOUNDARY = max([0, END_POS-4])
                                UP_BOUNDARY = min([START_POS+SEQ_CUTOFF, MAX_LENGTH])
                                Extd_ORF = handle.seq.complement()[LOW_BOUNDARY:UP_BOUNDARY]
                                # Flip ORF so I can friggin understand things
                                Extd_ORF = Extd_ORF[::-1]
                    # Now write in FASTA format
                    with open(PRJ_PATH + SEQS_DN_FNAME, 'a') as fOut:
                        fOut.write('>' + SEQ_ID.split('_assembly.fa')[0] +
                                   str('__[') + handle_id.split('_cov_')[0] +
                                   str(']') + str(' ') + gene_readable +
                                   str(' ID') + str(round(ID)) + str('\n'))
                        fOut.write(str(Extd_ORF) + str('\n'))
    return


def compile_genes_detected(assembly: str, blast_output: str, TARGET_GENES: str,
                           PREFIX: str, DIR_DEPTH: int, CALC_COVERAGE: bool,
                           SEQ_CUTOFF: int, ID_THRESHOLD: tuple,
                           de_novo: bool = False) -> str:
    """
        Retrieve nucleotide sequence from `assembly' based on BLAST results.
    """
    SEQ_ID, PRJ_PATH = _extract_assembly_ID(assembly, DIR_DEPTH, de_novo)

    mlst_output = blast_output.replace('.blast', '_MLST.blast')

    # Filter BLAST output (enforce higher restrictions for housekeeping genes)
    gene_metadata = _parse_blast_output(SEQ_ID, TARGET_GENES, blast_output,
                                        THRESHOLD_RANGE=ID_THRESHOLD)
    if CALC_COVERAGE is True and gene_metadata is not None:
        mlst_metadata = _parse_blast_output(SEQ_ID, TARGET_GENES, mlst_output,
                                            THRESHOLD_RANGE=(0.95, 1.0))
    else:
        mlst_metadata = None

    # Parse gene metadata assembly
    db_seq = SeqIO.parse(assembly.replace('.bam', '.fa'), 'fasta')
    _extract_gene_data(db_seq, PREFIX, TARGET_GENES, gene_metadata, SEQ_ID,
                       SEQ_CUTOFF, PRJ_PATH)

    if gene_metadata is not None:
        return gene_metadata, mlst_metadata, SEQ_ID, PRJ_PATH, \
            PRJ_PATH + SEQS_DN_FNAME
    else:
        return None, None, SEQ_ID, PRJ_PATH, PRJ_PATH + SEQS_DN_FNAME


def find_amr_genes(assembly: str, GENES_FNAME: str, HKGENES_FNAME: str,
                   CALC_COVERAGE: bool, FIND_NT: bool = False,
                   N_THREADS: int = 1, MERGED_CONTIGS: bool = False) -> str:
    """
        Compares 'assembly' to genes located in bespoke, local BLAST database
        and returns hits found. The number of hits returned can be filtered
        based on the identity to the query assembly.

        NOTE: I could export GENES_FNAME to use later on. But this would make
        'compile_genes_detected' dependant of 'find_amr_genes', so I'm not
        going to export it.
    """
    if MERGED_CONTIGS is True:  # Re-generate BLAST+ database
        convert_to_db(assembly, N_THREADS, MERGED_CONTIGS)

    # Compare list of genes to assembly_db.
    # tblastn: Prot-query in nucl-db, blastx: Nucl-query in prot-db
    if FIND_NT is False:
        blast = _find_tool('tblastn')
    else:
        blast = _find_tool('blastn')

    # Default params
    EVAL = 0.05
    WORD_SIZE = 7 if blast.find('tblastn') > -1 else 12
    MATRIX = str('BLOSUM62')
    G_OPEN = 11 if blast.find('tblastn') > -1 else 2
    G_EXTENDED = 1
    O_FMT = 6  # 6 = CSV, 7 = CSV w/ headers

    # Chr
    if assembly.find('.bam') > -1 and assembly.find('.bai') == -1:
        matches_file = assembly.replace('.bam', '.blast')
    elif assembly.find('.fasta') > -1:  # For assemblies from MicrobesNG
        matches_file = assembly.replace('.fasta', '.blast')
    elif assembly.find('.fa') > -1:
        matches_file = assembly.replace('.fa', '.blast')

    if CALC_COVERAGE is True:
        # Housekeeping genes
        housekeeping_file = matches_file.replace('.blast', '_MLST.blast')

    # Find GENES_FNAME in assembly
    if FIND_NT is True:
        blast_args = tuple(['-num_threads ' + str(N_THREADS), '-evalue ' +
                           str(EVAL), '-word_size ' + str(WORD_SIZE),
                           '-gapopen ' + str(G_OPEN), '-gapextend ' +
                            str(G_EXTENDED), '-outfmt ' + str(O_FMT),
                            '-query ' + GENES_FNAME, '-db ' + assembly,
                            '-out ' + matches_file])
    else:  # AA search
        blast_args = tuple(['-num_threads ' + str(N_THREADS), '-evalue ' +
                           str(EVAL), '-word_size ' + str(WORD_SIZE),
                           '-matrix ' + MATRIX, '-gapopen ' + str(G_OPEN),
                            '-gapextend ' + str(G_EXTENDED), '-outfmt ' +
                            str(O_FMT), '-seg no', '-query ' + GENES_FNAME,
                            '-db ' + assembly, '-out ' + matches_file])
    os.system(blast + str(' ').join(blast_args))

    if CALC_COVERAGE is True and os.lstat(matches_file).st_size > 0:
        # Find MLST (housekeeping) genes in assembly for coverage basedline
        if FIND_NT is True:
            blast_args = tuple(['-num_threads ' + str(N_THREADS), '-evalue ' +
                               str(EVAL), '-word_size ' + str(WORD_SIZE),
                               '-gapopen ' + str(G_OPEN), '-gapextend ' +
                                str(G_EXTENDED), '-outfmt ' + str(O_FMT),
                                '-query ' + GENES_FNAME, '-db ' + assembly,
                                '-out ' + matches_file])
        else:
            blast_args = tuple(['-num_threads ' + str(N_THREADS), '-evalue ' +
                               str(EVAL), '-word_size ' + str(WORD_SIZE),
                               '-matrix ' + MATRIX, '-gapopen ' + str(G_OPEN),
                                '-gapextend ' + str(G_EXTENDED), '-outfmt ' +
                                str(O_FMT), '-seg no',
                                '-query ' + HKGENES_FNAME, '-db ' + assembly,
                                '-out ' + housekeeping_file])
        os.system(blast + str(' ').join(blast_args))
