from Bio import SeqIO, Seq
from Bio.Align import PairwiseAligner, substitution_matrices
from ._mutant_classifier import _curate_mutations, _find_mutation_type, \
                                _is_truncated, _are_insertions
from HoundAnalyser.helper_func.promoter_tools import _find_mutations
import textwrap as tw


def _align_seqs(SEQ_A, SEQ_B, PROMOTER=False):
    """
        Basic pair-wise sequence alignment.
    """
    aligner = PairwiseAligner()
    aligner.mode = 'global'  # 'global' for gaps, 'local' for alignment window
    if PROMOTER is True:
        aligner.gap_score = -99950
        aligner.extend_gap_score = -99950
    else:
        aligner.gap_score = -1950
        aligner.extend_gap_score = -1950
        aligner.substitution_matrix = substitution_matrices.load('BLOSUM62')
    return next(aligner.align(SEQ_A, SEQ_B))


def _preprocess_query(SEQ: Seq, REFERENCE_SEQ: Seq, PROMOTER_FILE: str = None) -> Seq:
    """
        Preprocess query sequences to address gaps '-' that affect the
        appropriate translation to amino acid sequence.
    """
    # Remove gaps, and move them to the end of sequence (only if .aln are used)
    SEQ.seq = SEQ.seq.replace('-', '')
    REFERENCE_SEQ = REFERENCE_SEQ.replace('-', '')

    if PROMOTER_FILE is None:
        # Remove anything after early STOP codon, if it exists
        if SEQ.translate().seq.count('*') > 1:
            STOP_ID = SEQ.translate().seq.find('*')  # Find first STOP location
            SEQ.seq = SEQ.seq[:STOP_ID * 3 + 3]  # Helps classify early STOP
            N_GAPS = len(REFERENCE_SEQ)*3 - len(SEQ.seq)
            assert N_GAPS >= 0
            for gap in range(N_GAPS):
                SEQ.seq += str('N')

        # Align
        aln = _align_seqs(REFERENCE_SEQ, SEQ.translate().seq)
        ref_seq, qry_seq = aln  # This line allows to extract GAPS in alignment

        seq_diff = len(REFERENCE_SEQ)*3 - int(len(SEQ.seq))
        # Identify insertions in SEQ with respect to REFERENCE_SEQ
        if seq_diff == 0:  # Identical sequences
            return SEQ, REFERENCE_SEQ
        elif seq_diff < 0 and abs(seq_diff) % 3 == 0:  # Insertion in SEQ
            REFERENCE_SEQ = Seq.Seq(ref_seq)  # To pass assertion test
        else:  # Workaround to introduce gaps in SEQ
            if SEQ.seq[-3:] != str('TAA') or SEQ.seq[-3:] != str('TGA') or\
               SEQ.seq[-3:] != str('TAG'):  # Likely truncation found
                for i in range(seq_diff):
                    SEQ.seq += str('N')
                else:
                    # Truncation at the end of beginning of CDS?
                    if SEQ.translate().seq.count('*') == 2:
                        IDX = SEQ.translate().seq.rfind('*') * 3 - 1  # -1 compensates 2xSTOP
                    else:
                        IDX = SEQ.translate().seq.rfind('*') * 3 + 2  # +2 to cover STOP

                    if qry_seq[0] == str('-'):
                        SEQ.seq = SEQ.seq[IDX+1:] + SEQ.seq[:IDX+1]  # Move added Ns to beginning CDS
    else:
        # Align
        aln = _align_seqs(REFERENCE_SEQ, SEQ.seq)
        ref_seq, qry_seq = aln  # This line allows to extract GAPS in alignment

        seq_diff = len(REFERENCE_SEQ) - int(len(SEQ.seq))
        if seq_diff == 0:  # Identical sequences
            return SEQ, REFERENCE_SEQ
        elif seq_diff < 0 and abs(seq_diff) % 3 == 0:  # Insertion in SEQ
            REFERENCE_SEQ = Seq.Seq(ref_seq)  # To pass assertion test
        else:  # Workaround to introduce gaps in SEQ (cannot edit directly)
            SEQ.seq = Seq.Seq(qry_seq)  # To pass assertion test
    return SEQ, REFERENCE_SEQ


