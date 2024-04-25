from .contig_merger import merge_contigs
from .unalignment_tools import process_unaligned
from .promoter_tools import analyse_seqs_found, plot_analysis
from .rtrv_reads import rtrv_reads as retrieve_reads
from .ncbi import find_amr_genes, compile_genes_detected, convert_to_db
from .alignment_tools import align_reads, multiple_seq_alignment,\
                             collate_gene_seq, map_denovo_reads,\
                             retrieve_phylogeny
from .assembly_utilities import retrieve_depth, calculate_assembly_depth,\
                                assemble_denovo
from .data_organiser import organise_data
from argparse import Namespace
from ete3 import PhyloTree
import os, warnings
import textwrap as tw


def sanitise_options(options):
    """
        Check that options given by user are consistent with
        their dependencies.
    """
    import sys
    sys.tracebacklimit = 0  # No traceback needed FOR THESE errors.

    if options.PATH is None and options.PREPROCESS is None:
        err_msg = str("(Hound *BARKED*) '--project DIRECTORY' is required " \
                      "to do anything with this program, unless you want to " \
                      "preprocess the reads file 'reads.zip' provided by " \
                      "your sequencing facility. Use --help for instructions.")
        raise ValueError(tw.fill(err_msg))
    elif options.PATH is not None:
        # Check if PATH has '/' and if so, remove it. Can mess with assembly.
        if options.PATH[-1] == str("/"):
            options.PATH = options.PATH[:-1]

        if options.PATH is not None and options.ASSEMBLE is False and\
           options.SUMMARY is None and options.ORGANISE is None and\
           options.TARGET_GENES is None:
            err_msg = str("(Hound *BARKED*) Don't know what to do with the " \
                          "reads. Use '--assemble' or '--genes [FILE]', or " \
                          "use --help for instructions.")
            raise ValueError(tw.fill(err_msg))

        if options.ASSEMBLE is True and options.ASSEMBLE_DENOVO is False and\
           options.REF_GENOME is None:
            err_msg = str("(Hound *BARKED*) Assembly method not specified. ")
            raise ValueError(tw.fill(err_msg))

        if options.ASSEMBLE is False and options.ASSEMBLE_DENOVO is False:
            msg = str("(Hound *GROWLED*) Assembly method no specified, " \
                      "assuming --reference.")
            print(msg)
            options.REF_GENOME = str('EMPTY')

        if options.ASSEMBLE is True and options.CALC_COVERAGE is False:
            # Bless the user, so it doesn't have to run Hound twice.
            msg = str("(Hound *ASKS*) I noticed --coverage was not passed. " \
                      "Is this correct? [Y/n]: ")
            ans = input(msg)
            if ans.lower() == 'n':
                msg = str("Stopping run. Remember to add --coverage next time.")
                print(msg)
                sys.exit(0)
        elif options.CALC_COVERAGE is True and options.HK_GENES is False:
            err_msg = str("(Hound *BARKED*) '--coverage' requires " \
                          "reference or housekeeping genes to estimate " \
                          "baseline coverage depth. Use --help for " \
                          "instructions.")
            raise ValueError(tw.fill(err_msg))

        if options.NT_TYPE is True and options.TARGET_GENES is not None:
            from Bio import SeqIO
            SEQS = [SEQ for SEQ in SeqIO.parse(options.TARGET_GENES, 'fasta')]
            if SEQS[0].translate().count('X') > 0:
                err_msg = str("(Hound *BARKED*) '--genes' points to a file " \
                              "containing amino acid sequences. '--nucl' " \
                              "requires nucleotide sequences.")
                raise ValueError(tw.fill(err_msg))

        if options.HK_GENES is True and options.CALC_COVERAGE is False:
            warn_msg = str("(Hound *GROWLED*) '--hk-genes' were given without " \
                           "'--coverage', and so they will be ignored.")
            warnings.warn(tw.fill(warn_msg))

        if options.TARGET_GENES is not None and options.ID_THRESHOLD is None:
            options.ID_THRESHOLD = tuple([0.9, 1])  # Set default values

        if options.TARGET_GENES is not None and\
           options.ASSEMBLE_DENOVO is False and options.REF_GENOME is None:
            err_msg = str("(Hound *BARKED*) '--genes' requires either " \
                          "'--de-novo' or '--reference' to know how the " \
                          "data was assembled. Use --help for instructions.")
            raise ValueError(tw.fill(err_msg))

        if options.ID_THRESHOLD is not None and options.TARGET_GENES is None:
            err_msg = str("(Hound *BARKED*) '--identity' requires '--genes " \
                          "[FILE]'. Use --help for instructions.")
            raise ValueError(tw.fill(err_msg))

        if options.SEQ_CUTOFF > 0 and options.PROMOTER is False:
            err_msg = str("(Hound *BARKED*) '--cutoff' requires '--promoter'. " \
                          "Use --help for instructions.")
            raise ValueError(tw.fill(err_msg))

        if options.ROI_COORDS is not None and options.PLOT_FNAME is False:
            err_msg = str("(Hound *BARKED*) '--roi [FILE]' requires '--plot " \
                           "[FILE]'. Use --help for instructions.")
            raise ValueError(tw.fill(err_msg))

        if options.XLS_DB is not None and options.PLOT_FNAME is None:
            err_msg = str("(Hound *BARKED*) --labels FILE requires " \
                          "--plot [FILE]. Use --help for instructions.")
            raise ValueError(tw.fill(err_msg))

        if options.PLOT_FNAME is not None and options.PLOT_FNAME.count(".") == 0:
            err_msg = str("(Hound *GROWLED* and *BARKED*) Plot filename " \
                          "given, but what extension? (.pdf / .eps / .png)")
            raise ValueError(tw.fill(err_msg))

        if options.PLOT_FNAME is not None and options.PLOT_FNAME.count(".") == 0:
            err_msg = str("(Hound *GROWLED* and *BARKED*) Spreadsheet " \
                          "filename given, but what extension? (.xls/" \
                          ".xlsx)")
            raise ValueError(tw.fill(err_msg))

        if options.SUMMARY is not None and options.TARGET_GENES is None and\
           options.TARGET_GENES_DIR is None:
            err_msg = str("(Hound *BARKED*) '--summary' requires '--genes " \
                          "[FILE]' or '--genes-dir [DIR]' to annotate " \
                          "mutations.")
            raise ValueError(tw.fill(err_msg))

    if options.ID_THRESHOLD is not None:
        options.ID_THRESHOLD = tuple(options.ID_THRESHOLD)

    if options.PATH is not None and options.PATH[0][-1] == str("/"):
        options.PATH = os.path.abspath(options.PATH[0][:-1])
    elif options.PATH is not None:
        options.PATH = os.path.abspath(options.PATH[0])

    if options.REF_GENOME is not None and options.REF_GENOME != str('EMPTY'):
        options.REF_GENOME = os.path.abspath(options.REF_GENOME[0])

    if options.PREFIX is not None:
        options.PREFIX = options.PREFIX[0]

    # Restore Traceback for debugging
    del sys.tracebacklimit

    return options


