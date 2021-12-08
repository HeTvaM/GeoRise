#>------------SUMMARY----------------<
# This module is a point. Allows you to store, receive and
# indicate coordinates along the Ox and Oy axes
# class Dot:
# -init
# get_coords
# set_coords
#>------------SUMMARY----------------<

class Dot:
    def __init__(self, coord):
        self.x, self.y = coord[0], coord[1]

    def get_coords(self):
        return (self.x, self.y)

    def set_coords(self, x, y):
        self.x = x
        self.y = y
