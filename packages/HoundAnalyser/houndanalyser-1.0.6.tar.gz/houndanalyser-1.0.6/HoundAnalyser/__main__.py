#!/usr/bin/env python3

from HoundAnalyser import goFetch, __version__
import argparse


def main():
    # Retrieve options from CLI #
    Args = argparse.ArgumentParser(description="HOUND: species-independent \
                                                genetic profiling system (v" +
                                                __version__ + ")",
                                   epilog="Developed by Carlos Reding \
                                   as part of FARM-SAFE \
                                   (BBSRC grant BB/T004592/1) and Arwain DGC \
                                   at the University of Bristol (United Kingdom). \
                                   If you use this software please cite the \
                                   publication in \
                                   https://academic.oup.com/bib/article/25/2/bbae057")

    Args.add_argument("--preprocess", metavar=("FILE", "DIRNAME"), type=str,
                      nargs=2, dest="PREPROCESS", help="Unzip Illumina reads \
                      and create appropriate directory structure. It requires \
                      a name to create destination directory. REQUIRED unless \
                       --project is given.")

    Args.add_argument("--organise", action='store_true', dest="ORGANISE",
                      help="Directory containing FASTA files (.fa/.fasta) to \
                      be re-organised, so that they can be processed with \
                      Hound. Requires --project.")

    Args.add_argument("--project", metavar="DIR", type=str, nargs=1,
                      dest="PATH", help="Directory where FASTQ files can be \
                      found. It can be a directory of directories if FASTQ \
                      files are contained in a 'reads' directory. Maximum \
                      directory depth is 2 (PROJECT/DIR1/DIR2). REQUIRED \
                      unless --preprocess is given.")

    Args.add_argument("--assemble", action='store_true', dest="ASSEMBLE",
                      help="Assemble reads. Requires --project.")

    Args.add_argument("--reference", metavar="FILE", type=str, nargs=1,
                      dest="REF_GENOME", help="Reference genome in FASTA format.\
                       Requires --assemble.")

    Args.add_argument("--de-novo", action='store_true', dest="ASSEMBLE_DENOVO",
                      help="Assemble reads de novo. Used to assemble genomes and\
                      specify assembly type for data analysis. Requires \
                      --assemble.")

    Args.add_argument("--coverage", action='store_true', dest="CALC_COVERAGE",
                      help="Compute coverage depth to estimate gene copy number.\
                       Can be used to assemble genomes or include coverage depth\
                       in the data analysis. Requires --hk-genes.")

    Args.add_argument("--hk-genes", metavar="FILE", type=str, dest="HK_GENES",
                      help="List of Multilocus sequence typing (MLST) \
                      genes, or other reference genes, in FASTA format to \
                      compute baseline coverage depth. Requires --coverage.")

    Args.add_argument("--genes", metavar="FILE", type=str, dest="TARGET_GENES",
                      help="List of genes to be found, in FASTA \
                      format. Requires --identity and --prefix.")

    Args.add_argument("--genes-dir", metavar="DIR", type=str, dest="TARGET_GENES_DIR",
                      help="Directory containing genes of interest in FASTA \
                      format. Requires --summary.")

    Args.add_argument("--nucl", action='store_true', dest="NT_TYPE",
                      help="Use nucleotide sequences for the search. Requires \
                      --genes.")

    Args.add_argument("--prefix", metavar="NAME", type=str, dest="PREFIX",
                      nargs=1, help="Label added to all output files. Required \
                      to do multiple searches with the same assemblies.")

    Args.add_argument("--identity", metavar="NUM", type=float, nargs=2,
                      dest="ID_THRESHOLD", help="Identity threshold required \
                      to shortlist sequences found. Two floats (min identity, \
                      max identity) between 0 and 1 are required. Requires \
                      --genes.")

    Args.add_argument("--promoter", action='store_true', dest="PROMOTER",
                      help="Isolate the promoter region of the target gene(s) \
                      sequences found and ignore coding sequences. Requires \
                      --cutoff.")

    Args.add_argument("--cutoff", metavar="NUM", type=int, default=0,
                      dest="SEQ_CUTOFF", help="Length of the promoter in \
                      nucleotides. Requires --promoter.")

    Args.add_argument("--phylo", action='store_true', dest="PHYLOGENY",
                      help="Align sequences of promoter/coding sequences found,\
                       and generate the corresponding phylogeny.")

    Args.add_argument("--phylo-thres", metavar="NUM", dest="FILTER_THRESHOLD",
                      type=float, nargs=1, default=0.5, help="Remove sequences \
                      that are a fraction of the total size of alignment. Used \
                      to improve quality alignment. Requires a number between 0\
                      and 1 (defaults to ""0.5"").")

    Args.add_argument("--plot", metavar="FILE", type=str, dest="PLOT_FNAME",
                      help="Generate plot from the multiple alignment of \
                      sequences found, and save as FILE.")

    Args.add_argument("--roi", metavar="FILE", type=str,
                      dest="ROI_COORDS", help="Sequences of interest to look \
                      for in the gene(s) found, in FASTA format. Requires \
                      --plot.")

    Args.add_argument("--summary", metavar="FILE", type=str, dest="SUMMARY",
                      help="Save Hound analysis as a spreadsheet.\
                      Requires --project.")

    Args.add_argument("--labels", metavar="FILE", type=str,
                      dest="XLS_DB", help="XLS file containing assembly name \
                      (col 1), and assembly type (col 6) to label phylogeny \
                      leafs (defaults to assembly name). Requires --plot.")

    Args.add_argument("--force", action='store_true', dest="FORCE",
                      help="Force re-generation of phylogeny and/or plot even \
                      if they already exist.")

    Args.add_argument("--version", action='version', version='v' + __version__)
 
    # Call Hound
    Opts = Args.parse_args()
    goFetch.main(Opts)


if __name__ == '__main__':
    main()
