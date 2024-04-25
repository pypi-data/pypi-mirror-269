import os
import textwrap as tw


def rtrv_reads(path: str = None) -> list:
    """
        List files containing NGS illumina reads,
        and return a list with their absolute path.
    """
    if path is None:
        err_msg = str("(Hound *BARKED*) I need path where illumina reads " \
                      "are stored.")
        raise ValueError(tw.fill(err_msg))
        os.system.exit(-1)
    else:
        dir_list = sorted(os.listdir(path))
        if str('.DS_Store') in dir_list is True:
            dir_list.remove('.DS_Store')  # SH*T happens when coding in a mac...
        # Return only files, not directories
        rds_list = [os.path.abspath(path+direct) for direct in dir_list
                    if direct.find('.fastq') > -1]
        return rds_list
