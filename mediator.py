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
                if dot in side.dots: continue
                y = side.get_y(dot[0])
                if y is None: continue

                if y >= dot[1]:
                    btnTop += 1
                elif y < dot[1]:
                    btnBot +=1

                if (btnBot and btnTop) > 0:
                    self.find_dot(side)
                    return

    def find_dot(self, side):
        def get_coords(x1,y1,x2,y2,x3,y3,x4,y4):
            try:
                x = ((x4*y3 - x3*y4)*(x2-x1) - (x2*y1-x1*y2)*(x4-x3)) / ( (y2-y1)*(x4-x3) - (y4-y3)*(x2-x1))
                y = ((x4*y3 - x3*y4)*(y1-y2) - (x2*y1-x1*y2)*(y3-y4)) / ( (x1-x2)*(y3-y4) - (x3-x4)*(y1-y2))
            except ZeroDivisionError:
                return None
            return [round(x+0,1), round(y+0,1)]

        self.flag = True
        dots = []
        for dot in side.dots:
            for obj in dot:
                dots.append(obj)

        for line in self.sides:
            if side == line: continue

            for dot in line.dots:
                for obj in dot:
                    dots.append(obj)

            coords = get_coords(*dots)
            for i in range(4):
                dots.pop()

            if coords is not None:
                if tuple(coords) in line.dots: continue

                if line.x1 > line.x2:
                    x1, x2 = line.x1, line.x2
                else:
                    x1, x2 = line.x2, line.x1
                if line.y1 > line.y2:
                    y1, y2 = line.y1, line.y2
                else:
                    y1, y2 = line.y2, line.y1

                x, y = coords[0], coords[1]
                if x1 >= x and x >= x2:
                    if y1 >= y and y >= y2:
                        self.res.append((side.dots[0][0], side.dots[0][1]))
                        self.res.append((side.dots[1][0], side.dots[1][1]))
                        self.res.append((x,y))
                        return

    def get_res(self):
        if len(self.res) == 0:
            return None
        else:
            return self.res
