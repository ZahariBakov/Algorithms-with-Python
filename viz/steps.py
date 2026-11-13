from dataclasses import dataclass

COMPARE = 'compare'
SWAP = 'swap'
WRITE = 'write'
DONE = 'done'
RANGE = 'range'
NOT_FOUND = 'not_found'


@dataclass
class Step:
    """One small moment of an algorithm.

    kind: COMPARE, SWAP, WRITE, DONE, RANGE or NOT_FOUND.
    WRITE means one value was put into one position (used by merge sort).
    RANGE is used by searching: indices are (left, mid, right).
    NOT_FOUND is the last step of a search that did not find the target.
    indices: the positions that this step is about.
    data: a copy of the list at this moment.
    """
    kind: str
    indices: tuple
    data: list
