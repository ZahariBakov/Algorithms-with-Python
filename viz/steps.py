from dataclasses import dataclass

COMPARE = 'compare'
SWAP = 'swap'
WRITE = 'write'
DONE = 'done'


@dataclass
class Step:
    """One small moment of an algorithm.

    kind: COMPARE, SWAP, WRITE or DONE.
    WRITE means one value was put into one position (used by merge sort).
    indices: the positions that this step is about.
    data: a copy of the list at this moment.
    """
    kind: str
    indices: tuple
    data: list
