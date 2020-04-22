from math import pi, cos, sin, sqrt, radians
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import colorchooser
from tkinter import messagebox as mb
from config import Point
import config as cfg
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import tkinter.colorchooser
root = Tk()
root.geometry("1800x900")
root.title("Лабораторная работа №4")
colour = "#000000"
colour_line = ((0.0, 0.0, 0.0), '#000000')
def select_colour():
    global colour, colour_line
    colour = tkinter.colorchooser.askcolor()
    canv.create_rectangle(1500, 130, 1550, 180, fill = colour[1])
    colour_line = colour
    colour = colour[1]

    return colour

def check(event):
    try:
        value = int(entry_for_center_x.get())
        value = int(entry_for_center_y.get())
        value = int(entry_for_radius.get())
        btn_for_make_circle.config(state = "normal")
        btn_for_time_circle.config(state = "normal")
    except:
        btn_for_make_circle.config(state="disabled")
        btn_for_time_circle.config(state="disabled")

    try:
        value = int(entry_for_center_x.get())
        value = int(entry_for_center_y.get())
        value = int(entry_for_start_radius.get())
        value = int(entry_for_count_circles.get())
        btn_for_make_more_circles.config(state = "normal")
    except:
        btn_for_make_more_circles.config(state="disabled")


    try:
        value = int(entry_for_center_x_ellips.get())
        value = int(entry_for_center_y_ellips.get())
        value = int(entry_for_ellips_a.get())
        value = int(entry_for_ellips_b.get())
        btn_for_make_ellips.config(state = "normal")
    except:
        btn_for_make_ellips.config(state="disabled")

    try:
        value = int(entry_for_center_x_ellips.get())
        value = int(entry_for_center_y_ellips.get())
        value = int(entry_for_ellips_start_a.get())
        value = int(entry_for_ellips_start_b.get())
        value = int(entry_for_ellips_step.get())
        value = int(entry_for_ellips_count.get())
        btn_for_make_more_ellips.config(state = "normal")
    except:
        btn_for_make_more_ellips.config(state="disabled")


root.bind("<Key>",check)

def library_make_circle(x, y, r):
    global colour, colour_line
    canv.create_oval(x - r, y - r, x + r, y + r, outline = colour)


def dup_x(points, x, y):
    points += list(map(lambda p: Point(p.x, 2 * y - p.y, p.colour), points))

def dup_y(points, x, y):
    points += list(map(lambda p: Point(2 * x - p.x, p.y, p.colour), points))

def dup_biss(points, x, y):
    points += list(map(lambda p: Point(x + p.y - y, y + p.x - x, p.colour), points))


def brezenham_c(xc, yc, r, colour):
    points = list()

    x = 0
    y = r
    points.append(Point(x + xc, y + yc, colour))
    delta = 2 - r - r

    while x < y:
        if delta <= 0:
            d1 = delta + delta + y + y - 1
            x += 1
            if d1 >= 0:
                y -= 1
                delta += 2 * (x - y + 1)
            else:
                delta += x + x + 1

        else:
            d2 = 2 * (delta - x) - 1
            y -= 1
            if d2 < 0:
                x += 1
                delta += 2 * (x - y + 1)
            else:
                delta -= y + y - 1

        points.append(Point(x + xc, y + yc, colour))

    dup_biss(points, xc, yc)
    dup_x(points, xc, yc)
    dup_y(points, xc, yc)

    return points

def draw_figure(figure):
    for p in figure:
        draw_pixel(p)

def draw_pixel(p: Point):
    canv.create_line(p.x, p.y, p.x + 1, p.y + 1, fill=p.colour)

def normal_c(x, y, r):
    global colour, colour_line
    points = list()
    R = r * r
    for a in range(x, round(x + r / sqrt(2)) + 1):
        b = y + sqrt(R - (a - x) * (a - x))
        points.append(Point(a, b, colour))

    dup_biss(points, x, y)
    dup_x(points, x, y)
    dup_y(points, x, y)

    draw_figure(points)

    return points