def preprocess_reads(compressed_file: str, DESTINATION: str) -> str:
    """
        Given a compressed file with [quality controlled] sequencing reads,
        decompress the file creating the appropriate directory structure for
        Hound.
    """
    if os.path.exists(compressed_file) is False:
        err_msg = str("(Hound *BARKED*) The file specified does " \
                      "not exist. Typo?")
        raise ValueError(tw.fill(err_msg))

    READS_DIR = str("reads/")
    UNPAIRED_READS_DIR = str("unpaired/")
    UNPAIRED_PATTERN = str("*_U?_*")

    if DESTINATION[-1] != str("/"):
        DESTINATION = DESTINATION + str("/")

    # Create directory structure
    os.makedirs(DESTINATION + READS_DIR + UNPAIRED_READS_DIR)
    # Decompress reads into 'reads/'
    unzip_args = list(['-j', '-d ' + str("/").join([DESTINATION, READS_DIR]),
                       compressed_file])
    os.system('unzip ' + str(" ").join(unzip_args))
    # Move unpaired reads, if any, to 'unpaired/'
    print("Sorting unpaired reads, if any...")
    move_args = list([str("/").join([DESTINATION, READS_DIR, UNPAIRED_PATTERN]),
                      str("/").join([DESTINATION, READS_DIR, UNPAIRED_READS_DIR])])
    os.system('mv ' + str(" ").join(move_args))
    print(compressed_file, "can now be deleted.")
    return


def house_keeping(assembly_path: str, alignments: bool = False) -> str:
    """
        Remove temporary files that are not longer needed after assembly.
        BLAST index files are temporary but they will be re-used with
        every new gene search---and they can be slow to produce (2-4s each).
        However BLAST output files (.blast) can cause trouble when using the
        same assemblies to look for different genes. Fast to produce (<<1s),
        delete.
    """
    if alignments is True:
        aln_path = assembly_path.replace('/assemblies', '/alignments')
        if aln_path.split('/')[-1] != str("alignments"):
            # Is this a case of '/assemblies/de_novo' to '/alignments/de_novo'?
            # If so, remove last folder from name to retrieve abs path for 'alignments'
            aln_path = str("/").join(aln_path.split('/')[:-2])
        os.system('rm -Rf ' + aln_path)
    else:
        if assembly_path.find('.fasta') > -1:  # For assemblies from MicrobesNG
            blast_output = assembly_path.replace('.fasta', '.blast')
        else:
            blast_output = assembly_path.replace('.fa', '.blast')
        if os.path.exists(blast_output) is True:
            os.system('rm ' + blast_output)


