import matplotlib.pyplot as plt
import random # for color generation

def parse_data_into_points(filename, scan_num=True):
    with open(filename, "r") as fin:
        data = fin.readlines()

        lines = []

        cur_line = list()

        if scan_num: data = data[2:]

        for d in data:
            d = d.strip()
            if d == "":
                lines.append(cur_line)
                cur_line = list()
            else:
                d = d.split(",")
                cur_line.append((float(d[0]), float(d[1])))

        if cur_line:
            lines.append(cur_line)

    return lines


def plot_lines(lines):
    for line in lines:
        color = (random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255, 1)

        x = []
        y = []

        for point in line:
            x.append(point[0])
            y.append(point[1])

        plt.plot(x, y, color=color)

def plot_nice_picture(lines, result, line_file="", result_file=""):
    plt.figure(figsize=(5, 4))
    plt.title("Upper envelope")

    if line_file:
        lines = parse_data_into_points(line_file)
    if result_file:
        result = parse_data_into_points(result_file, scan_num=False)[0]

    plot_lines(lines)

    x = []
    y = []

    for point in result:
        try:
            x.append(point.x)
            y.append(point.y)
        except:
            x.append(point[0])
            y.append(point[1])

    plt.plot(x, y, color="red")
    plt.scatter(x, y, color="red")

    plt.show()