from viz.steps import DONE, NOT_FOUND, RANGE, Step


def binary_search(data, target):
    """Yield a RANGE step (left, mid, right) for each round.

    The last step is DONE with (index,) when the target is found,
    or NOT_FOUND with () when it is not. data must be sorted.
    """
    items = list(data)
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        yield Step(RANGE, (left, mid, right), list(items))
        if items[mid] == target:
            yield Step(DONE, (mid,), list(items))
            return
        if items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    yield Step(NOT_FOUND, (), list(items))


def result_index(steps):
    """The found index from a list of steps, or -1 when not found."""
    last = steps[-1]
    if last.kind == DONE:
        return last.indices[0]
    return -1