def param_c(x, y, r):
    global colour
    points = list()
    step = 1 / r
    for t in np.arange(0, pi / 4 + step, step):
        a = x + r * cos(t)
        b = y + r * sin(t)
        points.append(Point(a, b, colour))

    dup_biss(points, x, y)
    dup_x(points, x, y)
    dup_y(points, x, y)

    draw_figure(points)

    return points


def brezenham_c(xc, yc, r):
    global colour
    points = list()

    x = 0
    y = r
    points.append(Point(x + xc, y + yc, colour))
    delta = 2 - r - r

    while x < y:
        if delta <= 0:
            d1 = delta + delta + y + y - 1
            x += 1
            if d1 >= 0:
                y -= 1
                delta += 2 * (x - y + 1)
            else:
                delta += x + x + 1

        else:
            d2 = 2 * (delta - x) - 1
            y -= 1
            if d2 < 0:
                x += 1
                delta += 2 * (x - y + 1)
            else:
                delta -= y + y - 1

        points.append(Point(x + xc, y + yc, colour))

    dup_biss(points, xc, yc)
    dup_x(points, xc, yc)
    dup_y(points, xc, yc)

    draw_figure(points)
    return points

def middle_point_c(xc, yc, r):
    global colour
    points = list()
    x = r
    y = 0

    points.append(Point(xc + x, yc + y, colour))
    p = 1 - r

    while x > y:
        y += 1

        if p >= 0:
            x -= 1
            p -= x + x

        p += y + y + 1

        points.append(Point(xc + x, yc + y, colour))

    dup_biss(points, xc, yc)
    dup_x(points, xc, yc)
    dup_y(points, xc, yc)
    draw_figure(points)
    return points



def make_circle():
    try:
        choice_algoritm = combo_choose_algoritm.get()
        x = int(entry_for_center_x.get())
        y = int(entry_for_center_y.get())
        radius = int(entry_for_radius.get())

    except:
        mb.showinfo("Ошибка", "Введите корректные значения для центра окружности и радиуса")
        return

    if choice_algoritm == "Библиотечный":
        library_make_circle(x, y, radius)

    if choice_algoritm == "Канонический":
        normal_c(x,y,radius)

    if choice_algoritm == "Параметрический":
        param_c(x, y, radius)

    if choice_algoritm == "Брезенхема":
        brezenham_c(x, y, radius)

    if choice_algoritm == "Средней точки":
        middle_point_c(x, y, radius)


def library_o(x, y, r1, r2):
    global colour
    canv.create_oval(x - r1, y - r2, x + r1, y + r2, outline=colour, width=1)
    return []


def normal_o(xc, yc, a, b):
    global colour
    points = list()
    sqr_a = a * a
    sqr_b = b * b
    sqr_ab = sqr_a * sqr_b

    limit1 = round(xc + a / sqrt(1 + sqr_b / sqr_a))

    for x in range(xc, limit1):
        y = yc + sqrt(sqr_ab - (x - xc) * (x - xc) * sqr_b) / a
        points.append(Point(x, y, colour))

    limit2 = round(yc + b / sqrt(1 + sqr_a / sqr_b))

    for y in range(limit2, yc - 1, -1):
        x = xc + sqrt(sqr_ab - (y - yc) * (y - yc) * sqr_a) / b
        points.append(Point(x, y, colour))

    dup_x(points, xc, yc)
    dup_y(points, xc, yc)

    draw_figure(points)

    return points


def param_o(x, y, r1, r2):
    global colour
    points = list()
    step = 1 / r1 if r1 > r2 else 1 / r2
    for t in np.arange(0, pi / 2 + step, step):
        a = x + r1 * cos(t)
        b = y + r2 * sin(t)
        points.append(Point(a, b, colour))

    dup_x(points, x, y)
    dup_y(points, x, y)

    draw_figure(points)

    return points


