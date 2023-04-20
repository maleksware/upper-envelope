inf = 1e9
eps = 1e-6

class Point:
    def __init__(self, x, y, next_point=-1):
        self.x = x
        self.y = y
        self.next_point = next_point
    
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.next_point})"

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(v, u):
        return v.x * u.x + v.y * u.y

    def __mod__(v, u):
        return v.x * u.y - v.y * u.x

def vbp(a, b):
    return Vector(b.x - a.x, b.y - a.y)

class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def contains(self, p):
        return abs(self.a * p.x + self.b * p.y + self.c) <= eps


def intersect_lines(n, m):
    x = (n.b * m.c - n.c * m.b) / (n.a * m.b - n.b * m.a)
    y = -(n.a * m.c - n.c * m.a) / (n.a * m.b - n.b * m.a)
    return Point(x, y)

def lbp(n, m):
    a = m.y - n.y
    b = n.x - m.x
    c = -a * n.x - b * n.y
    return Line(a, b, c)

class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def lbs(s):
    return lbp(s.a, s.b)

def intersect_segments(a, b):
    return intersect_lines(lbs(a), lbs(b))


def find_intersection(a, b, line_x):
    return intersect_lines(lbp(a, b), lbp(Point(line_x, 0.0), Point(line_x, 1.0)))

def eq(a, b):
    return abs(a - b) <= eps

def merge(a, b): # this implementation is for local use only; don't use it in merge sort!
    result = list()

    while a and b:
        if not a:
            result.append(b.pop())
        elif not b:
            result.append(a.pop())
        else:
            if a[-1] < b[-1]:
                result.append(b.pop())
            elif a[-1] > b[-1]:
                result.append(a.pop())
            else:
                result.append(a.pop())
                b.pop()
        
    return result[::-1]

def get_ue2(first_line, second_line):
    # 1. Prepare all turning points for interpolation

    first_turning_points_x = list()
    second_turning_points_x = list()

    for point in first_line:
        first_turning_points_x.append(point.x)

    for point in second_line:
        second_turning_points_x.append(point.x)
    
    x_coords = merge(first_turning_points_x, second_turning_points_x)


    # 2. Create a treap-inspired list to store the segments without worrying about the actual order of points (using links)
    
    all_points = list()

    for index, point in enumerate(first_line[:-1]):
        point.next_point = index + 1
        all_points.append(point)
    all_points.append(first_line[-1])

    for index, point in enumerate(second_line[:-1]):
        point.next_point = len(first_line) + index + 1
        all_points.append(point)
    all_points.append(second_line[-1])


    # 3. Interpolation calculation in all turning points (computing intersections)

    p1 = 0
    p2 = len(first_line)
    c = 0

    while all_points[p1].next_point != -1 and all_points[p2].next_point != -1:
        if not eq(all_points[all_points[p2].next_point].x, x_coords[c + 1]):
            intersection = find_intersection(all_points[p2], all_points[all_points[p2].next_point], x_coords[c + 1])
            intersection.next_point = all_points[p2].next_point
            all_points[p2].next_point = len(all_points)
            all_points.append(intersection)
        elif not eq(all_points[all_points[p1].next_point].x, x_coords[c + 1]):
            intersection = find_intersection(all_points[p1], all_points[all_points[p1].next_point], x_coords[c + 1])
            intersection.next_point = all_points[p1].next_point
            all_points[p1].next_point = len(all_points)
            all_points.append(intersection)

        p1 = all_points[p1].next_point
        p2 = all_points[p2].next_point
        c += 1

    
    # 4. Calculating segment intersections to form a raw non-optimised envelope

    raw_env = list()

    p1 = 0
    p2 = len(first_line)

    while all_points[p1].next_point != -1 and all_points[p2].next_point != -1:
        if all_points[p1].y < all_points[p2].y:
            # swap the pointers to fix the invariant
            _tmp = p1
            p1 = p2
            p2 = _tmp

        if all_points[all_points[p1].next_point].y > all_points[all_points[p2].next_point].y:
            raw_env.append(all_points[p1])
        else:
            raw_env.append(all_points[p1])
            raw_env.append(intersect_segments(Segment(all_points[p1], all_points[all_points[p1].next_point]),
                                              Segment(all_points[p2], all_points[all_points[p2].next_point])))

        p1 = all_points[p1].next_point
        p2 = all_points[p2].next_point
                                            
    # add the last point as it's not processed in the loop
    if all_points[p1].y > all_points[p2].y:
        raw_env.append(all_points[p1])
    else:
        raw_env.append(all_points[p2])

    
    # 5. Clear all points on the segments to optimise performance when scaling

    clear_env = raw_env[:2]

    for point in raw_env[2:]:
        if lbp(clear_env[-2], clear_env[-1]).contains(point):
            clear_env.pop()
        clear_env.append(point)

    return clear_env

def get_ue(lines):
    # validating data
    if len(lines) <= 1:
        return lines

    # getting the resulting envelope iteratively
    result = get_ue2(lines[0], lines[1])

    for line in lines[2:]:
        result = get_ue2(result, line)

    return result