def parse_directories_init(PATH, DIR):
    """
        Checks the right folder structure exists, and returns
        project name, reads directory, and directory depth.
    """
    PRJ_NAME = DIR  # Keep this to make parsing results easier

    if os.path.exists(str("/").join([PATH, 'reads'])) is True:
        READS_PATH = str("/").join([PATH, 'reads/'])
        PRJ_NAME = PATH.split('/')[-1]  # Avoids saving files in 'reads/'
        DIR_DEPTH = 1
    elif os.path.exists(str("/").join([PATH, DIR, 'reads'])) is True:
        READS_PATH = str("/").join([PATH, DIR, 'reads/'])
        DIR_DEPTH = 2
    else:
        DIR_LIST = [DIR for DIR in os.listdir(str("/").join([PATH, DIR])) if
                    str(".") not in DIR]
        if len(DIR_LIST) == 0:
            err_msg = str("(Hound *BARKED*) The directory used with " \
                          "'--project' is empty.")
            raise ValueError(tw.fill(err_msg))
        else:
            if DIR[-1] != str("/"):
                NEW_PATH = str("/").join([PATH, DIR]) + str("/")
            else:
                NEW_PATH = str("/").join([PATH, DIR])

            NEW_DEPTH = 1
            DIR_DEPTH = 2  # Last value declared before entering this step
            for NEW_DIR in DIR_LIST:
                if os.path.exists(str("/").join([NEW_PATH, NEW_DIR, 'reads'])) is True:
                    READS_PATH = str("/").join([PATH, DIR, NEW_DIR, 'reads/'])
                    DIR_DEPTH = DIR_DEPTH + NEW_DEPTH
                    break
                else:
                    if DIR_LIST[-1] == NEW_DIR:
                        err_msg = str("(Hound *BARKED*) Directories screened " \
                                      "but nothing found. Re-arrange your data " \
                                      "and try again.")
                        raise ValueError(tw.fill(err_msg))
                    else:
                        NEW_DEPTH += 1
    return PRJ_NAME, READS_PATH, DIR_DEPTH


def process_reads(illumina_rd: str, REFERENCE: str, PRJ_NAME: str, N_CPU: int,
                  denovo_assembly: bool, calculate_coverage: bool,
                  SYS_MEM: float=8.0) -> bool:
    """
        Process illumina read to map them to a reference genome, assemble de
        novo those that could not be mapped to the reference, and find genes
        of interest using BLAST.
    """
    if denovo_assembly is False:
        # Align reads to reference if given.
        if REFERENCE is None:
            err_msg = str("(Hound *BARKED*) Trying to align to a reference, " \
                          "but no reference genome given. Provide a reference " \
                          "in FASTA format or use '--de-novo'. Use --help for " \
                          "instructions.")
            raise ValueError(tw.fill(err_msg))

        assembly, REFERENCE_PATH, \
            unaligned_template = align_reads(illumina_rd, ref_chromosome=REFERENCE,
                                             project_name=PRJ_NAME, N_THREADS=N_CPU)
        # Process those reads that could not be aligned, and assemble de novo
        # unaligned_reads = process_unaligned(unaligned_template, N_THREADS=N_CPU)
        # unmapped_assembly = assemble_denovo(unaligned_reads, assemble_unaligned,
        #                                     project_name=PRJ_NAME,
        #                                     N_THREADS=N_CPU)
        # Generate BLAST database
        convert_to_db(assembly, N_CPU)

        if calculate_coverage is True:
            depth_file = calculate_assembly_depth(assembly, N_THREADS=N_CPU)

        # Delete BAM file
        ASMBL_PATH = str("/").join(assembly.split('/')[:-1])
        [os.remove(ASMBL_PATH + str("/") + f) for f in os.listdir(ASMBL_PATH)
            if str(".bam") in f]
        return ASMBL_PATH, None, REFERENCE_PATH
    else:
        # Limit N_CPU _only_ for assembler. The rest of the pipeline can
        # benefit from using _all_ CPUs available.
        if SYS_MEM <= 18:  # If system memory is 16GB or less
            DN_CPU = min(7, N_CPU)
        elif SYS_MEM <= 36:
            # This may need testing (I don't have 32GB available)
            DN_CPU = min(14, N_CPU)

        # Assembly de novo without aligning to reference
        denovo_assembly, \
            assembly_success = assemble_denovo(illumina_rd, N_THREADS=DN_CPU,
                                               project_name=PRJ_NAME)
        if calculate_coverage is True:
            if assembly_success is True:
                mapped_assembly = map_denovo_reads(illumina_rd, denovo_assembly,
                                                   N_THREADS=N_CPU,
                                                   project_name=PRJ_NAME)
                depth_file = calculate_assembly_depth(mapped_assembly,
                                                      N_THREADS=N_CPU)
                # Generate BLAST database
                convert_to_db(denovo_assembly, N_CPU)
            else:
                # Assembly failed due to _very_ low quality reads
                # Generate depth file (empty) for convenience.
                depth_file = denovo_assembly.replace('de_novo/', '').replace('.fa', '_depth.txt')
                os.system('touch ' + depth_file)
                # Generate BLAST database
                convert_to_db(denovo_assembly, N_CPU)
            return str("/").join(denovo_assembly.split('/')[:-1]) + str("/"), \
                str("/").join(depth_file.split('/')[:-1]), None
        else:
            if assembly_success is True:
                mapped_assembly = map_denovo_reads(illumina_rd, denovo_assembly,
                                                   N_THREADS=N_CPU,
                                                   project_name=PRJ_NAME)
                # Generate BLAST database
                convert_to_db(denovo_assembly, N_CPU)
            return str("/").join(denovo_assembly.split('/')[:-1]) + str("/"), \
                None, None