def brezenham_o(xc, yc, a, b):
    points = list()
    global colour
    x = 0
    y = b
    sqr_b = b * b
    sqr_a = a * a
    points.append(Point(x + xc, y + yc, colour))
    delta = sqr_b - sqr_a * (2 * b + 1)

    while y > 0:
        if delta <= 0:
            d1 = 2 * delta + sqr_a * (2 * y - 1)
            x += 1
            delta += sqr_b * (2 * x + 1)
            if d1 >= 0:
                y -= 1
                delta += sqr_a * (-2 * y + 1)

        else:
            d2 = 2 * delta + sqr_b * (-2 * x - 1)
            y -= 1
            delta += sqr_a * (-2 * y + 1)
            if d2 < 0:
                x += 1
                delta += sqr_b * (2 * x + 1)

        points.append(Point(x + xc, y + yc, colour))

    dup_x(points, xc, yc)
    dup_y(points, xc, yc)
    draw_figure(points)

    return points


def middle_point_o(xc, yc, a, b):
    global colour
    points = list()
    sqr_a = a * a
    sqr_b = b * b


    # x, where y` = -1
    limit = round(a / sqrt(1 + sqr_b / sqr_a))

    x = 0
    y = b
    points.append(Point(x + xc, y + yc, colour))

    fu = sqr_b - round(sqr_a * (b - 1 / 4))
    while x < limit:
        if fu > 0:
            y -= 1
            fu -= 2 * sqr_a * y

        x += 1
        fu += sqr_b * (2 * x + 1)
        points.append(Point(x + xc, y + yc, colour))

    # y, where y` = -1
    limit = round(b / sqrt(1 + sqr_a / sqr_b))

    y = 0
    x = a
    points.append(Point(x + xc, y + yc, colour))

    fu = sqr_a - round(sqr_b * (a - 1 / 4))
    while y < limit:
        if fu > 0:
            x -= 1
            fu -= 2 * sqr_b * x

        y += 1
        fu += sqr_a * (2 * y + 1)
        points.append(Point(x + xc, y + yc, colour))


    dup_y(points, xc, yc)
    dup_x(points, xc, yc)
    draw_figure(points)

    return points



def make_ellipse():
    try:
        choice_algoritm = combo_choose_algoritm.get()
        x = int(entry_for_center_x_ellips.get())
        y = int(entry_for_center_y_ellips.get())
        r1 = int(entry_for_ellips_a.get())
        r2 = int(entry_for_ellips_b.get())
    except:
        mb.showinfo("Ошибка", "Введите корректные значения")
        return

    if (choice_algoritm == "Библиотечный"):
        library_o(x, y, r1, r2)

    if (choice_algoritm == "Канонический"):
        normal_o(x, y, r1, r2)

    if (choice_algoritm == "Параметрический"):
        param_o(x, y, r1, r2)

    if (choice_algoritm == "Брезенхема"):
        brezenham_o(x, y, r1, r2)

    if (choice_algoritm == "Средней точки"):
        middle_point_o(x, y, r1, r2)


def make_more_cicles():
    try:
        choice_algoritm = combo_choose_algoritm.get()
        count = int(entry_for_count_circles.get())
        x = int(entry_for_center_x.get())
        y = int(entry_for_center_y.get())
        start_radius = int(entry_for_start_radius.get())
        step_radis = int(entry_for_step_radius.get())
    except:
        mb.showinfo("Ошибка", "Введите корректные значения")
        return
    radius = start_radius
    for i in range(count):

        if choice_algoritm == "Библиотечный":
            library_make_circle(x, y, radius)

        if choice_algoritm == "Канонический":
            normal_c(x, y, radius)

        if choice_algoritm == "Параметрический":
            param_c(x, y, radius)

        if choice_algoritm == "Брезенхема":
            brezenham_c(x, y, radius)

        if choice_algoritm == "Средней точки":
            middle_point_c(x, y, radius)

        radius += step_radis