def _find_start_codon(SEQ: Seq, REFERENCE_SEQS: Seq) -> int:
    """
        Provided a sequence with Promoter + CDS, find the start codon to
        properly index the location of the promoter mutations. The first
        residue of the start codon ('A') being +1.
    """
    SEQ.seq = SEQ.seq.replace('-', '')  # Remove gaps from sequence
    REFERENCE_CODON = [s for s in REFERENCE_SEQS if 'ATG' in s.name][0]
    # TODO: What if mutations in the START codon?
    IDX = SEQ.seq.find(REFERENCE_CODON.seq)
    if IDX > 1:
        return IDX
    elif SEQ.seq[-3:] != str('TAA') or SEQ.seq[-3:] != str('TGA') or\
            SEQ.seq[-3:] != str('TAG'):  # Check CDS not truncated at the START
        IDX = SEQ.seq.rfind('ATG')
    else:
        return None


def _find_promoter_rois(SEQ: Seq, REFERENCE_SEQ: Seq) -> list:
    """
        Find REFERENCE_SEQ and cluster them. In the case of TEM-1,
        this should be TWO clusters: Pb (closest to ATG) and P3
    """
    # TODO/FIX: This is bespoke for TEM promoter regions.
    # Make it general/generic?
    Pb_seq = list()
    Pb_loc = list()
    P3_seq = list()
    P3_loc = list()
    PROMOTER = None
    # Retrieve locations
    for REFERENCE in REFERENCE_SEQ:
        if 'Promoter' in REFERENCE.name:
            PROMOTER = REFERENCE.seq
        elif 'Pb' in REFERENCE.name or 'Pa' in REFERENCE.name:
            Pb_seq.append(REFERENCE.seq)
            INIT = PROMOTER.find(str(REFERENCE.seq))
            END = INIT + len(REFERENCE.seq)
            Pb_loc.extend([INIT, END])
        elif 'P3' in REFERENCE.name or 'P_3' in REFERENCE.name:
            P3_seq.append(REFERENCE.seq)
            INIT = PROMOTER.find(str(REFERENCE.seq))
            END = INIT + len(REFERENCE.seq)
            P3_loc.extend([INIT, END])

    OFFSET = 8  # Add position immediately next to ROIs. TODO: Give user choice?
    Pb = list([min(Pb_loc) - OFFSET, max(Pb_loc) + OFFSET])
    P3 = list([min(P3_loc) - OFFSET, max(P3_loc) + OFFSET])
    # Are Pb coordinates inside P3 coordinates? (messed sequences)?
    if Pb[0] >= P3[0] and Pb[1] <= P3[1]:
        # Pb 'sandwiched' inside P3
        Pb = P3
    elif P3[0] >= Pb[0] and P3[1] <= Pb[1]:
        # P3 'sandwiched' inside Pb
        P3 = Pb

    if PROMOTER is None:
        return [Pb, P3], [None, None], None
    else:
        return [Pb, P3], [PROMOTER[Pb[0]:Pb[1]], PROMOTER[P3[0]:P3[1]]], PROMOTER


def _identify_reference(SEQ: Seq, REFERENCE_FILE: list) -> Seq:
    """
        Screen through REFERENCE_FILE list to find which specific
        sequence needs to be used as reference sequence.
    """
    if len(REFERENCE_FILE) == 1:
        return REFERENCE_FILE[0].seq, REFERENCE_FILE[0].description
    else:
        REFERENCE_SEQ = [s for s in REFERENCE_FILE if s.name in SEQ.description]
        if len(REFERENCE_SEQ) == 0:
            return None, None
        else:
            return REFERENCE_SEQ[0].seq, REFERENCE_SEQ[0].description


