import os


def _create_file_list(PATH: str, DIR: str, FILTER_PATTERN: str) -> list:
    """
        Retrieve list of files for downstream processing.
    """
    FILE_LIST = os.listdir(PATH + DIR)
    FILTERED_LIST = [FILE for FILE in FILE_LIST if FILTER_PATTERN in FILE]
    return FILTERED_LIST


def extract_prefixes(PATH: str, DIR: str, FILTER_PATTERN: str,
                     FILTER_EXT: str) -> list:
    """
        Isolate search result by prefix, and return the prefix used.
    """
    FILTERED_LIST = _create_file_list(PATH, DIR, FILTER_PATTERN)
    PREFIX_LIST = list()
    INCLUDE_REF = False
    for FILE in FILTERED_LIST:
        if FILTER_EXT in FILE and str('_FILTERED') not in FILE:
            PREFIX = FILE.split(FILTER_PATTERN)[1].split(FILTER_EXT)[0]
            PREFIX_LIST.append(PREFIX)
            if str('promoter') in PREFIX.lower():
                INCLUDE_REF = True

    # If 'Promoter' is part of PREFIX_LIST, also load gene w/o Promoter
    if INCLUDE_REF is True:
        for FILE in FILTERED_LIST:
            if FILTER_EXT in FILE and PREFIX.replace('_promoter', '') in FILE.lower():
                PREFIX_LIST.append(PREFIX.replace('_promoter', ''))
    return PREFIX_LIST


def retrieve_genes_references(PREFIX_LIST: list, GENES_PATH: str) -> dict():
    """
        Retrieve fasta files with the aa sequence of the references.
    """
    references = dict()

    if GENES_PATH.split('/')[-1].find('.fa') > -1:  # GENES_PATH == FILE
        filtered_output = GENES_PATH.split('.')[0].replace('-', '').lower()
        for PREFIX in PREFIX_LIST:
            if PREFIX.replace('-', '').lower() in filtered_output:
                # fix PREFIX is gene name is used as PREFIX:
                if PREFIX.count('_') > 1:
                    PREFIX = str('_').join(PREFIX.split('_')[1:])
                elif PREFIX.count('_') == 1:
                    if str('promoter') not in PREFIX.lower():
                        PREFIX = PREFIX.split('_')[0]

                references[PREFIX] = GENES_PATH
    else:  # GENES_PATH == PATH TO FILES
        DIR_LIST = [dir for dir in os.listdir(GENES_PATH) if dir.count('.') == 0]
        for DIR in DIR_LIST:
            output = os.listdir(GENES_PATH + DIR)
            filtered_output = [s.split('.')[0].replace('-', '').lower() for s in output]
            for PREFIX in PREFIX_LIST:
                if PREFIX.replace('-', '').lower() in filtered_output:
                    # fix PREFIX is gene name is used as PREFIX:
                    if PREFIX.count('_') > 1:
                        PREFIX = str('_').join(PREFIX.split('_')[1:])
                    elif PREFIX.count('_') == 1:
                        if str('promoter') not in PREFIX.lower():
                            PREFIX = PREFIX.split('_')[0]

                    for REF_FILE in output:
                        if REF_FILE.split('.')[0].replace('-', '').lower() in \
                           PREFIX.replace('_FILTERED', '').replace('-', '').lower():
                            references[PREFIX] = GENES_PATH + DIR + str('/') + REF_FILE
    return references
