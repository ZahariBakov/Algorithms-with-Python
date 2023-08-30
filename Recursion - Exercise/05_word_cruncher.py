def find_all_solution(idx, target, strings_by_idx, strings_count, used_string):
    if idx >= len(target):
        print(' '.join(used_string))
        return

    if idx not in strings_by_idx:
        return

    for string in strings_by_idx[idx]:
        if strings_count[string] == 0:
            continue

        used_string.append(string)
        strings_count[string] -= 1

        find_all_solution(idx + len(string), target, strings_by_idx, strings_count, used_string)

        used_string.pop()
        strings_count[string] += 1


strings = input().split(", ")
target = input()

strings_by_idx = {}
strings_count = {}

for string in strings:
    if string in strings_count:
        strings_count[string] += 1
        continue

    strings_count[string] = 1

    try:
        idx = 0
        while True:
            idx = target.index(string, idx)

            if idx not in strings_by_idx:
                strings_by_idx[idx] = []

            strings_by_idx[idx].append(string)
            idx += len(string)
    except ValueError:
        pass

find_all_solution(0, target, strings_by_idx, strings_count, [])
