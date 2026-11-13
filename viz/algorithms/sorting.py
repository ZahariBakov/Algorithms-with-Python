from viz.steps import COMPARE, DONE, SWAP, WRITE, Step


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


def _merge(data, low, middle, high):
    left = data[low:middle]
    right = data[middle:high]
    i = j = 0
    k = low

    while i < len(left) and j < len(right):
        yield _step(COMPARE, (low + i, middle + j), data)
        if left[i] <= right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        yield _step(WRITE, (k,), data)
        k += 1

    for value in left[i:] + right[j:]:
        data[k] = value
        yield _step(WRITE, (k,), data)
        k += 1


def _merge_sort_part(data, low, high):
    if high - low < 2:
        return
    middle = (low + high) // 2
    yield from _merge_sort_part(data, low, middle)
    yield from _merge_sort_part(data, middle, high)
    yield from _merge(data, low, middle, high)


def merge_sort(values):
    data = list(values)
    yield from _merge_sort_part(data, 0, len(data))
    yield _step(DONE, range(len(data)), data)


def quick_sort(values):
    data = list(values)
    # An explicit stack of (low, high) ranges, both ends included.
    stack = [(0, len(data) - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        # Lomuto partition with the last item as the pivot.
        pivot = data[high]
        boundary = low
        for i in range(low, high):
            yield _step(COMPARE, (i, high), data)
            if data[i] < pivot:
                if i != boundary:
                    data[i], data[boundary] = data[boundary], data[i]
                    yield _step(SWAP, (i, boundary), data)
                boundary += 1
        if boundary != high:
            data[boundary], data[high] = data[high], data[boundary]
            yield _step(SWAP, (boundary, high), data)
        stack.append((low, boundary - 1))
        stack.append((boundary + 1, high))

    yield _step(DONE, range(len(data)), data)


def _sift_down(data, root, size):
    while True:
        largest = root
        for child in (2 * root + 1, 2 * root + 2):
            if child < size:
                yield _step(COMPARE, (largest, child), data)
                if data[child] > data[largest]:
                    largest = child
        if largest == root:
            return
        data[root], data[largest] = data[largest], data[root]
        yield _step(SWAP, (root, largest), data)
        root = largest


def heap_sort(values):
    data = list(values)
    n = len(data)

    for root in range(n // 2 - 1, -1, -1):
        yield from _sift_down(data, root, n)

    for end in range(n - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        yield _step(SWAP, (0, end), data)
        yield from _sift_down(data, 0, end)

    yield _step(DONE, range(n), data)
