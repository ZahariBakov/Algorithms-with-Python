def gen01vector(idx, vector):
    if idx >= len(vector):
        print(*vector, sep='')
        return

    for n in range(2):
        vector[idx] = n
        gen01vector(idx + 1, vector)


num = int(input())
vector = [None] * num

gen01vector(0, vector)
