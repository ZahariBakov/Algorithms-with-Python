def gen01vector(idx, vector, result):
    if idx >= len(vector):
        result.append(''.join(str(x) for x in vector))
        return

    for n in range(2):
        vector[idx] = n
        gen01vector(idx + 1, vector, result)


def generate_vectors(num):
    result = []
    gen01vector(0, [None] * num, result)
    return result


def main():
    num = int(input())

    for line in generate_vectors(num):
        print(line)


if __name__ == '__main__':
    main()
