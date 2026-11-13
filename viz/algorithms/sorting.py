from viz.steps import COMPARE, DONE, SWAP, Step


def _step(kind, indices, data):
    # Always send a copy, so later changes do not touch old steps.
    return Step(kind, tuple(indices), list(data))


def bubble_sort(values):
    data = list(values)
    n = len(data)

    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            yield _step(COMPARE, (i, i + 1), data)
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                swapped = True
                yield _step(SWAP, (i, i + 1), data)
        if not swapped:
            break

    yield _step(DONE, range(n), data)


def selection_sort(values):
    data = list(values)
    n = len(data)

    for start in range(n - 1):
        smallest = start
        for i in range(start + 1, n):
            yield _step(COMPARE, (smallest, i), data)
            if data[i] < data[smallest]:
                smallest = i
        if smallest != start:
            data[start], data[smallest] = data[smallest], data[start]
            yield _step(SWAP, (start, smallest), data)

    yield _step(DONE, range(n), data)


def insertion_sort(values):
    data = list(values)
    n = len(data)

    for i in range(1, n):
        j = i
        while j > 0:
            yield _step(COMPARE, (j - 1, j), data)
            if data[j - 1] <= data[j]:
                break
            data[j - 1], data[j] = data[j], data[j - 1]
            yield _step(SWAP, (j - 1, j), data)
            j -= 1

    yield _step(DONE, range(n), data)
