def reverse_aray(left_idx, array):
    if left_idx == len(array) // 2:
        return

    right_idx = len(array) - 1 - left_idx
    array[left_idx], array[right_idx] = array[right_idx], array[left_idx]
    reverse_aray(left_idx + 1, elements)

elements = input().split()

reverse_aray(0, elements)

print(' '.join(elements))

