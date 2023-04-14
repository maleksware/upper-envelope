import matplotlib.pyplot as plt

plt.figure(figsize=(5, 4))
plt.title("Lines")



def parse_data_into_points(filename, scan_num=True):
    with open(filename, "r") as fin:
        data = fin.readlines()

        lines = []

        cur_line = list()

        if (scan_num): data = data[2:]

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

def plot_lines(lines, connect=True):
    for line in lines:
        x = []
        y = []

        for point in line:
            x.append(point[0])
            y.append(point[1])

        if connect: plt.plot(x, y)
        plt.scatter(x, y)


lines = parse_data_into_points("data/lines.txt")
pts_res = parse_data_into_points("data/result.txt", scan_num=False)
print(lines)
print(pts_res)

plot_lines(lines)
plot_lines(pts_res)
plt.show()