def reverse_aray(left_idx, elements):
    if left_idx == len(elements) // 2:
        return

    right_idx = len(elements) - 1 - left_idx
    elements[left_idx], elements[right_idx] = elements[right_idx], elements[left_idx]
    reverse_aray(left_idx + 1, elements)

elements = input().split()

reverse_aray(0, elements)

print(' '.join(elements))