def extract_genes_seq(assembly: str, TARGET_GENES: str, HK_GENES: str,
                      project_name: str, PREFIX: str, DIR_DEPTH: int,
                      N_THREADS: int, seq_cutoff: int, ID_THRESHOLD: tuple,
                      DENOVO: bool = False, CALC_COVERAGE: bool = False,
                      FIND_NT: bool = False) -> str:
    """
        Process assembly folder to retrieve BLAST output files, and parse
        them to create a FASTA file containing the nucleotidic sequence of
        all genes found in the assembly. This FASTA file will later be used
        to compare the sequences across multiples assemblies.
    """
    # Wipe previous BLAST results to avoid parsing errors
    # when using the same assembly for look for different genes
    house_keeping(assembly)

    # Find matches
    find_amr_genes(assembly, TARGET_GENES, HK_GENES, CALC_COVERAGE, FIND_NT,
                   N_THREADS)

    if assembly.find('.fasta') > -1:  # For assemblies from MicrobesNG
        blast_output = assembly.replace('.fasta', '.blast')
    else:
        blast_output = assembly.replace('.fa', '.blast')

    # Check if query needs to be used to re-construct the sequence in assembly
    if FIND_NT is False and ID_THRESHOLD[0] >= 0.9:  # AA search
        FORCE_ID_THRESHOLD = max(90.0, ID_THRESHOLD[0])
        merge_contigs(assembly, blast_output, TARGET_GENES, FORCE_ID_THRESHOLD,
                      DIR_DEPTH, HK_GENES, CALC_COVERAGE, FIND_NT, N_THREADS,
                      de_novo=DENOVO, merge_coverage=CALC_COVERAGE)
    elif FIND_NT is True and ID_THRESHOLD[0] >= 0.99:  # NT search
        FORCE_ID_THRESHOLD = max(99.0, ID_THRESHOLD[0])
        merge_contigs(assembly, blast_output, TARGET_GENES, FORCE_ID_THRESHOLD,
                      DIR_DEPTH, HK_GENES, CALC_COVERAGE, FIND_NT, N_THREADS,
                      de_novo=DENOVO, merge_coverage=CALC_COVERAGE)
    else:
        if FIND_NT is True:
            print("***WARNING*** Skipping contig merger (identity window set "\
                  "below 99% for nucleotide search)\n")
        else:
            print("***WARNING*** Skipping contig merger (identity window set "\
                  "below 90%)\n")

    gene_metadata, housekeeping_metadata, SEQ_ID, PRJ_PATH, \
        genes_list = compile_genes_detected(assembly, blast_output,
                                            TARGET_GENES, PREFIX, DIR_DEPTH,
                                            CALC_COVERAGE, seq_cutoff,
                                            ID_THRESHOLD, DENOVO)
    # Genes found?
    if os.lstat(blast_output).st_size > 0:
        return gene_metadata, housekeeping_metadata, SEQ_ID, PRJ_PATH, genes_list
    else:
        # If genes not found, create empty file to acknowledge
        # there was a search but nothing found.
        if os.path.exists(genes_list) is False:
            os.system('touch ' + genes_list)
        return None, None, SEQ_ID, PRJ_PATH, genes_list
