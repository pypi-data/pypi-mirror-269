from Bio import SeqIO, Seq
from Bio.Align import PairwiseAligner
from .ncbi import _extract_assembly_ID
import csv, os, subprocess


# Define constants
START_POS_ID = 8
END_POS_ID = 9
ID_POS_ID = 1

QUERY_START_POS_ID = 6
QUERY_END_POS_ID = 7
LEN_POS_ID = 3


def _load_assembly(assembly: str) -> dict:
    """
        Load assembly sequence and coverage data, and arrange them as a
        dictionary.
    """
    # Load sequence data
    SEQ_RAW = [contig for contig in SeqIO.parse(assembly, 'fasta')]
    ASMBL_SEQ = dict()
    for contig in SEQ_RAW:
        ASMBL_SEQ[contig.name] = contig.seq
    return ASMBL_SEQ


def _align_seqs(SEQ_A, SEQ_B):
    """
        Basic pair-wise sequence alignment.
    """
    aligner = PairwiseAligner()
    aligner.mode = 'local'  # 'global' for gaps, 'local' for alignment window
    aligner.gap_score = -1950
    aligner.extend_gap_score = -1950
    return aligner.align(SEQ_A, SEQ_B)


def _reconstruct_sequence(SEQ_A, SEQ_B, REV_COMPLEMENT):
    """
        Align SEQ_A to SEQ_B, each in different contigs, to reconstruct
        the original QUERY_SEQ sequence.
    """
    aln = _align_seqs(SEQ_A, SEQ_B)
    coords = aln[0].coordinates[1]
    # Reconstitute QUERY_SEQ
    if aln[0].coordinates[1][0] < aln[0].coordinates[0][0]:  # 0=target seq, 1=query seq
        # SEQ_B aligns with the end part of SEQ_A
        RECONST_QUERY = SEQ_A + SEQ_B[coords[1]:]
        BEFORE_TARGET = False
    elif aln[0].coordinates[1][0] > aln[0].coordinates[0][0]:
        # SEQ_B aligns with the initial part of SEQ_A
        RECONST_QUERY = SEQ_B[:coords[0]] + SEQ_A  # -1 to remove '*'
        BEFORE_TARGET = True
    else:
        # SEQ_A and SEQ_B are IDENTICAL
        RECONST_QUERY = None
        BEFORE_TARGET = None
    return RECONST_QUERY, BEFORE_TARGET, aln


def _load_aa_seq(CONTIG, START_POS, END_POS):
    """
        Translate and determine strand.
    """
    if START_POS < END_POS:
        LOW_BOUNDARY = max([0, START_POS-1])
        UP_BOUNDARY = min([END_POS+3, len(CONTIG)])
        SEQ_AA = CONTIG[LOW_BOUNDARY:UP_BOUNDARY].translate()
        SEQ_NT = CONTIG[LOW_BOUNDARY:UP_BOUNDARY]
        REV_COMPLEMENT = False
    elif START_POS > END_POS:
        LOW_BOUNDARY = max([0, END_POS-4])
        UP_BOUNDARY = min([START_POS, len(CONTIG)])
        SEQ_AA = CONTIG[LOW_BOUNDARY:UP_BOUNDARY].reverse_complement().translate()
        SEQ_NT = CONTIG[LOW_BOUNDARY:UP_BOUNDARY].reverse_complement()
        REV_COMPLEMENT = True
    return SEQ_AA, SEQ_NT, REV_COMPLEMENT


