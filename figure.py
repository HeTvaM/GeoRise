# import user's libs
from side import Side

#>------------SUMMARY----------------<
# This modul is required for working with polygons. Stores information about the sides
# and points of the shape.
# class Figure:
# -init
# -init_sides
# -get_dots
# -get_sides
#>------------SUMMARY----------------<

class Figure:
    def __init__(self, dots):
        if dots is not None:
            self.dots = dots
            self.init_sides()
        else:
            self.key = False

        self.res = []

    def init_sides(self):
        self.sides = []
        size = len(self.dots) - 1
        for i in range(size+1):
            k = 0 if i == size else i+1

            side = Side(self.dots[i], self.dots[k])
            self.sides.append(side)

    def get_dots(self):
        for side in self.sides:
            for dot in side.dots:
                yield dot

    def get_sides(self):
        return self.sides
