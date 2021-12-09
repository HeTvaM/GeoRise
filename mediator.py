# import user's libs
from figure import Figure

#>------------SUMMARY----------------<
# This mediator module in which is implemented, the entire logical part of the program.
# It gets the points, the equation of the sides, and looks to see if the polygon is convex or non-convex.
# If 2, then it finds a side and a point inside the figure, drawing a straight line through which,
# we get the union of convex polygons.
# class Mediator:
# -init
# -start
# -solve_task
# -find_dot
# -get_res
#>------------SUMMARY----------------<

class Mediator:
    def __init__(self):
        self.dots = []

    def start(self, dots):
        self.res = []
        figure = Figure(dots)
        self.sides = figure.get_sides()
        self.dots = dots
        self.solve_task()
        return self.res

    def solve_task(self):
        for side in self.sides:
            btnTop, btnBot = 0, 0

            for dot in self.dots:
                # Если рассматриваемая точка явл. частью стороны, то пропускаем
                if dot in side.dots: continue
                y = side.get_y(dot[0])
                # Если это точка параллельной прямой, то пропускаем
                if y is None: continue

                if y >= dot[1]:
                    btnTop += 1
                elif y < dot[1]:
                    btnBot +=1

                if (btnBot and btnTop) > 0:
                    self.find_dot(side)
                    # Нахожу одну сторону
                    # Если убрать return, то будут найдены
                    # Все стороны, относительно которых
                    # Вершины лежат в разных областях
                    return

    def find_dot(self, side):
        def get_coords(x1,y1,x2,y2,x3,y3,x4,y4):
            # Получение точки пересечения 2х прямых
            try:
                x = ((x4*y3 - x3*y4)*(x2-x1) - (x2*y1-x1*y2)*(x4-x3)) / ( (y2-y1)*(x4-x3) - (y4-y3)*(x2-x1))
                y = ((x4*y3 - x3*y4)*(y1-y2) - (x2*y1-x1*y2)*(y3-y4)) / ( (x1-x2)*(y3-y4) - (x3-x4)*(y1-y2))
            except ZeroDivisionError:
                return None
            # python может выдавать -0.0, чтобы сделать 0.0
            # необходимо прибавить 0
            return [round(x+0,1), round(y+0,1)]

        self.flag = True
        # Необходим массив точек найденной стороны
        # И рассматриваемой стоороны, для функции
        # get_coords
        dots = []
        for dot in side.dots:
            for obj in dot:
                dots.append(obj)

        # Для каждой стороны в фигуре
        for line in self.sides:
            # Если рассматриваем найденую сторону то пропускаем
            if side == line: continue

            # Добавляем точки рассматриваемой стороны
            for dot in line.dots:
                for obj in dot:
                    dots.append(obj)

            coords = get_coords(*dots)
            for i in range(4):
                dots.pop()

            # Если не парралельная прямая проверяем принадлежность точки отрезку
            if coords is not None:
                # Возможны случаи, когда координаты будут такие же как вершины
                # Такой случай, необходимо исключать, потому, что
                # В нём нет смысла, это просто вершина, соединяющая 2 стороны
                if tuple(coords) in line.dots: continue

                x1, x2 = line.x1, line.x2
                y1, y2 = line.y1, line.y2

                if x1 < x2:
                    x1, x2 = x2, x1
                if y1 < y2:
                    y1, y2 = y2, y1

                x, y = coords[0], coords[1]
                if x1 >= x and x >= x2:
                    if y1 >= y and y >= y2:
                        # Необходимо вывести 3 точки
                        # Первые 2 это сторона многоугольника
                        # Последняя, найденная точка перечения
                        self.res.append(side.dots[0])
                        self.res.append(side.dots[1])
                        self.res.append((x,y))
                        return

    def get_res(self):
        if len(self.res) == 0:
            return None
        else:
            return self.res