def _contig_sorter(CONTIGS_W_QUERY: list, ASMBL_SEQ: dict) -> list:
    """
        Determine the order of the contigs containing QUERY_SEQ. Returns the
        contig order and reconstructed QUERY_SEQ as RECONST_QUERY.
    """
    CONTIGS_SORTED = list()
    for contig_num, contig in enumerate(CONTIGS_W_QUERY):
        C_ID = contig[ID_POS_ID]
        START_POS = int(contig[START_POS_ID])
        END_POS = int(contig[END_POS_ID])
        # Load longest hit (first in BLAST report)
        if contig[1] == CONTIGS_W_QUERY[0][1]:
            # CONTIGS_SORTED.append([C_ID, 0, None, None])
            SCAFFOLD_SEQ, _, SCAFFOLD_REV_COMPLEMENT = _load_aa_seq(ASMBL_SEQ[C_ID],
                                                                    START_POS,
                                                                    END_POS)
            CONTIGS_SORTED.append([C_ID, None, SCAFFOLD_REV_COMPLEMENT])
        else:
            EXT_SEQ, _, EXT_REV_COMPLEMENT = _load_aa_seq(ASMBL_SEQ[C_ID],
                                                          START_POS, END_POS)
            # Find common ORF between contigs
            RECONST_QUERY, SCAFFOLD_FIRST, _ = _reconstruct_sequence(SCAFFOLD_SEQ,
                                                                     EXT_SEQ,
                                                                     True)
            if RECONST_QUERY is not None:
                # Update SCAFFOLD_SEQ if sequences are not identical
                SCAFFOLD_SEQ = RECONST_QUERY

                # Update contig order
                CONTIGS_SORTED.append([C_ID, SCAFFOLD_FIRST,
                                       EXT_REV_COMPLEMENT])
    return CONTIGS_SORTED


def _check_query_in_contig(QUERY_NAME: str, QUERY_SEQ: Seq, BLAST_output: list,
                           ID_THRESHOLD: float) -> list:
    """
        Checks if QUERY_SEQ is in one or multiple contigs.
    """
    # CHECK THIS, NOT SURE PICKS UP DIFFERENT QUERIES
    CONTIGS_W_QUERY = list()
    QUERY_LEN = len(QUERY_SEQ) if QUERY_SEQ[-1] == '*' else len(QUERY_SEQ) + 1  # +1 accounts for termination codon '*'R
    BLAST_output = [e for e in BLAST_output if float(e[2]) >= ID_THRESHOLD and
                    QUERY_NAME == e[0]]
    for entry in BLAST_output:
        # Already arrange by size: longest hits come first.
        if entry[1] == BLAST_output[0][1]:
            CONTIGS_W_QUERY.append(entry)
            HIT_START = int(entry[QUERY_START_POS_ID])
            HIT_END = int(entry[QUERY_END_POS_ID])
            HIT_LEN = int(entry[LEN_POS_ID])
            if QUERY_LEN == HIT_LEN:
                break  # QUERY_SEQ inside a single entry
        else:
            # If any of these is TRUE, 'entry' does not overlap with first entry
            if int(entry[QUERY_START_POS_ID]) < HIT_START or int(entry[QUERY_END_POS_ID]) > HIT_END:
                CONTIGS_W_QUERY.append(entry)
                HIT_LEN = HIT_LEN + int(entry[LEN_POS_ID])
                HIT_START = min(HIT_START, int(entry[QUERY_START_POS_ID]))
                HIT_END = max(HIT_END, int(entry[QUERY_END_POS_ID]))

    # Check all contigs are unique, if not, remove duplicates---caused
    # by genes split within the same contig due to structural variations
    contig_list = [c[1] for c in CONTIGS_W_QUERY]
    for entry in CONTIGS_W_QUERY:
        if contig_list.count(entry[1]) > 1:
            CONTIGS_W_QUERY.remove(entry)
    return CONTIGS_W_QUERY


def _coverage_processor(COVERAGE_DATA: list) -> dict():
    """
        Transform COVERAGE_DATA into two dictionaries that look like ASMBL_SEQ.
        This is to facilitate re-arranging coverage data following the method
        in _contig_writer().
    """
    # Sanitise
    if COVERAGE_DATA[-1] == str(''):
        COVERAGE_DATA = COVERAGE_DATA[:-1]

    COV_DEPTH = dict()
    COV_POSITION = dict()
    for entry in COVERAGE_DATA:
        C_ID, LOC, DEPTH = entry.split('\t')
        if C_ID not in COV_DEPTH.keys():
            COV_DEPTH[C_ID] = list([int(DEPTH)])
            COV_POSITION[C_ID] = list([int(LOC)])
        else:
            COV_DEPTH[C_ID].append(int(DEPTH))
            COV_POSITION[C_ID].append(int(LOC))
    return COV_DEPTH, COV_POSITION


