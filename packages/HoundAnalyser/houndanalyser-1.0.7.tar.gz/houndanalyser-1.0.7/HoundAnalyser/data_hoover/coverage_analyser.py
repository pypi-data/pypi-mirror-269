import os
from Bio import SeqIO


def screen_cov_data(FILE: str, REFERENCE_FILE) -> dict:
    """
        Load relative coverage data from FILE.
    """
    cov_data = dict()
    if str('promoter') in REFERENCE_FILE.lower():
        QUERY_N = 1
    else:
        QUERY_N = len([s for s in SeqIO.parse(REFERENCE_FILE, 'fasta')])

    if os.path.exists(FILE):
        cov_raw = open(FILE, 'r').readlines()
        for entry in cov_raw:
            baseline = float(entry.removesuffix('\n').split('\t')[-1])
            copy_number = float(entry.removesuffix('\n').split('\t')[-2])
            isolate = entry.removesuffix('\n').split('\t')[0].removeprefix('>')

            locus_name = str(entry.removesuffix('\n').split('\t')[1])
            if QUERY_N > 1:  # FASTA files contain multiple queries
                if int(locus_name.split('_')[1]) > 1:
                    query = str('_').join(locus_name.split('_')[:2])
                else:
                    query = locus_name.split('_')[0]
            else:  # FASTA files contain ONE query each
                REFERENCE = SeqIO.read(REFERENCE_FILE, 'fasta')
                if REFERENCE.name == locus_name:
                    query = REFERENCE_FILE.split('/')[-1].removesuffix('.fasta')
                else:
                    query = locus_name
            contig = str(entry.removesuffix('\n').split('\t')[2])

            # Has 'isolate' been processed?
            if isolate not in cov_data.keys():
                if baseline == 0:
                    # Query sequence was found, but not the HKGENES provided
                    # to estimate the baseline coverage--provide more HKGENES.
                    cov_data[isolate] = list([[query, contig,
                                              str('ERR: baseline coverage is zero.')]])
                else:
                    cov_data[isolate] = list([[query, contig,
                                              round(copy_number / baseline, ndigits=3)]])
            else:  # 'isolate' has been processed
                if baseline == 0:
                    # Query sequence was found, but not the HKGENES provided
                    # to estimate the baseline coverage--provide more HKGENES.
                    cov_data[isolate].append(list([query, contig,
                                             str('ERR: baseline coverage is zero.')]))
                else:
                    cov_data[isolate].append(list([query, contig,
                                                  round(copy_number / baseline, ndigits=3)]))
    return cov_data