def make_more_ellips():
   # try:
    choice_algoritm = combo_choose_algoritm.get()
    start_radius_a = int(entry_for_ellips_start_a.get())
    start_radius_b = int(entry_for_ellips_start_b.get())
    x = int(entry_for_center_x_ellips.get())
    y = int(entry_for_center_y_ellips.get())
    count = int(entry_for_ellips_count.get())
    step_radius = int(entry_for_ellips_step.get())
    #except:
     #   mb.showinfo("Ошибка", "Введите корректные значения")
      #  return

    r1 = start_radius_a
    r2 = start_radius_b

    for i in range(count):
        if (choice_algoritm == "Библиотечный"):
            library_o(x, y, r1, r2)

        if (choice_algoritm == "Канонический"):
            normal_o(x, y, r1, r2)

        if (choice_algoritm == "Параметрический"):
            param_o(x, y, r1, r2)

        if (choice_algoritm == "Брезенхема"):
            brezenham_o(x, y, r1, r2)

        if (choice_algoritm == "Средней точки"):
            middle_point_o(x, y, r1, r2)

        r1 += step_radius
        r2 += step_radius


def clear_all():
    global colour, colour_line
    colour = "#000000"
    colour_line = ((0.0, 0.0, 0.0), '#000000')
    canv.delete("all")
    canv.create_rectangle(1500, 130, 1550, 180, fill=colour)


def diff_time_circle():
    x = 100
    y = 100
    start_r = 10


    r = [0] * 20

    times = [0] * 5
    for i in range(5):
        times[i] = []

    step = 500
    r[0] = start_r
    for i in range(1, 20):
        r[i] = r[i - 1] + step

    print(r)


    for i in range(20):
        start_time_library = time.time()
        library_make_circle(x, y, r[i])
        end_time_library = time.time()
        time_library = end_time_library - start_time_library
        times[0].append(time_library)





    for i in range(20):
        start_time_canon = time.time()
        normal_c(x, y, r[i])
        end_time_canon = time.time()
        time_canon = end_time_canon - start_time_canon
        times[1].append(time_canon)


    for i in range(20):
        start_time_param = time.time()
        param_c(x, y, r[i])
        end_time_param = time.time()
        time_param = end_time_param - start_time_param
        times[2].append(time_param)



    for i in range(20):
        start_time_brezenham = time.time()
        brezenham_c(x, y, r[i])
        end_time_brezenham = time.time()
        time_brezenham = end_time_brezenham - start_time_brezenham
        times[3].append(time_brezenham)



    for i in range(20):
        start_time_middle_point = time.time()
        middle_point_c(x, y, r[i])
        end_time_middle_point = time.time()
        time_middle_point = end_time_middle_point - start_time_middle_point
        times[4].append(time_middle_point)

    print(times)

    print(r)

    Methods = ["Библотечный", "Канонический", "Параметрический", "Брезенхема", "Средней точки"]

    for i in range(5):
        plt.plot(r, times[i], label = Methods[i])

    clear_all()

    plt.legend()

    plt.xlabel('Размеры')
    plt.ylabel('Время')

    plt.grid()
    plt.show()

def diff_time_ellips():
    x = 100
    y = 100
    a = 10
    b = 20
    r_a = [0] * 20
    r_b = [0] * 20
    step = 500
    r_a[0] = a
    r_b[0] = b
    for i in range(1, 20):
        r_a[i] = r_a[i - 1] + step
        r_b[i] = r_b[i - 1] + step

    times = [0] * 5
    for i in range(len(times)):
        times[i] = []

    for i in range(20):
        start_time_library = time.time()
        library_o(x, y, r_a[i], r_b[i])
        end_time_library = time.time()
        time_library = end_time_library - start_time_library
        times[0].append(time_library)





    for i in range(20):
        start_time_canon = time.time()
        normal_o(x, y, r_a[i], r_b[i])
        end_time_canon = time.time()
        time_canon = end_time_canon - start_time_canon
        times[1].append(time_canon)


    for i in range(20):
        start_time_param = time.time()
        param_o(x, y, r_a[i], r_b[i])
        end_time_param = time.time()
        time_param = end_time_param - start_time_param
        times[2].append(time_param)



    for i in range(20):
        start_time_brezenham = time.time()
        brezenham_o(x, y, r_a[i], r_b[i])
        end_time_brezenham = time.time()
        time_brezenham = end_time_brezenham - start_time_brezenham
        times[3].append(time_brezenham)



    for i in range(20):
        start_time_middle_point = time.time()
        middle_point_o(x, y, r_a[i], r_b[i])
        end_time_middle_point = time.time()
        time_middle_point = end_time_middle_point - start_time_middle_point
        times[4].append(time_middle_point)

    Methods = ["Библотечный", "Канонический", "Параметрический", "Брезенхема", "Средней точки"]

    for i in range(5):
        plt.plot(r_a, times[i], label=Methods[i])

    clear_all()

    plt.legend()

    plt.xlabel('Размеры')
    plt.ylabel('Время')

    plt.grid()
    plt.show()