def _identify_gene_organism(REFERENCE_DESC: str, REFERENCE_FNAME: str = None) -> str:
    """
        Retrieve species from reference sequence, if it exists. Otherwise,
        return the accession code used.
    """
    if REFERENCE_DESC.count(' [') > 0:  # Species included in query
        ORGANISM = REFERENCE_DESC.split('[')[-1].split(']')[0]
        GENE_NAME = REFERENCE_DESC.split(' ')[-2]
    elif REFERENCE_DESC.count('_') > 1 and REFERENCE_DESC.count(':') <= 1:
        # Formatted as ResFinderDB
        ACCESSION_NUMBER = REFERENCE_DESC.split('_')[-1]
        ORGANISM = str('Database used: ACCESSION ') + ACCESSION_NUMBER
        if REFERENCE_DESC.split('_')[1].isdigit():
            LOCUS_N = REFERENCE_DESC.split('_')[1]
        else:
            LOCUS_N = REFERENCE_DESC.split('_')[2]
        if LOCUS_N.isnumeric() and int(LOCUS_N) > 1:
            GENE_NAME = str('_').join(REFERENCE_DESC.split('_')[:2])
        else:
            GENE_NAME = REFERENCE_DESC.split('_')[0]
    elif REFERENCE_DESC.count(':') >= 2:
        # Formatted as VirulenceFinderDB
        ACCESSION_NUMBER = REFERENCE_DESC.split(':')[-1]
        ORGANISM = str('Database used: ACCESSION ') + ACCESSION_NUMBER
        if int(REFERENCE_DESC.split(':')[1]) > 1:
            GENE_NAME = str('_').join(REFERENCE_DESC.split(':')[:2])
        else:
            GENE_NAME = REFERENCE_DESC.split(':')[0]
    elif str('NC_') in REFERENCE_DESC:  # Header from nucleotide FASTA
        msg = str("(Hound *GROWLED*) Looks like the header in query file is \
                  from a translated nucleotide sequence and it is incomplete. \
                  Guessing metadata...")
        print(tw.fill(msg))
        # These headers don't typically contain gene name, use fname instead
        GENE_NAME = REFERENCE_FNAME.split('/')[-1].split('.')[0]
        ORGANISM = str(' ').join(REFERENCE_DESC.split(' ')[1:])
    else:
        msg = str("(Hound *GROWLED*) Looks like this entry was made by hand. \
                  Guessing metadata...")
        print(tw.fill(msg))
        if len(REFERENCE_DESC.split(' ')) > 1:
            GENE_NAME = REFERENCE_DESC.split(' ')[-2]
            ORGANISM = REFERENCE_DESC.split(' ')[-1]
        else:
            GENE_NAME = REFERENCE_DESC
            ORGANISM = str("Unknown (entry made by hand)")
    return GENE_NAME, ORGANISM


