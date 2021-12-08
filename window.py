# import system libs
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial

# import user's libs
from logger import log_print_cls
from mediator import Mediator
from graph import Plot
from loader import save, upload

#>------------SUMMARY----------------<
# This module creates the application window. This is an interface window
# that allows you to see the process of creating a figure and solving a problem.
# Widgets help you enter coordinates in real time,
# and buttons associate different classes
# class Win:
# -init
# -show
# -show_plot
# -add_dot
# -click
# -save
#>------------SUMMARY----------------<

# init dirs for win
BASEDIR = os.path.abspath(os.path.dirname(__name__))
IMAGEDIR = BASEDIR + "//Image//"
LOGDIR = BASEDIR + "//Log//"
FILEDIR = BASEDIR + "//Save"



class Win():
    def __init__(self, size, mediator, plot):
        self.mediator = mediator
        self.plot = plot

        # Создание окна
        self.win = Tk()
        self.win.title("Geometry")
        self.win.geometry(f"{size[0]}x{size[1]}")
        self.win.resizable(width=False, height=False)
        self.win.focus_set()

        # Иницилизация переменных для работы класса
        self.ent = []
        self.btn = []
        self.dots = []
        self.rigthdot = None

        # Загрузка изображений для тулбара
        self.iSave = ImageTk.PhotoImage(file=IMAGEDIR + "save_icon.png")
        self.iDel = ImageTk.PhotoImage(file=IMAGEDIR + "del_icon.png")
        self.iRes = ImageTk.PhotoImage(file=IMAGEDIR + "return_icon.png")

        # Отображение виджетов
        self.show()

        self.win.mainloop()

    def show(self):
        """Отображает
        Виджеты программы в окне tkinter. Добавляет окно matplotlib, где рисуется график
        в окно tkinter.
        """
        def frame():
            self.toolbar = Frame(self.win, relief=SUNKEN, height=50, width=350, bg="wheat1")
            self.zero = Frame(self.win,relief=FLAT, height=50, width=450, bg="white")
            self.plot_frame = Frame(self.win,relief=FLAT, height=650, width = 800, bg="white")
            self.button_frame = Frame(self.win,bd=5, relief=SUNKEN, height=150, width = 800, bg="white")

            self.toolbar.place(x=0,y=0)
            self.zero.place(x=350,y=0)
            self.plot_frame.place(x=0,y=50)
            self.button_frame.place(x=0,y=700)
        def entry():
            text = ["X", "Y"]
            x, y = 5, 35
            for i in range(2):
                lb = Label(self.button_frame, text = f"Введите {text[i]} координату:", height=3, width = 25, bg="white")
                i = Entry(self.button_frame, text = f"Введите {text[i]} координату:", width=10)
                lb.place(x=x, y=y-15)
                i.place(x=x+155, y=y)
                self.ent.append(i)
                y += 50
            self.ent[0].bind("<Down>", lambda event: self.ent[1].focus())
            self.ent[1].bind("<Return>", lambda event: self.add_dot())
        def toolbar():
            btnSave = Button(self.toolbar, relief=FLAT,image=self.iSave,bg="wheat1",width=50,height=40, command=self.file_func)
            btnDel = Button(self.toolbar, relief=FLAT,image=self.iDel,bg="wheat1",width=50,height=40, command=remove)
            btnRes = Button(self.toolbar, relief=FLAT,image=self.iRes,bg="wheat1",width=50,height=40, command=reset)
            btnSave.place(x=5,y=3)
            btnDel.place(x=55,y=3)
            btnRes.place(x=105, y=3)
        def btn():
            text = ["Добавить", "Рассчитать"]
            command = [self.add_dot, self.click]
            color = ["green","cyan"]
            x = 405
            for i in range(2):
                i = Button(self.button_frame, text = text[i], height = 5, width = 22, command = command[i], bg=color[i])
                i.place(x=x, y=35)
                self.btn.append(i)
                x += 200
        def bind():
            self.win.bind("<Escape>", lambda event: reset())
            self.win.bind("<Return>", lambda event: self.ent[0].focus())
        def reset():
            fig = self.plot.laststep()
            self.show_plot(figure=fig)
            self.rigthdot = None
        def remove():
            self.plot._del()
            self.show_plot()

        def init():
            frame()
            entry()
            toolbar()
            btn()
            bind()
            self.show_plot()

        init()

    def show_plot(self, figure = None, key=False):
        """Отображает
        Виджет matplotlib с декартовой системой координат
        """
        if self.plot.key is False:
            self.plot.init_graph()
            figure = self.plot.init_display()
        self.canvas=FigureCanvasTkAgg(figure,self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=0,y=-50)
        self.canvas._tkcanvas.place(x=0,y=-50)

    def add_dot(self):
        """Добавлеяет
        Точку в данные + отображает её на графике
        """
        dot = []
        for num, ent in enumerate(self.ent):
            if ent.get() == "":
                showerror("Ошибка!", "Введите значение в поле")
                return ["Error"]
            else:
                dot.append(float(ent.get()))
                ent.delete(0, END)

        self.dots.append(tuple(dot))
        fig = self.plot.show_dot(dot)
        self.show_plot(fig)


    def click(self):
        """Запускает
        Проверку решения. Если пользователь указал многоугольник, тогда проверяет какой это многоугольник.
        Если невыпуклый, то находит точки, прямой, которая разделяет многоугольник на выпуклые и отображает
        её на оси.
        """
        def more_dot():
            if self.ent[0].get != "":
                self.add_dot()
                self.click()
            else:
                showerror("Минимум 3 точки!", f"Чтобы получить многоугольник нужно от 3х точек.\nУ вас: {len(self.dots)}")
                return
        def solve():
            res = self.mediator.start(self.dots)
            for i in range(len(self.dots)):
                self.dots.pop()
            check_res(res)
        def check_res(res):
            if res is None:
                showinfo("Выпуклый!","Данный многоугольник является выпуклым!\nПопробуйте добавить точку")
            else:
                self.rigthdot = res[-1]
                fig = self.plot.solve_task(res)
                self.show_plot(fig)


        if len(self.dots) < 3:
            more_dot()
        else:
            solve()

    def file_func(self):
        if self.rigthdot is None:
            self.open()
        else:
            self.save()


    def save(self):
        """Сохраняет
        Файл. Данные содержат, точки фигуры и точку, которую нашла программа.
        """
        try:
            data = {"Figure": [dots for side in self.mediator.sides for dots in side.dots],
                    "Dot": [(self.rigthdot)]}
        except AttributeError:
            showinfo("Невозможно!", "Нельзя сохранить пустой файл, необходимо построить фигуру!")
            return

        path = asksaveasfile(initialdir=FILEDIR, title="Select file", filetypes=(("txt files", "*.txt"),("all files", "*.*")))
        if path is not None:
            save(path.name, data)
        else:
            return

    def open(self):
        """Открывает
        Файл и выводит фигуру забитую в текстовом формате
        """
        path = askopenfile(initialdir=FILEDIR, title="Select file", filetypes=(("txt files", "*.txt"),("all files", "*.*")))
        if path is not None:
            data = upload(path.name)
            print(data)
            for dots in data["Figure"]:
                self.dots.append(tuple(dots))
                fig = self.plot.show_dot(dots)
                self.show_plot(fig)
        else:
            return




if __name__=="__main__":
    size = [800, 850]
    mediator = Mediator()
    plot = Plot()
    win = Win(size, mediator, plot)
