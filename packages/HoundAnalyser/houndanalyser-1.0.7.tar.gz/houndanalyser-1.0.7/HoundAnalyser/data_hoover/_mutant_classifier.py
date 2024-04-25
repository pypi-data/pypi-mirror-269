from Bio import Seq


def _curate_mutations(MUT_LOCATIONS: list, SEQ: Seq, CDS: str = None,
                      MUT_ROI: list = None) -> list:
    """
        Check if mutations are in consecutive locations, and therefore
        whether they belong to a truncated sequence, and filter.
    """
    # TODO: better locate mutations when theres lots of Xs
    NON_TRUNCATED_MUTATIONS = list()
    if CDS is not None:
        assert MUT_ROI is not None  # Assert some reference regions are given

        if isinstance(MUT_ROI[0], list) is True:
            for ROI in MUT_ROI:
                NON_TRUNCATED_MUTATIONS.extend([mut for mut in MUT_LOCATIONS
                                                if mut in range(ROI[0],
                                                                ROI[1] + 1)])
        else:
            NON_TRUNCATED_MUTATIONS.extend([mut for mut in MUT_LOCATIONS
                                            if mut in range(MUT_ROI[0],
                                                            MUT_ROI[1] + 1)])

        if len(NON_TRUNCATED_MUTATIONS) == 0:
            NON_TRUNCATED_MUTATIONS = None
        return NON_TRUNCATED_MUTATIONS
    elif len(MUT_LOCATIONS) < 2:
        NON_TRUNCATED_MUTATIONS = MUT_LOCATIONS
    else:
        X_INIT = SEQ.translate().seq.find('X')
        X_END = SEQ.translate().seq.rfind('X')
        NON_TRUNCATED_MUTATIONS = [mut for mut in MUT_LOCATIONS
                                   if mut not in range(X_INIT, X_END + 1)]
        # Only mutations found because of the Xs?
        if len(NON_TRUNCATED_MUTATIONS) == 0:
            NON_TRUNCATED_MUTATIONS = None
    return NON_TRUNCATED_MUTATIONS


def _find_mutation_type(SEQ: Seq, REFERENCE_SEQ: Seq, MUT_LOCATION: int,
                        CDS: str = None):
    """
        Find whether a given mutations is synonymous or non-synonymous.
    """
    if CDS is None:
        # Case of AA sequence
        return REFERENCE_SEQ[MUT_LOCATION] + str(' -> ') + SEQ[MUT_LOCATION]
    else:
        # Case of NT sequence TODO: why same NT would come out as a mutation??
        # Only happens in 232450_HAW1BAM1
        if REFERENCE_SEQ[MUT_LOCATION] != SEQ[MUT_LOCATION]:
            return REFERENCE_SEQ[MUT_LOCATION] + str(' -> ') + SEQ[MUT_LOCATION]
        else:
            return None


def _is_truncated(SEQ: Seq, REFERENCE_SEQ: Seq) -> float:
    """
        Align a sequence against a reference sequence to measure the number
        of gaps ('-') at the beginning of the alignment. If they exist, then
        SEQ is truncated.
    """
    if REFERENCE_SEQ.count('-') == 0 and SEQ.seq.count('-') > 0:
        TRUNCATED = len(SEQ.seq.lstrip('-')) / len(REFERENCE_SEQ)
    else:
        TRUNCATED = False
    return TRUNCATED


def _are_insertions(SEQ: Seq, REFERENCE_SEQ: Seq) -> float:
    """
        Align a sequence against a reference sequence to measure the number
        of gaps ('-') in the reference. If they exist, then there is an
        insertion in SEQ.
    """
    if SEQ.count('-') == 0 and REFERENCE_SEQ.count('-') > 0:
        INSERTION = REFERENCE_SEQ.count('-')
    else:
        INSERTION = False
    return INSERTION