def _sort_coverage(assembly: str, CONTIGS_SORTED: list) -> list:
    """
        Reorganise file with coverage data to match the new order given by
        CONTIGS_SORTED
    """
    # Set coverage file
    COV_SUFFIX = str('_assembly_depth.txt')
    ASMBL_SUFFIX = str('_assembly.fa')
    coverage_file = assembly.replace('de_novo/', '').replace(ASMBL_SUFFIX,
                                                             COV_SUFFIX)
    # Set patterns
    PATTERNS = str('|').join([c[0] for c in CONTIGS_SORTED])
    PATTERNS = PATTERNS.replace('+', '\\+')  # Escape '+' if it exists
    # 1) Extract data for contigs in PATTERNS
    grep_args = str('-E "') + PATTERNS + str('" ') + coverage_file
    COV_DATA = subprocess.check_output(['grep ' + grep_args],
                                       shell=True).decode()
    # 2) Re-generate coverage file without data from contigs in PATTERNS
    # WARNING: It requires a temporary file, otherwise grep will err
    grep_args = str('-Ev "') + PATTERNS + str('" ') + coverage_file + \
                str(' > ') + coverage_file.replace('.txt', '.tmp')
    cmd_output = subprocess.check_output(['grep ' + grep_args],
                                         shell=True).decode()

    # Transform data
    DEPTH, POSITION, = _coverage_processor(COV_DATA.split('\n'))
    return DEPTH, POSITION, coverage_file


def _count_merged_contigs(ASMBL: str, SEARCH_PATTERN: str='MERGED_CONTIG_') -> str:
    """
        Count number of merged contigs in ASMBL, and return the number
        plus 1 to help keep track of number of merged contigs.
    """
    grep_args = [str('-Er "') + SEARCH_PATTERN + str('"'),  # Pattern to find
                 ASMBL,  # Where to do the SEARCH_PATTERN
                 str(' | wc -l') ]  # Return number of entries
    N_MERGED_CONTIGS = subprocess.check_output(['grep ' + str(' ').join(grep_args)],
                                               shell=True).decode().split('\n')
    return int(N_MERGED_CONTIGS[0]) + 1


