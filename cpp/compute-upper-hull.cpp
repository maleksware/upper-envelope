#include <bits/stdc++.h>
#define endl "\n"

#pragma GCC optimize("O3,unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")

using namespace std;
using ll = long long;
using ld = long double;

ll inf = 1e9;
const ld eps = 10e-6;

struct Point {
  ld x;
  ld y;

  ll next_point = -1;

  ld angle() {
    return atan(y / x);
  }
};


struct Vector {
    ld x, y;
};


ld operator*(const Vector& v, const Vector& u) {
    return v.x * u.x + v.y * u.y;
}


ld operator%(const Vector& a, const Vector& b) {
  return a.x * b.y - a.y * b.x;
}


Vector vbp(Point a, Point b) {
  return Vector{b.x - a.x, b.y - a.y};
}


struct Line {
  ld a, b, c;
};


bool contains(Line l, Point p) {
  return abs(l.a * p.x + l.b * p.y + l.c) <= eps;
}


Point intersect_lines(Line n, Line m) {
  ld y = -(n.a * m.c - n.c * m.a) / (n.a * m.b - n.b * m.a);
  ld x = (n.b * m.c - n.c * m.b) / (n.a * m.b - n.b * m.a);
  return Point{x, y};
}


Line line_by_points(Point n, Point m) {
  ld a = m.y - n.y;
  ld b = n.x - m.x;
  ld c = -a * n.x - b * n.y;
  return Line{a, b, c};
}


struct Segment {
  Point a, b;
};


Line line_by_segment(Segment s) {
  return line_by_points(s.a, s.b);
}


Point intersect_segments(Segment a, Segment b) {
  return intersect_lines(line_by_segment(a), line_by_segment(b));
}


bool eq(ld a, ld b) {
  return (abs(a - b) < eps);
}


vector<ld> merge(vector<ld>& a, vector<ld>& b) {
  vector<ld> result;
  while (!a.empty() || !b.empty()) {
    if (b.empty()) {
      result.push_back(a.back());
      a.pop_back();
    } else if (a.empty()) {
      result.push_back(b.back());
      b.pop_back();
    } else {
      if (a.back() < b.back()) {
        result.push_back(b.back());
        b.pop_back();
      } else {
        result.push_back(a.back());
        a.pop_back();
      }
    }
  }
  reverse(result.begin(), result.end());

  vector<ld> new_result;
  new_result.push_back(result[0]);
  
  for (int i = 1; i < result.size(); i++) {
    if (eq(result[i], new_result.back())) continue;
    new_result.push_back(result[i]);
  }
  
  return new_result;
}


Point find_intersection(Point a, Point b, ld line_x) {
  return intersect_lines(line_by_points(a, b), line_by_points(Point{line_x, 0}, Point{line_x, 1}));
}


