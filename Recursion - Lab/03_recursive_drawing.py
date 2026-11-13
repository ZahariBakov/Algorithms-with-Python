def draw_figure(num, lines):
    if num == 0:
        return

    lines.append('*' * num)

    draw_figure(num - 1, lines)
    lines.append('#' * num)


def get_figure(num):
    lines = []
    draw_figure(num, lines)
    return lines


def main():
    num = int(input())

    for line in get_figure(num):
        print(line)


if __name__ == '__main__':
    main()