def _contig_writer(assembly: str, ASMBL_SEQ: dict, CONTIGS_SORTED: list,
                   COVERAGE: bool = False, ASMBL_COV: dict = None):
    """
        Given the order in CONTIGS_SORTED: 1) merge the contigs, 2) re-generate
        the assembly file, and 3) re-generate the file with coverage data.

        This method aligns the flanks of the contigs so the CDS is in-frame,
        and de-duplicates of the overlapping sequences so that translation is
        RECONST_QUERY.
    """
    if COVERAGE is True:
        ASMBL_DEPTH, ASMBL_POS, DEPTH_F = _sort_coverage(assembly,
                                                         CONTIGS_SORTED)

    CONTIG_NUMBER = _count_merged_contigs(assembly)
    NEW_CONTIG_NAME = str('MERGED_CONTIG_') + str(CONTIG_NUMBER)
    for contig in CONTIGS_SORTED:
        C_ID = contig[0]
        SCAFFOLD_FIRST = contig[1]
        RIGHT_FIT = contig[2]

        if SCAFFOLD_FIRST is None:
            NEW_CONTIG_SEQ = ASMBL_SEQ[C_ID]
            if COVERAGE is True:
                NEW_CONTIG_COV = ASMBL_DEPTH[C_ID]
                NEW_CONTIG_POS = ASMBL_POS[C_ID]
        elif SCAFFOLD_FIRST is True:
            if RIGHT_FIT is True:
                ASMBL_SEQ[C_ID] = ASMBL_SEQ[C_ID].reverse_complement()
                # Fixing the lenfth  of the alignment to 300 allows this step
                # to be faster, particularly in the case of large contigs. The
                # length must be long enough to avoid spurious positive
                # alignments.
                contig_aln = _align_seqs(NEW_CONTIG_SEQ[:300], ASMBL_SEQ[C_ID][-300:])
            else:
                contig_aln = _align_seqs(NEW_CONTIG_SEQ[-300:], ASMBL_SEQ[C_ID][:300])
            C_BOUNDARY = len(contig_aln[0][0])
            if RIGHT_FIT is True:
                NEW_CONTIG_SEQ = ASMBL_SEQ[C_ID][:-C_BOUNDARY] + NEW_CONTIG_SEQ
            else:
                NEW_CONTIG_SEQ = NEW_CONTIG_SEQ +  ASMBL_SEQ[C_ID][C_BOUNDARY:]

            if COVERAGE is True:
                if RIGHT_FIT is True:
                    ASMBL_DEPTH[C_ID] = ASMBL_DEPTH[C_ID][::-1]
                    NEW_CONTIG_COV = ASMBL_DEPTH[C_ID][:-C_BOUNDARY] + NEW_CONTIG_COV
                else:
                    NEW_CONTIG_COV = NEW_CONTIG_COV + ASMBL_DEPTH[C_ID][C_BOUNDARY:]
                # Add new positions, starting from the last known position.
                # Note ASMBL_DEPTH[C_ID][0] = 1 for all C_ID
                SHIFTED_POS = [c + NEW_CONTIG_POS[-1] - C_BOUNDARY
                               for c in ASMBL_POS[C_ID][C_BOUNDARY:]]
                NEW_CONTIG_POS = NEW_CONTIG_POS + SHIFTED_POS
        else:  # SCAFFOLD_FIRST is False
            if RIGHT_FIT is True:
                ASMBL_SEQ[C_ID] = ASMBL_SEQ[C_ID].reverse_complement()
                # Fixing the lenfth  of the alignment to 300 allows this step
                # to be faster, particularly in the case of large contigs. The
                # length must be long enough to avoid spurious positive
                # alignments.
                contig_aln = _align_seqs(NEW_CONTIG_SEQ[:300], ASMBL_SEQ[C_ID][-300:])
            else:
                contig_aln = _align_seqs(NEW_CONTIG_SEQ[-300:], ASMBL_SEQ[C_ID][:300])
            C_BOUNDARY = len(contig_aln[0][0])
            if RIGHT_FIT is True:
                NEW_CONTIG_SEQ = ASMBL_SEQ[C_ID][:-C_BOUNDARY] + NEW_CONTIG_SEQ
            else:
                NEW_CONTIG_SEQ = NEW_CONTIG_SEQ +  ASMBL_SEQ[C_ID][C_BOUNDARY:]

            if COVERAGE is True and C_ID in ASMBL_DEPTH.keys():
                # In some isolates, the housekeeping genes given to estimate the
                # baseline coverage could not be found, and so Hound is unable
                # to output coverage depth despite detecting a given sequence.
                # Skip these cases to avoid corrupting the data.
                if RIGHT_FIT is True:
                    ASMBL_DEPTH[C_ID] = ASMBL_DEPTH[C_ID][::-1]
                    NEW_CONTIG_COV = ASMBL_DEPTH[C_ID][:-C_BOUNDARY] + NEW_CONTIG_COV
                else:
                    NEW_CONTIG_COV = NEW_CONTIG_COV + ASMBL_DEPTH[C_ID][C_BOUNDARY:]
                # Shift value of positions before inserting new contig
                SHIFTED_POS = [c + len(ASMBL_DEPTH[C_ID][:-C_BOUNDARY])
                               for c in NEW_CONTIG_POS]
                NEW_CONTIG_POS = ASMBL_POS[C_ID][:-C_BOUNDARY] + SHIFTED_POS

    if COVERAGE is True:
        # Assert basic condition is met
        assert len(NEW_CONTIG_COV) == len(NEW_CONTIG_POS)

    # Write assembly data into a temporary file
    MERGED_CONTIGS = [c[0] for c in CONTIGS_SORTED]
    with open(assembly.replace('.fa', '.tmp'), 'w') as ASMBL_FILE:
        for contig in ASMBL_SEQ:
            # Write contigs that were not considered as they were
            if contig not in MERGED_CONTIGS:
                record = SeqIO.SeqRecord(ASMBL_SEQ[contig], id=contig,
                                         description='')
                SeqIO.write(record, ASMBL_FILE, 'fasta')

        # Now write the new, merged contig.
        # This will be the last contig in the assembly file
        record = SeqIO.SeqRecord(NEW_CONTIG_SEQ, id=NEW_CONTIG_NAME,
                                 description='')
        SeqIO.write(record, ASMBL_FILE, 'fasta')

    if COVERAGE is True:
        # Overwrite coverage data
        with open(DEPTH_F.replace('.txt', '.tmp'), 'a', encoding='utf-8') as \
             COVERAGE_FILE:
            coverage_writer = csv.writer(COVERAGE_FILE, dialect='unix',
                                         delimiter='\t', quoting=csv.QUOTE_NONE)
            for i in range(len(NEW_CONTIG_COV)):
                coverage_writer.writerow([NEW_CONTIG_NAME, NEW_CONTIG_POS[i],
                                          NEW_CONTIG_COV[i]])

        # Overwrite coverage depth file & delete temporary file
        os.rename(DEPTH_F.replace('.txt', '.tmp'), DEPTH_F)

    # Overwrite assembly & delete assembly temp
    os.rename(assembly.replace('.fa', '.tmp'), assembly)
    return


