import random

n = 100
max_line_length = 50

min_y = 0
max_y = 10000

lines = []

for _ in range(n):
    line = []
    min_x = 0
    max_x = 10000

    line.append((0, random.randint(min_y, max_y)))

    for i in range(random.randint(2, max_line_length)):
        line.append((random.randint(min_x + 1, max_x - 1), random.randint(min_y, max_y)))

        if line[-1][0] > (max_x / max_line_length) and line[-2][0] > (max_x / max_line_length): break

        min_x = line[-1][0]
        if min_x == max_x - 1: break

    line.append((max_x, random.randint(min_y, max_y)))

    lines.append(line)


with open("data/lines.txt", "w") as fout:
    print(n, file=fout)
    print(file=fout)

    for line in lines:
        for p in line:
            print(str(p[0]) + ',' + str(p[1]), file=fout)
        print(file=fout)

    