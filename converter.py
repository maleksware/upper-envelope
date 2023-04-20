# Helper functions to convert between different line representations
from envelope import Point

def coordinates2line(x_s, y_s):
    line = list()

    assert len(x_s) == len(y_s)

    for i in range(len(x_s)):
        line.append(Point(x_s[i], y_s[i]))
    
    return line

def coordlines2lines(coordlines):
    lines = list()
    for x_s, y_s in coordlines:
        lines.append(coordinates2line(x_s, y_s))

    return lines

def tuples2line(tuples):
    line = list()

    for x, y in tuples:
        line.append(Point(x, y))

    return line

def tuplelines2lines(tuplelines):
    lines = list()

    for tupleline in tuplelines:
        lines.append(tuples2line(tupleline))

    return lines

def line2tupleline(line):
    tupleline = list()

    for point in line:
        tupleline.append((point.x, point.y))

    return tupleline

def lines2tuplelines(lines):
    tuplelines = list()

    for line in lines:
        tuplelines.append(line2tupleline(line))

    return tuplelines

def line2coordline(line):
    x_s, y_s = list(), list()

    for point in line:
        x_s.append(point.x)
        y_s.append(point.y)
    
    return (x_s, y_s)

def lines2coordlines(lines):
    coordlines = []

    for line in lines:
        coordlines.append(line2coordline(line))
    
    return coordlines