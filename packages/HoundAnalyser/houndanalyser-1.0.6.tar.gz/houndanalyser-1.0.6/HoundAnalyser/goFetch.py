from multiprocessing import cpu_count
from .helper_func import preprocess_reads, process_reads, retrieve_reads, \
                         retrieve_depth, extract_genes_seq, house_keeping, \
                         collate_gene_seq, analyse_seqs_found, plot_analysis, \
                         sanitise_options, parse_directories_init, \
                         retrieve_phylogeny, organise_data
from .helper_func.promoter_tools import _extract_coverage
from .data_hoover import collate_results, list_assemblies_processed
import os
import gc
import sys
import psutil
sys.setrecursionlimit(6000)  # Defaults to 3000, may not be enough for some isolates


def main(Opts):
    """
        Main function
    """
    # Check Opts consistency
    options = sanitise_options(Opts)

    # Set available CPUs minus 1, to allow the system to be responsive
    N_CPU = cpu_count() - 1

    if options.PREPROCESS is not None:
        ZIP_FILE = options.PREPROCESS[0]
        DEST_DIR = options.PREPROCESS[1]
        preprocess_reads(ZIP_FILE, DEST_DIR)
    else:
        # htps://github.com/ablab/spades/issues/19#issuecomment-631981051
        # SPAdes allocates fixed amount of memory per thread for some stages
        # of the assembly process. Reduce N_CPU from to circumvent errors of
        # memory limitation.
        if options.ASSEMBLE is True and options.ASSEMBLE_DENOVO is True:
            SYS_MEM = psutil.virtual_memory().total / 10**9  # Memory in GiB

        try:
            if options.ORGANISE is True and\
               os.path.isdir(options.PATH + str('/reads/')) is False:
               os.mkdir(options.PATH + str('/reads/'))
            DIR_LIST = os.listdir(options.PATH)
        except FileNotFoundError:
            print("(Hound *BARKED*) Directory used with '--project' does not exist. Typo?")
            sys.exit(-3)

        DIR_LIST = sorted([DIR for DIR in DIR_LIST if DIR.find(".") == -1])
        if str('reads') in DIR_LIST:  # If 'reads' found, then PATH -> DIR_LIST
            DIR_LIST = list([options.PATH.split('/')[-1],])

        for DIR in DIR_LIST:
            PRJ_NAME, READS_PATH, DIR_DEPTH = parse_directories_init(options.PATH, DIR)
            if DIR_DEPTH > 2:
                err_msg = str("(HOUND *BARKED*) Folder structure is too deep, "\
                              "please re-arrange your data into fewer folders.")
                print(err_msg)
                break

            if options.ASSEMBLE is True:
                rds_count = 1
                illumina_rds = retrieve_reads(path=READS_PATH)
                for rd in illumina_rds[0:-1:2]:
                    print("\nGenerating %i of %i assemblies." % (rds_count,
                                                                 len(illumina_rds[0:-1:2])))
                    if os.path.exists(rd.replace('_1_', '_2_')) is True:
                        if options.ASSEMBLE_DENOVO is True:  # ASSEMBLE DE NOVO
                            ASSEMBLY_PATH, \
                                DEPTH_PATH, \
                                REFERENCE_PATH = process_reads(rd, options.REF_GENOME,
                                                               PRJ_NAME, N_CPU,
                                                               options.ASSEMBLE_DENOVO,
                                                               options.CALC_COVERAGE)
                        else:  # ASSEMBLE USING REFERENCE GENOME
                            ASSEMBLY_PATH,\
                                DEPTH_PATH,\
                                REFERENCE_PATH = process_reads(rd, options.REF_GENOME,
                                                               PRJ_NAME, N_CPU,
                                                               options.ASSEMBLE_DENOVO,
                                                               options.CALC_COVERAGE,
                                                               SYS_MEM)
                    else:
                        print("Read file", rd.replace('_1_', '_2_'), "not found. Skipping.\n")
                    # Update count
                    rds_count += 1

                # Remove alignment files to save space? (Take up more than 85% of space)
                if options.ASSEMBLE_DENOVO is True:
                    house_keeping(ASSEMBLY_PATH, alignments=True)
                else:
                    house_keeping(ASSEMBLY_PATH.replace('/reference_mapped', ''),
                                  alignments=True)
            else:
                if options.ASSEMBLE_DENOVO is True and options.REF_GENOME is None:
                    if DIR_DEPTH == 1:
                        ASSEMBLY_PATH = str("/").join([options.PATH, 'assemblies/de_novo/'])
                    else:
                        ASSEMBLY_PATH = str("/").join([options.PATH, DIR, 'assemblies/de_novo/'])
                elif options.ASSEMBLE_DENOVO is False:
                    if DIR_DEPTH == 1:
                        ASSEMBLY_PATH = str("/").join([options.PATH, 'assemblies/reference_mapped/'])
                    else:
                        ASSEMBLY_PATH = str("/").join([options.PATH, DIR, 'assemblies/reference_mapped/'])

                    # if options.ORGANISE is False:
                    #     break  # Treat options.PATH as root directory
                else:
                    print("(Hound *GROWLED*) I don't understand your options. Exiting...")
                    sys.exit(-2)

                if options.SUMMARY is None:
                    house_keeping(ASSEMBLY_PATH, alignments=True)

                if options.PATH is not None and options.ORGANISE is True:
                    organise_data(options.PATH, ASSEMBLY_PATH)

            if options.TARGET_GENES is not None:
                # Extract information for genes of interest
                assemblies = [file for file in os.listdir(ASSEMBLY_PATH)
                              if file.find('.fa') > -1 and file.find('.fa.') == -1]

                # Exclude assemblies that have already been processed
                QUERY_NAME = options.TARGET_GENES.split('/')[-1].split('.')[0]
                excluded_assemblies, \
                    assemblies_seqfile = list_assemblies_processed(options.PATH,
                                                                   options.PREFIX,
                                                                   QUERY_NAME)
                if assemblies_seqfile is not None:
                    modifiedby_orig = os.lstat(assemblies_seqfile).st_mtime
                else:
                    modifiedby_orig = 0

                RD_DEPTH_STATS = dict() if options.CALC_COVERAGE is True else None
                for assembly in assemblies:  # Force extracting promoter + CDS
                    if assembly.split('_assembly.fa')[0] not in excluded_assemblies:
                        loci_metadata, hk_metadata, SEQ_ID, PRJ_PATH,\
                            GENES_LIST = extract_genes_seq(ASSEMBLY_PATH + assembly,
                                                           options.TARGET_GENES,
                                                           options.HK_GENES, PRJ_NAME,
                                                           options.PREFIX, DIR_DEPTH,
                                                           N_CPU, options.SEQ_CUTOFF,
                                                           options.ID_THRESHOLD,
                                                           DENOVO=options.ASSEMBLE_DENOVO,
                                                           CALC_COVERAGE=options.CALC_COVERAGE,
                                                           FIND_NT=options.NT_TYPE)
                        if loci_metadata is not None and options.CALC_COVERAGE is True:
                            # Extract coverage depth for genes of interest + MLST genes
                            RD_DEPTH,\
                                STATS = retrieve_depth((ASSEMBLY_PATH + assembly,
                                                        loci_metadata, SEQ_ID,
                                                        options.SEQ_CUTOFF, hk_metadata),
                                                       options.TARGET_GENES,
                                                       options.PREFIX, PRJ_PATH)
                            if STATS[0] is not str('NaN'):
                                RD_DEPTH_STATS[assembly] = (STATS)  # mean, std

            # Run garbage collector to free-up memory
            gc.collect()
            if options.TARGET_GENES is not None:
                if assemblies_seqfile is not None:
                    modifiedby_updated = os.lstat(assemblies_seqfile).st_mtime
                else:
                    modifiedby_updated = 1

        # Do not move inside for-loop, or will generate a phylogeny/plot per DIR
        # while updating GENES_LIST in the background if DIR_LIST has multiple DIR
        if options.PHYLOGENY is True and 'modifiedby_updated' in locals() and \
                modifiedby_orig != modifiedby_updated:
            phylogeny, alignment_file = analyse_seqs_found(GENES_LIST,
                                                           N_THREADS=N_CPU,
                                                           FLT_THR=options.FILTER_THRESHOLD)
        elif options.PHYLOGENY is True and options.FORCE is True:
            QUERY_NAME = options.TARGET_GENES.split('/')[-1].split('.')[0]
            # Define GENES_LIST
            if options.PREFIX is not None:
                GENES_LIST = options.PATH + \
                             str('/genes_found_denovo_assembly_') + \
                             QUERY_NAME + str('_') + options.PREFIX + str('.fa')
            else:
                GENES_LIST = options.PATH + \
                             str('/genes_found_denovo_assembly_') + \
                             QUERY_NAME + str('.fa')
            phylogeny, alignment_file = analyse_seqs_found(GENES_LIST,
                                                           N_THREADS=N_CPU,
                                                           FLT_THR=options.FILTER_THRESHOLD)
        else:
            phylogeny = None

        if options.PLOT_FNAME is not None:
            # If options.PHYLOGENY is not given, discover phylogeny generated
            if options.PHYLOGENY is False:
                alignment_file, phylogeny = retrieve_phylogeny(options.PATH,
                                                               options.TARGET_GENES,
                                                               options.PREFIX)
                RD_DEPTH = None
                RD_DEPTH_STATS = None

            # RD_DEPTH needed by plot_analysis routine, correct if neccessary
            if options.CALC_COVERAGE is False:
                RD_DEPTH = None
                RD_DEPTH_STATS = None
            else:
                QUERY_NAME = options.TARGET_GENES.split('/')[-1].split('.')[0]
                # Extract coverage data, don't care much about stats yet
                if options.PROMOTER is True and options.PREFIX is not None:
                    RD_DEPTH = [options.PATH + str('/') + f
                                for f in os.listdir(options.PATH) if
                                str('coverage_') in f and QUERY_NAME in f and
                                options.PREFIX in f and
                                str('promoter') in f.lower()]
                elif options.PROMOTER is True:  # options.PREFIX == None
                    RD_DEPTH = [options.PATH + str('/') + f
                                for f in os.listdir(options.PATH) if
                                str('coverage_') in f and QUERY_NAME in f and
                                str('promoter') in f.lower()]
                elif options.PREFIX is not None:  # options.PROMOTER == False
                    RD_DEPTH = [options.PATH + str('/') + f
                                for f in os.listdir(options.PATH) if
                                str('coverage_') in f and QUERY_NAME in f and
                                options.PREFIX in f and
                                str('promoter') not in f.lower()]
                else:  # options.PREFIX == None and options.PROMOTER == False
                    RD_DEPTH = [options.PATH + str('/') + f
                                for f in os.listdir(options.PATH) if
                                str('coverage_') in f and QUERY_NAME in f and
                                str('promoter') not in f.lower()]

                if len(RD_DEPTH) == 0:
                    PREFIX = str('NO PREFIX') if options.PREFIX is None else options.PREFIX
                    print("WARNING!! Read depth coverage not found. Did",
                          "you use '--coverage' for", QUERY_NAME,
                          "('" + PREFIX + "')?")
                    RD_DEPTH = None
                else:
                    RD_DEPTH = RD_DEPTH[0]
                RD_DEPTH_STATS = None

            # Proceed with plot analysis only if genes were found/added.
            if phylogeny is not None and 'modifiedby_updated' in locals() and \
                    modifiedby_orig != modifiedby_updated:
                plot_analysis(alignment_file, phylogeny, RD_DEPTH, RD_DEPTH_STATS,
                              options.PLOT_FNAME, CUTOFF=options.SEQ_CUTOFF,
                              ROI=options.ROI_COORDS, PROMOTER=options.PROMOTER,
                              LABELS=options.XLS_DB)
            elif phylogeny is not None and options.FORCE is True:
                plot_analysis(alignment_file, phylogeny, RD_DEPTH, RD_DEPTH_STATS,
                              options.PLOT_FNAME, CUTOFF=options.SEQ_CUTOFF,
                              ROI=options.ROI_COORDS, PROMOTER=options.PROMOTER,
                              LABELS=options.XLS_DB)

        # Generate summary
        if options.SUMMARY is not None:
            if options.TARGET_GENES is not None:
                collate_results(options.PATH, options.TARGET_GENES,
                                options.SUMMARY, options.PREFIX,
                                options.ASSEMBLE_DENOVO)
            elif options.TARGET_GENES_DIR is not None:
                collate_results(options.PATH, options.TARGET_GENES_DIR,
                                options.SUMMARY, options.PREFIX,
                                options.ASSEMBLE_DENOVO)
