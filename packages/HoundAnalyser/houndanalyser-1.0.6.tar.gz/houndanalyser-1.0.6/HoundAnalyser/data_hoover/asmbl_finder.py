import os
from numpy import unique
from Bio import SeqIO


# Define constants
COV_PATTERN = str('coverage_denovo_genes_')
COV_EXT = str('.txt')
ALN_PATTERN = str('genes_found_denovo_assembly_')
ALN_EXT = str('_FILTERED.aln')
FA_EXT = str('.fa')
FA_DIR = str('assemblies/de_novo/')  # TODO: add need for --de-novo?


def find_all_assemblies(ASMBL_DIR: str) -> list:
    """
        Retrieve all isolate names from ASMBL_DIR.
    """
    ASMBL_LIST = list()
    if os.path.exists(ASMBL_DIR):
        ASMBL_LIST = [FILE for FILE in os.listdir(ASMBL_DIR) if FA_EXT in FILE]
    else:
        # Look one level deeper
        ASMBL_LIST = list()
        PATH = str('/').join(ASMBL_DIR.split('/')[:-3]) + str('/')
        DIR_LIST = [DIR for DIR in os.listdir(PATH) if str('.') not in DIR]
        for DIR in DIR_LIST:
            DIR = DIR + str('/')
            if os.path.exists(PATH + DIR + FA_DIR):
                ASMBL_LIST.extend([FILE for FILE in os.listdir(PATH + DIR + FA_DIR) if FA_EXT in FILE])
    # Retrieve isolate name
    ASMBL_NAME_LIST = [ASMBL.removesuffix('_assembly.fa') for ASMBL in ASMBL_LIST if
                       FA_EXT in ASMBL and ASMBL.find(FA_EXT + '.') == -1]
    return unique(ASMBL_NAME_LIST).tolist()


def list_assemblies_processed(PATH: str, PREFIX: str, QUERY_NAME: str) -> list:
    """
        Screen PATH and return a list with all assemblies processed.
    """
    # Extract information from output files (SUMMARY)
    if PREFIX is None:
        FILE_LIST = [file for file in os.listdir(PATH) if FA_EXT in file
                     and str('_FILTERED') not in file and QUERY_NAME in file]
    else:
        FILE_LIST = [file for file in os.listdir(PATH) if FA_EXT in file
                     and str('_FILTERED') not in file and PREFIX in file
                     and QUERY_NAME in file]

    if len(FILE_LIST) == 0:
        return list([]), None
    else:
        ASMBL_LIST = list()
        for FILE in FILE_LIST:
            dataset = SeqIO.parse(str('/').join([PATH, FILE]), 'fasta')
            for ASMBL in dataset:
                ASMBL_LIST.append(ASMBL.name.split('__')[0])
        return unique(ASMBL_LIST).tolist(), str('/').join([PATH, FILE_LIST[0]])