vector<Point> get_upper_hull_of_2_lines(vector<Point> first_initial_line, vector<Point> second_initial_line) {
  // 1. Запомнить координаты ключевых для нас точек

  vector<ld> coords;
  vector<ld> line_1, line_2;

  for (int i = 0; i < first_initial_line.size(); i++) {
    line_1.push_back(first_initial_line[i].x);
  }

  for (int i = 0; i < second_initial_line.size(); i++) {
    line_2.push_back(second_initial_line[i].x);
  }

  coords = merge(line_1, line_2); // получили отсортированный массив x-координат всех точек обеих ломаных (ключевые точки)

  // 2. Пройти по отрезкам и представить их в виде точек (выгодно хранить отрезки в виде точек с индексом на следующую точку)

  vector<Point> all_points;

  for (int i = 0; i < first_initial_line.size(); i++) {
    if (i < first_initial_line.size() - 1) {
      first_initial_line[i].next_point = i + 1; // массив пока пустой, заполняем его от начала по индексам i
      all_points.push_back(first_initial_line[i]);
    } else {
      all_points.push_back(first_initial_line[i]); // у последней точки ссылка -1
    }
  }

  for (int i = 0; i < second_initial_line.size(); i++) {
    if (i < second_initial_line.size() - 1) {
      second_initial_line[i].next_point = first_initial_line.size() + i + 1; // учитывая, что массив уже хранит первую линию
      all_points.push_back(second_initial_line[i]);
    } else {
      all_points.push_back(second_initial_line[i]); // у последней точки ссылка -1 - значение по умолчанию в структуре
    }
  }


  // 3. Сложная часть - деление отрезков в местах перегибов другой ломаной

  /*
    У нас есть текущие отрезки и указатель на текущую точку в векторе all_points.
    Считаем все за один проход - если отрезок пересекает вертикальную прямую, проходящую через точку на указателе, добавляем в конец all_points точку пересечения и обновляем индексы (важно!)
    [IGNORE] Самый важный момент: надо запомнить общее число точек в all_points, ведь длина массива будет расти, а в for-e будет динамически пересчитываться условие выхода из цикла.
    Самый важный момент можно игнорировать, ведь условие - отсутствие перехода в текущей точке [p1], а p1 и p2 всегда равны.
  */

  ll p1 = 0;
  ll p2 = first_initial_line.size();
  ll c = 0;


  while (all_points[p1].next_point != -1 && all_points[p2].next_point != -1) {
    // cout << p1 << " " << p2 << " " << c << endl;
  
    if (all_points[all_points[p2].next_point].x != coords[c + 1]) {
      Point intersection = find_intersection(all_points[p2], all_points[all_points[p2].next_point], coords[c + 1]);
      intersection.next_point = all_points[p2].next_point;
      all_points[p2].next_point = all_points.size(); // после добавления индекс будет правильный
      all_points.push_back(intersection);
    } else if (all_points[all_points[p1].next_point].x != coords[c + 1]) {
      Point intersection = find_intersection(all_points[p1], all_points[all_points[p1].next_point], coords[c + 1]);
      intersection.next_point = all_points[p1].next_point;
      all_points[p1].next_point = all_points.size(); // после добавления индекс будет правильный
      all_points.push_back(intersection);
    }

    p1 = all_points[p1].next_point;
    p2 = all_points[p2].next_point;
    c++;
  }

  // 4. Считаем пересечения отрезочков))) наконец-то получаем какой-никакой ответ.

  vector<Point> raw_env;

  p1 = 0;
  p2 = first_initial_line.size();

  while (all_points[p1].next_point != -1 && all_points[p2].next_point != -1) {
    // cout << p1 << " " << p2 << endl;
    // Найдем самую высокую точку:
    if (all_points[p1].y < all_points[p2].y) {
      swap(p1, p2);
    }
    // Теперь инвариант - p1.y > p2.y

    if (all_points[all_points[p1].next_point].y > all_points[all_points[p2].next_point].y) {
      raw_env.push_back(all_points[p1]);
    } else {
      raw_env.push_back(all_points[p1]);
      raw_env.push_back(intersect_segments(Segment{all_points[p1], all_points[all_points[p1].next_point]}, Segment{all_points[p2], all_points[all_points[p2].next_point]}));
    }

    p1 = all_points[p1].next_point;
    p2 = all_points[p2].next_point;
  }


  // добавляем последнюю точку, потому что она не обрабатывается в цикле
  if (all_points[p1].y > all_points[p2].y) {
    raw_env.push_back(all_points[p1]);
  } else {
    raw_env.push_back(all_points[p2]);
  }

  // 5. Зачистить точки, лежащие на одной прямой (оптимизация для случайных выборок)

  vector<Point> env;

  env.push_back(raw_env[0]);
  env.push_back(raw_env[1]);

  for (int i = 2; i < raw_env.size(); i++) {
    Point p_a = env[env.size() - 2];
    Point p_b = env[env.size() - 1];
    Point p_c = raw_env[i];

    if (contains(line_by_points(p_a, p_c), p_b)) {
      env.pop_back();
    }

    env.push_back(p_c);
  }

  return env;
}

vector<Point> get_upper_hull(vector<vector<Point>> lines) {
  vector<Point> result = get_upper_hull_of_2_lines(lines[0], lines[1]);

  for (int i = 2; i < lines.size(); i++) {
    result = get_upper_hull_of_2_lines(result, lines[i]);
  }

  return result;
}


int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  freopen("data/lines.txt", "r", stdin);

  string s;

  getline(cin, s);
  const ll NUMBER_OF_LINES = stoll(s);
  getline(cin, s); // read newline after the number of lines

  vector<vector<Point>> lines;
  lines.resize(NUMBER_OF_LINES);

  for (int cur_line_number = 0; cur_line_number < NUMBER_OF_LINES; cur_line_number++) {
    getline(cin, s);

    while (s.size() > 2) {
      string x;
      string y;

      bool read_x = true;

      for (char c : s) {
        if (c == ',') {
          read_x = false;
          continue;
        }

        if (read_x) {
          x += c;
        } else {
          y += c;
        }
      }

      lines[cur_line_number].push_back(Point{stold(x), stold(y)});
      getline(cin, s);
    }
  }

  vector<Point> result = get_upper_hull(lines);

  ofstream fo;
  fo.open("data/result.txt");
  for (auto p : result) {
    fo << p.x << ',' << p.y << endl;
  }
  fo.close();

  cout << "done." << endl;

  return 0;
}
