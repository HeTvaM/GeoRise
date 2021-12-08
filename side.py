# import user's libs
from dot import Dot

#>------------SUMMARY----------------<
# This module is the side of the figure. Stores the coordinates of 2 points +
# +the equation of a straight line + its length
# class Side:
# -init
# -get_y
# -get_x
# -get_len
#>------------SUMMARY----------------<

class Side:
    def __init__(self, *dots):
        self.dots = [0]*2
        for i in range(2):
            self.dots[i] = Dot(dots[i])
            self.dots[i] = self.dots[i].get_coords()

        self.x1 = self.dots[0][0]
        self.x2 = self.dots[1][0]
        self.y1 = self.dots[0][1]
        self.y2 = self.dots[1][1]
        self.vector = (self.x2 - self.x1, self.y2-self.y1)

    def get_y(self, x):
        try:
            line = ((self.x2*self.y1 - self.x1*self.y2) + (self.y2-self.y1)*x) / (self.x2 - self.x1)
        except ZeroDivisionError:
            return None
        return round(line, 1)

    def get_x(self, y):
        try:
            line = ((self.x2*self.y1 - self.x1*self.y2) + (self.x1 - self.x2)*y)/ (self.y1 - self.y2)
        except ZeroDivisionError:
            return None
        return round(line, 1)

    def get_len(self):
        len = (self.vector[0] ** 2 + self.vector[1] ** 2) ** (1/2)
        return round(len, 1)
