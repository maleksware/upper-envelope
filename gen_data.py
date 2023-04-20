import random

def gen_random_data(num_lines=100, max_line_length=1000, max_coordinate=10000, file=""):
    min_y = 0
    max_y = max_coordinate

    lines = []

    for _ in range(num_lines):
        line = []
        min_x = 0
        max_x = max_coordinate

        line.append((0, random.randint(min_y, max_y)))

        for i in range(random.randint(2, max_line_length)):
            line.append((random.randint(min_x + 1, max_x - 1), random.randint(min_y, max_y)))

            if line[-1][0] > (max_x / max_line_length) and line[-2][0] > (max_x / max_line_length): break

            min_x = line[-1][0]
            if min_x == max_x - 1: break

        line.append((max_x, random.randint(min_y, max_y)))


        for i in range(len(line)):
            line[i][0] = float(line[i][0])
            line[i][1] = float(line[i][1])

        lines.append(line)

    if file:
        with open(file, "w") as fout:
            print(num_lines, file=fout)
            print(file=fout)

            for line in lines:
                for p in line:
                    print(str(p[0]) + ',' + str(p[1]), file=fout)
                print(file=fout)

    return lines

    