canv = Canvas(root, width=1800, height=900, bg="white")
canv.place(x=0, y=0)


label_for_choose_algoritm = Label(root, text = "Выберите алгоритм из списка")
label_for_choose_algoritm.place(x = 1300, y = 30, width=200, height = 30)



combo_choose_algoritm = Combobox(root, state = 'readonly')
combo_choose_algoritm['values'] = ("Канонический", "Параметрический", "Брезенхема", "Средней точки", "Библиотечный")
combo_choose_algoritm.current(0)
combo_choose_algoritm.place(x = 1300, y = 80, width = 200, height = 30)


label_for_colour = Label(root, text = "Выберите цвет")
label_for_colour.place(x = 1200, y = 130, width = 200, height = 30)

button_colour = Button(root, text="Выбрать цвет", command=select_colour)
button_colour.place(x=1200, y=130, width=200, height=30)
canv.create_rectangle(1500, 130, 1550, 180, fill = "black")

label_for_circle_center = Label(root, text = "Введите центр окружности")
label_for_circle_center.place(x = 1200, y = 250, width = 200, height = 30)

label_for_center_x = Label(root, text = "X")
label_for_center_x.place(x = 1550, y = 220, width = 50, height = 15)

label_for_center_x = Label(root, text = "Y")
label_for_center_x.place(x = 1700, y = 220, width = 50, height = 15)

entry_for_center_x = Entry(root)
entry_for_center_x.place(x = 1550, y = 250, width = 50, height = 30)

entry_for_center_y = Entry(root)
entry_for_center_y.place(x = 1700, y = 250, width = 50, height = 30)


label_for_one_circle = Label(root, text = "Введите радиус\nдля построения\nодной окружности")
label_for_one_circle.place(x = 1200, y = 330, width = 200, height = 50)

entry_for_radius = Entry(root)
entry_for_radius.place(x = 1525, y = 330, width = 50, height = 30)

label_for_radius = Label(root, text = "Радиус")
label_for_radius.place(x = 1500, y = 290, width = 100, height = 40)

btn_for_make_circle = Button(root, text = "Построить окружность", command = make_circle, state = "disabled")
btn_for_make_circle.place(x = 1600, y = 330, width = 175, height = 40)


label_for_many_circles = Label(root, text = "Введите значения для\nпостроения спектра\nконцентрических окружностей")
label_for_many_circles.place(x = 1200, y = 420, width = 200, height = 50)

entry_for_start_radius = Entry(root)
entry_for_start_radius.place(x = 1450, y = 420, width = 50, height = 40)

label_for_count_circles = Label(root, text = "Начальный\nрадиус")
label_for_count_circles.place(x = 1430, y = 380, width = 88, height = 30)

entry_for_step_radius = Entry(root)
entry_for_step_radius.place(x = 1550, y = 420, width = 50, height = 40)

label_for_count_circles = Label(root, text = "Шаг\nрадиуса")
label_for_count_circles.place(x = 1530, y = 380, width = 88, height = 30)

entry_for_count_circles = Entry(root)
entry_for_count_circles.place(x = 1650, y = 420, width = 50, height = 40)

label_for_count_circles = Label(root, text = "Количество\nокружностей")
label_for_count_circles.place(x = 1630, y = 380, width = 88, height = 30)