def merge_contigs(assembly: str, blast_report: str, TARGET_GENES: str,
                  ID_THRESHOLD: float, DIR_DEPTH: int, HK_GENES: str,
                  CALC_COVERAGE: bool, FIND_NT: bool = False,
                  N_THREADS: int = 1, de_novo: bool = False,
                  merge_coverage: bool = False) -> bool:
    """
        This function screens blast_report to check if TARGET_GENES are
        contained within a single contig. If not, re-construct TARGET_GENES
        from contigs in blast_report.
    """
    import textwrap as tw
    from .ncbi import find_amr_genes

    # Step 0: Does blast_report exist?
    file_stats = os.lstat(blast_report)
    if file_stats.st_size > 0:
        target_genes = SeqIO.parse(TARGET_GENES, 'fasta')
        BLAST_output = [entry for entry in csv.reader(open(blast_report, 'r'),
                                                      delimiter='\t')]
        LOCI_FOUND = [entry[0] for entry in BLAST_output if
                      float(entry[2]) >= ID_THRESHOLD]

        if len(LOCI_FOUND) > 0:
            SEQ_ID, PRJ_PATH = _extract_assembly_ID(assembly, DIR_DEPTH, de_novo)

        # Step 1: Is query contained within a single contig?
        for query in target_genes:
            # Was the current query found?
            if query.name in LOCI_FOUND:
                    CONTIGS_W_QUERY = _check_query_in_contig(query.name,
                                                             query.seq,
                                                             BLAST_output,
                                                             ID_THRESHOLD)
                    if len(CONTIGS_W_QUERY) > 1:
                        # Step 2: query spans multiple contigs, sort and merge them
                        msg = str("Merging contigs to reconstruct '" +
                                  query.name + "' in assembly '" +
                                  SEQ_ID.split('_assembly.fa')[0] + "'...")
                        print(tw.fill(msg))
                        ASMBL_SEQ = _load_assembly(assembly)
                        CONTIGS_SORTED = _contig_sorter(CONTIGS_W_QUERY, ASMBL_SEQ)
                        _contig_writer(assembly, ASMBL_SEQ, CONTIGS_SORTED,
                                       COVERAGE=merge_coverage)
                        # Update BLAST_output by re-running BLAST:
                        find_amr_genes(assembly, TARGET_GENES, HK_GENES,
                                       CALC_COVERAGE, FIND_NT, N_THREADS, True)
                        BLAST_output = [entry for entry in csv.reader(open(blast_report, 'r'),
                                                      delimiter='\t')]

