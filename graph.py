# import system libs
import numpy as np
import matplotlib.pyplot as plt

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

    def init_graph(self):
        "Создание декартовой сетки"
        self.key = True
        self.plot = plt.plot()
        self.figure = plt.figure(figsize=(10, 10), dpi=75)
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
            mas = np.arange(min,max)
            plt.xlim(min, max)
            plt.xticks(mas, [str(i) for i in mas])

        def tick_y(max,min):
            mas = np.arange(min,max)
            plt.ylim(min, max)
            plt.yticks(mas, [str(i) for i in mas])

        x = np.array([dot[0] for dot in dots])
        y = np.array([dot[1] for dot in dots])

        tick_x(x.max()*1.0, x.min()*1.0)
        tick_y(y.max()*1.0, x.min()*1.0)

    def init_display(self):
        "Создание объёекта сетки"
        self.show_graph([(-5, 6), (6,-5)])
        return self.figure

    def show_dot(self, dot):
        "Отображение точки на сетке + рисование линий при условии что точек > 3"
        def last_line():
            "Отрисовка линии, соединяющая последную и первую точку, чтобы можно было визуально представлять фигуру"
            self.lastline["X"] = [dot[0] for dot in [self.dots[0], self.dots[-1]]]
            self.lastline["Y"] = [dot[1] for dot in [self.dots[0], self.dots[-1]]]
            self.ax.plot(self.lastline["X"],self.lastline["Y"], color="b",label=f"Side №:{ls+1}")
        def new_line():
            self.data["X"].append([dot[0] for dot in self.dots[size-2:]])
            self.data["Y"].append([dot[1] for dot in self.dots[size-2:]])
            self.ax.plot(self.data["X"][ls], self.data["Y"][ls], color="b", label=f"Side №:{ls+1}")
        def remove():
            self.ax.clear()
            self.init_graph()
            self.show_graph([(-5, 6), (6,-5)])

            for dot in self.dots:
                self.ax.scatter(dot[0],dot[1])

            for i in range(len(self.data["X"])):
                self.ax.plot(self.data["X"][i], self.data["Y"][i], color="b", label=f"Side №:{i+1}")

        self.dots.append(dot)
        self.ax.scatter(dot[0],dot[1])
        size = len(self.dots)
        ls = len(self.data["X"])

        if size > 1:
            new_line()
        if size > 2:
            if self.lastline["X"] is not None:
                remove()
            last_line()

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
        def remove():
            self.ax.clear()
            self.init_graph()
            self.show_graph([(-5, 6), (6,-5)])
            ls = len(self.data["X"])

            try:
                self.dots.pop()
                self.data["X"].pop()
                self.data["Y"].pop()
            except IndexError:
                return self.figure

            for dot in self.dots:
                self.ax.scatter(dot[0],dot[1])

            for i in range(len(self.data["X"])):
                self.ax.plot(self.data["X"][i], self.data["Y"][i], color="b", label=f"Side №:{i+1}")

            self.lastline["X"] = [dot[0] for dot in [self.dots[0], self.dots[-1]]]
            self.lastline["Y"] = [dot[1] for dot in [self.dots[0], self.dots[-1]]]
            self.ax.plot(self.lastline["X"],self.lastline["Y"], color="b",label=f"Side №:{ls+1}")

        remove()
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
