import os
from .ncbi import convert_to_db


def organise_data(PATH: str, ASSEMBLY_PATH: str) -> bool:
    """
        When only FASTA files are available, create a folder structure inside
        PATH that Hound understand.
    """
    if PATH[-1] != str('/'):
        PATH = PATH + str('/')

    # Rename to .fa if necessary
    FASTA_FILES = [file for file in os.listdir(PATH) if
                   str('.fasta') in file or str('.fa') in file]
    if len(FASTA_FILES) > 0:
        # Create directories if necessary
        if os.path.isdir(ASSEMBLY_PATH) is False:
            os.makedirs(ASSEMBLY_PATH)

        for file in FASTA_FILES:
            # Move files to ASSEMBLY_PATH
            os.rename(PATH + file, ASSEMBLY_PATH + file.replace('.fasta', '.fa'))
            # Generate DB
            convert_to_db(ASSEMBLY_PATH + file.replace('.fasta', '.fa'), 0)
    return