btn_for_make_more_circles = Button(root, text = "Построить спектр\nконцентрических окружностей", command = make_more_cicles, state = "disabled")
btn_for_make_more_circles.place(x = 1450, y = 480, width = 205, height = 60)

label_for_ellips_center = Label(root, text = "Введите центр эллипса")
label_for_ellips_center.place(x = 1200, y = 580, width = 200, height = 30)

entry_for_center_x_ellips = Entry(root)
entry_for_center_x_ellips.place(x = 1550, y = 580, width = 50, height = 30)

label_for_center_x_elllips = Label(root, text = "X")
label_for_center_x_elllips.place(x = 1530, y = 560, width = 88, height = 15)

entry_for_center_y_ellips = Entry(root)
entry_for_center_y_ellips.place(x = 1700, y = 580, width = 50, height = 30)

label_for_center_y_elllips = Label(root, text = "Y")
label_for_center_y_elllips.place(x = 1680, y = 560, width = 88, height = 15)

label_for_ellips_center = Label(root, text = "Введите данные\nдля построения эллипса")
label_for_ellips_center.place(x = 1200, y = 640, width = 200, height = 30)

entry_for_ellips_a = Entry(root)
entry_for_ellips_a.place(x = 1430, y = 640, width = 50, height = 30)

label_for_a_ellips = Label(root, text = "R1")
label_for_a_ellips.place(x = 1410, y = 620, width = 88, height = 15)

entry_for_ellips_b = Entry(root)
entry_for_ellips_b.place(x = 1530, y = 640, width = 50, height = 30)

label_for_b_ellips = Label(root, text = "R2")
label_for_b_ellips.place(x = 1510, y = 620, width = 88, height = 15)

label_for_many_ellips = Label(root, text = "Введите данные\nдля построения спектра\nконцентрических эллипсов")
label_for_many_ellips.place(x = 1200, y = 700, width = 200, height = 50)

entry_for_ellips_start_a = Entry(root)
entry_for_ellips_start_a.place(x = 1430, y = 700, width = 50, height = 30)

label_for_ellips_start_a = Label(root, text = "Начальный R1")
label_for_ellips_start_a.place(x = 1410, y = 675, width = 88, height = 15)

entry_for_ellips_start_b = Entry(root)
entry_for_ellips_start_b.place(x = 1530, y = 700, width = 50, height = 30)

label_for_ellips_start_a = Label(root, text = "Начальный R2")
label_for_ellips_start_a.place(x = 1510, y = 675, width = 88, height = 15)

entry_for_ellips_step = Entry(root)
entry_for_ellips_step.place(x = 1630, y = 700, width = 50, height = 30)

label_for_ellips_start_a = Label(root, text = "Шаг радиуса")
label_for_ellips_start_a.place(x = 1610, y = 675, width = 88, height = 15)

entry_for_ellips_count = Entry(root)
entry_for_ellips_count.place(x = 1730, y = 700, width = 50, height = 30)

label_for_ellips_start_a = Label(root, text = "Кол-во\nокружностей")
label_for_ellips_start_a.place(x = 1710, y = 675, width = 88, height = 30)

btn_for_make_ellips = Button(root, text = "Построить эллипс", command = make_ellipse, state = "disabled")

btn_for_make_ellips.place(x = 1600, y = 640, width = 170, height = 30)

btn_for_make_more_ellips = Button(root, text = "Построить спектр\nконцентрических эллипсов", command = make_more_ellips, state = "disabled")
btn_for_make_more_ellips.place(x = 1500, y = 760, width = 230, height = 60)

btn_for_clear = Button(root, text = "Очистить всё", command = clear_all)
btn_for_clear.place(x = 1500, y = 840, width = 230, height = 30)

btn_for_time_circle = Button(root, text = "Сравнить время\nпостроения окружностей", command = diff_time_circle)
btn_for_time_circle.place(x = 1200, y = 840, width = 230, height = 30)

btn_for_time_ellips = Button(root, text = "Сравнить время\nпостроения эллипсов", command = diff_time_ellips)
btn_for_time_ellips.place(x = 1200, y = 800, width = 230, height = 30)


mainloop()

root.mainloop()