def screen_mut_data(FILE: str, REF_FILE: str, PROMOTER_FILE: str = None) -> dict:
    """
        Compare each entry of the alignment in FILE to reference in REF_FILE,
        after removing gaps, to find mutations.
    """
    if PROMOTER_FILE is None:
        # FILE does not contain the promoter, only CDS
        REFERENCE_FILE = [s for s in SeqIO.parse(REF_FILE, 'fasta')]
        FA_OUTPUT = [s for s in SeqIO.parse(FILE, 'fasta')]

        mut_data = dict()
        trunc_data = dict()
        ins_data = dict()
        stop_data = dict()
        id_data = dict()
        species_data = dict()
        for SEQ in FA_OUTPUT:
            # Extract isolate ID
            isolate = SEQ.name.split('__')[0]
            if len(SEQ) > 0 and SEQ.description.split('_')[-1][:-1] != str('[NO HITS'):
                # Extract reference sequence, gene name, and organism
                REFERENCE_SEQ, REFERENCE_DESC = _identify_reference(SEQ, REFERENCE_FILE)
                GENE_NAME, ORGANISM = _identify_gene_organism(REFERENCE_DESC,
                                                              REF_FILE)

                if GENE_NAME is False:  # FASTA contains ONE query sequence
                    GENE_NAME = REF_FILE.split('/')[-1].rstrip('.fasta')

                # Ensure STOP codon '*' is present in the sequence
                if REFERENCE_SEQ[-1] != str('*'):  # TAA not included
                    REFERENCE_SEQ = REFERENCE_SEQ + str('*')

                # Harmonise query and reference in case of existence of gaps
                SEQ, REFERENCE_SEQ = _preprocess_query(SEQ, REFERENCE_SEQ)

                if isolate in species_data.keys():
                    species_data[isolate].append(list([GENE_NAME, ORGANISM]))
                else:
                    species_data[isolate] = list([[GENE_NAME, ORGANISM]])

                if isolate in id_data.keys():
                    id_data[isolate].append(list([GENE_NAME,
                                                  SEQ.description.split(' ID')[-1]]))
                else:
                    id_data[isolate] = list([[GENE_NAME, SEQ.description.split(' ID')[-1]]])

                # Estimate truncations
                if SEQ.translate().seq.count('X') / len(REFERENCE_SEQ) > 0:  # Ns are translated as X
                    TRUNCATED = SEQ.translate().seq.count('X') / len(REFERENCE_SEQ)
                else:
                    TRUNCATED = False
                if isolate in trunc_data.keys():
                    trunc_data[isolate].append(list([GENE_NAME, TRUNCATED]))
                else:
                    trunc_data[isolate] = list([[GENE_NAME, TRUNCATED]])

                # Estimate insertions
                if REFERENCE_SEQ.count('-') > 0:
                    INSERTION = REFERENCE_SEQ.count('-')
                else:
                    INSERTION = False
                if isolate in ins_data.keys():
                    ins_data[isolate].append(list([GENE_NAME, INSERTION]))
                else:
                    ins_data[isolate] = list([[GENE_NAME, INSERTION]])

                # Early STOP codon
                if SEQ.translate().seq.count('*') > 1:
                    PREMATURE = True
                else:
                    PREMATURE = False
                if isolate in stop_data.keys():
                    stop_data[isolate].append(list([GENE_NAME, PREMATURE]))
                else:
                    stop_data[isolate] = list([[GENE_NAME, PREMATURE]])

                # Find mutations
                if SEQ.translate().seq != REFERENCE_SEQ:
                    mut_locations = _curate_mutations(_find_mutations(SEQ.translate().seq,
                                                                      REFERENCE_SEQ,
                                                                      None), SEQ)
                    if mut_locations is None:
                        # SEQ is subset of REFERENCE_SEQ, but have same sequence
                        if isolate in mut_data.keys():
                            mut_data[isolate].append(list([GENE_NAME, None]))
                        else:
                            mut_data[isolate] = list([[GENE_NAME, None]])
                    elif len(mut_locations) == 1:
                        mut_type = _find_mutation_type(SEQ.translate().seq,
                                                       REFERENCE_SEQ,
                                                       mut_locations[0])
                        if isolate in mut_data.keys():
                            mut_data[isolate].append(list([GENE_NAME,
                                                           [mut_locations[0],
                                                            mut_type]]))
                        else:
                            mut_data[isolate] = list([[GENE_NAME,
                                                      [mut_locations[0],
                                                       mut_type]]])
                    else:
                        mut_list = list()
                        for mut in mut_locations:
                            mut_type = _find_mutation_type(SEQ.translate().seq,
                                                           REFERENCE_SEQ, mut)
                            mut_list.append([mut, mut_type])

                        if isolate in mut_data.keys():
                            mut_data[isolate].append(list([GENE_NAME, mut_list]))
                        else:
                            mut_data[isolate] = list([[GENE_NAME, mut_list]])
                else:  # SEQ == REFERENCE_SEQ
                    # If mut_data[isolate] = None,
                    # Hound can err with 'NoneType' has no 'append'
                    if isolate in mut_data.keys():
                        mut_data[isolate].append([GENE_NAME, None])
                    else:
                        mut_data[isolate] = list([[GENE_NAME, None]])
            elif len(REFERENCE_FILE) == 1:  # 'NO HITS FOUND OR BELOW ID THRESHOLD'
                # If mut_data[isolate] = None,
                # Hound can err with 'NoneType' has no 'append'
                REFERENCE = SeqIO.read(REF_FILE, 'fasta')
                GENE_NAME = REF_FILE.split('/')[-1].rstrip('.fasta')
                _, ORGANISM = _identify_gene_organism(REFERENCE.description,
                                                      REF_FILE)
                if isolate in mut_data.keys():
                    mut_data[isolate].append([GENE_NAME, None])
                    trunc_data[isolate].append([GENE_NAME, None])
                    ins_data[isolate].append([GENE_NAME, None])
                    stop_data[isolate].append([GENE_NAME, None])
                    id_data[isolate].append([GENE_NAME, None])
                    species_data[isolate].append([GENE_NAME, ORGANISM])
                else:
                    mut_data[isolate] = list([[GENE_NAME, None]])
                    trunc_data[isolate] = list([[GENE_NAME, None]])
                    ins_data[isolate] = list([[GENE_NAME, None]])
                    stop_data[isolate] = list([[GENE_NAME, None]])
                    id_data[isolate] = list([[GENE_NAME, None]])
                    species_data[isolate] = list([[GENE_NAME, ORGANISM]])

        if len(REFERENCE_FILE) > 1:
            # 'NO HITS FOUND OR BELOW ID THRESHOLD' and REFERENCE_FILE
            # contains multiple query sequences
            for isolate in id_data:
                MISSING_REFS = [s.description for s in REFERENCE_FILE]
                # Isolate queries that were not found
                for gene in range(len(id_data[isolate])):
                    GENE_NAME = id_data[isolate][gene][0]
                    for ref_gene in MISSING_REFS:
                        R_GENE_NAME, _ = _identify_gene_organism(ref_gene)
                        if R_GENE_NAME == GENE_NAME:
                            MISSING_REFS.remove(ref_gene)
                # Annotate queries that were not found
                for REFERENCE in MISSING_REFS:
                    # If mut_data[isolate] = None,
                    # Hound can err with 'NoneType' has no 'append'
                    GENE_NAME, ORGANISM = _identify_gene_organism(REFERENCE)
                    if isolate in mut_data.keys():
                        mut_data[isolate].append([GENE_NAME, None])
                        trunc_data[isolate].append([GENE_NAME, None])
                        ins_data[isolate].append([GENE_NAME, None])
                        stop_data[isolate].append([GENE_NAME, None])
                        id_data[isolate].append([GENE_NAME, None])
                        species_data[isolate].append([GENE_NAME, ORGANISM])
                    else:
                        mut_data[isolate] = list([[GENE_NAME, None]])
                        trunc_data[isolate] = list([[GENE_NAME, None]])
                        ins_data[isolate] = list([[GENE_NAME, None]])
                        stop_data[isolate] = list([[GENE_NAME, None]])
                        id_data[isolate] = list([[GENE_NAME, None]])
                        species_data[isolate] = list([[GENE_NAME, ORGANISM]])
    else:
        # File contains promoter sequences only
        REFERENCE_SEQS = [s for s in SeqIO.parse(PROMOTER_FILE, 'fasta')]
        REFERENCE_CDS = SeqIO.read(REF_FILE, 'fasta')
        GENE_NAME, ORGANISM = _identify_gene_organism(REFERENCE_CDS.description,
                                                      REF_FILE)
        if GENE_NAME is False:  # FASTA contains ONE query sequence
            GENE_NAME = PROMOTER_FILE.split('/')[-1].rstrip('.fasta')
        FA_OUTPUT = [s for s in SeqIO.parse(FILE, 'fasta')]

        mut_data = dict()
        trunc_data = dict()
        ins_data = dict()
        stop_data = dict()
        id_data = dict()
        species_data = dict()  # Added for consistency of outputs
        for SEQ in FA_OUTPUT:
            isolate = SEQ.name.split('__')[0]
            if isolate in id_data.keys():
                id_data[isolate].append([GENE_NAME, SEQ.description.split(' ID')[-1]])
            else:
                id_data[isolate] = list([[GENE_NAME, SEQ.description.split(' ID')[-1]]])

            if len(SEQ) > 0 and SEQ.description.split('_')[-1][:-1] != str('[NO HITS'):

                if isolate in mut_data.keys():
                    species_data[isolate].append([GENE_NAME, ORGANISM])
                else:
                    species_data[isolate] = list([[GENE_NAME, ORGANISM]])

                # Find start codon (ATG) in SEQ, C_FACTOR = 'A' position
                C_FACTOR = _find_start_codon(SEQ, REFERENCE_SEQS)
                PROMOTER_SEQ = SEQ[:C_FACTOR]

                # Is the promoter (also possibly part of CDS) truncated?
                if PROMOTER_SEQ.seq[-3:] == str('TAA') or \
                   PROMOTER_SEQ.seq[-3:] == str('TGA') or \
                   PROMOTER_SEQ.seq[-3:] == str('TAG'):
                    PROMOTER_SEQ = list()

                if len(PROMOTER_SEQ) > 0:
                    PROMOTER_ROI_LOC, PROMOTER_ROI_SEQ, \
                        REFERENCE_SEQ = _find_promoter_rois(PROMOTER_SEQ,
                                                            REFERENCE_SEQS)

                    if len(REFERENCE_SEQ) < len(PROMOTER_SEQ.seq):
                        # Chosen promoter is larger than reference promoter
                        DIFF = abs(len(PROMOTER_SEQ.seq) - len(REFERENCE_SEQ))
                        PROMOTER_SEQ = PROMOTER_SEQ[DIFF:]

                    if PROMOTER_ROI_LOC[0] == PROMOTER_ROI_LOC[1]:
                        PROMOTER_ROI_LOC = PROMOTER_ROI_LOC[0]

                    # Ensure REFERENCE_SEQ and PROMOTER_SEQ have same length
                    PROMOTER_SEQ, REFERENCE_SEQ = _preprocess_query(PROMOTER_SEQ,
                                                                    REFERENCE_SEQ,
                                                                    PROMOTER_FILE)

                    # Correct C_FACTOR now that both sequences have the same length
                    C_FACTOR = len(REFERENCE_SEQ)

                    if REFERENCE_SEQ is not None:
                        if isolate in mut_data.keys():
                            trunc_data[isolate].append([GENE_NAME, _is_truncated(PROMOTER_SEQ, REFERENCE_SEQ)])
                            ins_data[isolate].append([GENE_NAME, _are_insertions(PROMOTER_SEQ, REFERENCE_SEQ)])
                            # Does not apply with Promoters. Leave as output used elsewhere
                            stop_data[isolate].append([GENE_NAME, False])
                        else:
                            trunc_data[isolate] = list([[GENE_NAME, _is_truncated(PROMOTER_SEQ, REFERENCE_SEQ)]])
                            ins_data[isolate] = list([[GENE_NAME, _are_insertions(PROMOTER_SEQ, REFERENCE_SEQ)]])
                            # Does not apply with Promoters. Leave as output used elsewhere
                            stop_data[isolate] = list([[GENE_NAME, False]])

                        if PROMOTER_SEQ.seq != REFERENCE_SEQ:
                            mut_locations = _curate_mutations(_find_mutations(PROMOTER_SEQ.seq,
                                                                              REFERENCE_SEQ,
                                                                              None),
                                                                              PROMOTER_SEQ,
                                                                              PROMOTER_FILE,
                                                                              PROMOTER_ROI_LOC)

                            if mut_locations is None:
                                # SEQ is subset of REFERENCE_SEQ, but have same sequence
                                if isolate in mut_data.keys():
                                    mut_data[isolate].append(list([GENE_NAME, None]))
                                else:
                                    mut_data[isolate] = list([[GENE_NAME, None]])
                            elif len(mut_locations) == 1:
                                mut_type = _find_mutation_type(PROMOTER_SEQ.seq,
                                                               REFERENCE_SEQ,
                                                               mut_locations[0],
                                                               PROMOTER_FILE)
                                if mut_type is not None:
                                    if isolate in mut_data.keys():
                                        mut_data[isolate].append(list([GENE_NAME,
                                                                      [mut_locations[0] - C_FACTOR,
                                                                       mut_type]]))
                                    else:
                                        mut_data[isolate] = list([[GENE_NAME,
                                                                  [mut_locations[0] - C_FACTOR,
                                                                   mut_type]]])
                                else:  # mut_type == None
                                    if isolate in mut_data.keys():
                                        mut_data[isolate].append(list([GENE_NAME, [None, None]]))
                                    else:
                                        mut_data[isolate] = list([[GENE_NAME, [None, None]]])
                            else:
                                mut_list = list()
                                for mut in mut_locations:
                                    mut_type = _find_mutation_type(PROMOTER_SEQ.seq,
                                                                   REFERENCE_SEQ, mut,
                                                                   PROMOTER_FILE)
                                    if mut_type is not None:
                                        mut_list.append([mut - C_FACTOR, mut_type])

                                    if isolate in mut_data.keys():
                                        mut_data[isolate].append(list([GENE_NAME, mut_list]))
                                    else:
                                        mut_data[isolate] = list([[GENE_NAME, mut_list]])
                        else:
                            # If mut_data[isolate] = None,
                            # Hound can err with 'NoneType' has no 'append'
                            # GENE_NAME = REF_FILE.split('/')[-1].rstrip('.fasta')
                            if isolate in mut_data.keys():
                                mut_data[isolate].append([GENE_NAME, None])
                            else:
                                mut_data[isolate] = list([[GENE_NAME, None]])
                    else:
                        # If mut_data[isolate] = None,
                        # Hound can err with 'NoneType' has no 'append'
                        # GENE_NAME = REF_FILE.split('/')[-1].rstrip('.fasta')
                        if isolate in mut_data.keys():
                            mut_data[isolate].append([GENE_NAME, None])
                            trunc_data[isolate].append([GENE_NAME, 1.0])
                        else:
                            mut_data[isolate] = list([[GENE_NAME, None]])
                            trunc_data[isolate] = list([[GENE_NAME, 1.0]])
                else:  # len(PROMOTER_SEQ) == 0
                    # If mut_data[isolate] = None,
                    # Hound can err with 'NoneType' has no 'append'
                    # GENE_NAME = REF_FILE.split('/')[-1].rstrip('.fasta')
                    if isolate in mut_data.keys():
                        mut_data[isolate].append([GENE_NAME, None])
                        trunc_data[isolate].append([GENE_NAME, 1.0])
                        ins_data[isolate].append([GENE_NAME, None])
                        stop_data[isolate].append([GENE_NAME, None])
                        id_data[isolate].append([GENE_NAME, None])
                        species_data[isolate].append([GENE_NAME, ORGANISM])
                    else:
                        mut_data[isolate] = list([[GENE_NAME, None]])
                        trunc_data[isolate] = list([[GENE_NAME, 1.0]])
                        ins_data[isolate] = list([[GENE_NAME, None]])
                        stop_data[isolate] = list([[GENE_NAME, None]])
                        id_data[isolate] = list([[GENE_NAME, None]])
                        species_data[isolate] = list([[GENE_NAME, ORGANISM]])
            else:  # len(PROMOTER_SEQ) == 0
                # If mut_data[isolate] = None,
                # Hound can err with 'NoneType' has no 'append'
                # GENE_NAME = REF_FILE.split('/')[-1].rstrip('.fasta')
                if isolate in mut_data.keys():
                    mut_data[isolate].append([GENE_NAME, None])
                    trunc_data[isolate].append([GENE_NAME, 1.0])
                    ins_data[isolate].append([GENE_NAME, None])
                    stop_data[isolate].append([GENE_NAME, None])
                    id_data[isolate].append([GENE_NAME, None])
                    species_data[isolate].append([GENE_NAME, ORGANISM])
                else:
                    mut_data[isolate] = list([[GENE_NAME, None]])
                    trunc_data[isolate] = list([[GENE_NAME, 1.0]])
                    ins_data[isolate] = list([[GENE_NAME, None]])
                    stop_data[isolate] = list([[GENE_NAME, None]])
                    id_data[isolate] = list([[GENE_NAME, None]])
                    species_data[isolate] = list([[GENE_NAME, ORGANISM]])
    return mut_data, trunc_data, id_data, ins_data, stop_data, GENE_NAME, species_data
