from dataclasses import dataclass

COMPARE = 'compare'
SWAP = 'swap'
DONE = 'done'


@dataclass
class Step:
    """One small moment of an algorithm.

    kind: COMPARE, SWAP or DONE.
    indices: the positions that this step is about.
    data: a copy of the list at this moment.
    """
    kind: str
    indices: tuple
    data: list
