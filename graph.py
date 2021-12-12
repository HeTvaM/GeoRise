# import system libs
import numpy as np
import matplotlib.pyplot as plt

# import user's libs
from decor import scale

#>------------SUMMARY----------------<
# This module is intended for displaying a Cartesian coordinate system. Dots and lines on it.
# class Plot:
# -init
# -init_graph
# -init_display
# -show_graph
# -show_dot
# -solve_task
# -laststep
# -scale_in
# -scale_out
# -reinit
# -_del
#>------------SUMMARY----------------<


class Plot:
    def __init__(self):
        self.key = False
        self.dots = []
        self.data = {"X": [],
                     "Y": []}
        self.lastline = {"X":[],
                         "Y":[]}
        self.border = [(-5, 6), (6, -5)]
        self.step = 1.0

    def init_graph(self):
        "Создание декартовой сетки"
        self.key = True
        self.plot = plt.plot()
        self.figure = plt.figure(figsize=(11, 10), dpi=75)
        self.ax = plt.subplot(111)
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.yaxis.set_ticks_position('left')
        self.ax.spines['left'].set_position(('data', 0))

    def show_graph(self, dots):
        "Размеры сетки и отображение координатных полос"
        def tick_x(max, min):
            mas = np.arange(min, max, self.step)
            plt.xlim(min, max)
            plt.xticks(mas, [str(i) for i in mas])

        def tick_y(max, min):
            mas = np.arange(min, max, self.step)
            plt.ylim(min, max)
            plt.yticks(mas, [str(i) for i in mas])

        x = np.array([dot[0] for dot in dots])
        y = np.array([dot[1] for dot in dots])

        tick_x(x.max()*1.0, x.min()*1.0)
        tick_y(y.max()*1.0, x.min()*1.0)

    def init_display(self):
        "Создание объёекта сетки"
        self.show_graph(self.border)
        return self.figure

    def show_dot(self, dot):
        "Отображение точки на сетке + рисование линий при условии что точек > 3"
        def analyse_dot(dot):
            "Анализ границ декартовой сетки. Если какая-то точка находиться за пределами, то пределы меняются"
            for num, Oi in enumerate(dot):
                if abs(Oi) > (abs(self.border[0][num]) or abs(self.border[1][num])):
                    self.border = [(-Oi, Oi+1), (Oi+1, -Oi)]
                    self.step = Oi/10
                    self.redraw()
                    return
        def new_line():
            self.data["X"].append([dot[0] for dot in self.dots[size-2:]])
            self.data["Y"].append([dot[1] for dot in self.dots[size-2:]])
            self.ax.plot(self.data["X"][ls], self.data["Y"][ls], color="b", label=f"Side №:{ls+1}")

        self.dots.append(dot)
        analyse_dot(dot)
        self.ax.scatter(dot[0],dot[1])
        size = len(self.dots)
        ls = len(self.data["X"])

        if size > 1:
            new_line()
        if size > 2:
            if self.lastline["X"] is not None:
                self.redraw()

        self.ax.legend(loc='upper left', frameon=False)
        return self.figure

    def solve_task(self, dots):
        "Отображение линии, которая разделяет невыклый многоугольник на выпуклые. Отображается красным светом"
        self.ax.scatter(dots[-1][0], dots[-1][1])

        self.ax.plot([dot[0] for dot in dots],[dot[1] for dot in dots], color="r", label="Line")
        self.ax.legend(loc='upper left', frameon=False)
        return self.figure

    def laststep(self):
        "Откатывает сетку, к предыдущему вводу точки"
        def reinit():
            try:
                self.dots.pop()
                self.data["X"].pop()
                self.data["Y"].pop()
            except IndexError:
                return self.figure

            self.redraw()

        reinit()
        return self.figure

    @scale
    def scale_in(self, size):
        "Увеличение масштаба декартовой сетки"
        self.step = (size*2)/10
        return [(-size*2, size*2+1), (size*2+1, -size*2)]

    @scale
    def scale_out(self, size):
        "Уменьшение масштаба декартовой сетки"
        self.step = (size/2)/10
        return [(-size/2, size/2+1), (size/2+1, -size/2)]

    def redraw(self):
        "Перерисовка декартовой сетки"
        self.ax.clear()
        self.init_graph()
        self.show_graph(self.border)
        ls = len(self.data["X"])

        for dot in self.dots:
            self.ax.scatter(dot[0],dot[1])

        for i in range(len(self.data["X"])):
            self.ax.plot(self.data["X"][i], self.data["Y"][i], color="b", label=f"Side №:{i+1}")

        self.lastline["X"] = [dot[0] for dot in [self.dots[0], self.dots[-1]]]
        self.lastline["Y"] = [dot[1] for dot in [self.dots[0], self.dots[-1]]]
        self.ax.plot(self.lastline["X"],self.lastline["Y"], color="b",label=f"Side №:{ls+1}")

        return self.figure

    def _del(self):
        "Очищает сетку и данные отображенные на ней"
        self.ax.clear()
        self.key = False
        self.dots = []
        self.data = {"X": [],
                     "Y": []}
        self.lastline = {"X":[],
                         "Y":[]}
