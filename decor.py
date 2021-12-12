# import system libs
import os

#>------------SUMMARY----------------<
# This module contains various decorators that simplify the code in some modules.
# So far there are only 2 decorators - a check for checking a file in a
# directory and a scale for simplifying the code base of two identical functions
# functions:
# -check
# -scale
#>------------SUMMARY----------------<

def check(error):
    def log(func):
        def wrapper(*args, **kwargs):
            file = f"{args[0]}.txt"
            if os.path.isfile(file):
                return error()
            else:
                res = func(*args, **kwargs)

            return res
        return wrapper
    return log

def scale(func):
    def wrapper(*args, **kwargs):
        def check_border():
            border = func(cls, size)
            if border[0][1] < 5:
                return cls.reinit()
            else:
                cls.border = border

            if cls.step < 1:
                cls.step = 1

        cls = args[0]
        size = cls.border[0][1] - 1

        check_border()

        res = cls.draw()

        return res
    return wrapper
