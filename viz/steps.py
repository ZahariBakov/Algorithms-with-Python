from dataclasses import dataclass

COMPARE = 'compare'
SWAP = 'swap'
WRITE = 'write'
DONE = 'done'
RANGE = 'range'
NOT_FOUND = 'not_found'
CELL = 'cell'
PATH = 'path'
VISIT = 'visit'
FOUND = 'found'


@dataclass
class Step:
    """One small moment of an algorithm.

    kind: COMPARE, SWAP, WRITE, DONE, RANGE or NOT_FOUND.
    WRITE means one value was put into one position (used by merge sort).
    RANGE is used by searching: indices are (left, mid, right).
    NOT_FOUND is the last step of a search that did not find the target.
    indices: the positions that this step is about.
    data: a copy of the list at this moment.
    info: extra data for table algorithms (None for the others).
    CELL: indices is (row, col), info is the tuple of cells it reads from.
    PATH: info is the tuple of path cells found so far.
    DONE (table): info is the answer.
    Graphs: data is a copy of the visited nodes (in order), info is a copy
    of the queue.
    VISIT: indices is (node,), the node taken from the queue.
    FOUND: indices is (node,), a neighbor that was just put in the queue.
    DONE (graph): info is the BFS order.
    For tables, data is a copy of the table (every row is copied too).
    """
    kind: str
    indices: tuple
    data: list
    info: object = None
