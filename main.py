from math import pi, cos, sin, sqrt, radians
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import colorchooser
from tkinter import messagebox as mb
from config import Point
import config as cfg
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
        btn_for_make_circle.config(state = "normal")
    except:
        btn_for_make_circle.config(state="disabled")
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

btn_for_make_circle = Button(root, text = "Построить окружность", command = make_circle)
btn_for_make_circle.place(x = 1600, y = 330, width = 175, height = 40)


label_for_many_circles = Label(root, text = "Введите значения для\nпостроения спектра\nконцентрических окружностей")
label_for_many_circles.place(x = 1200, y = 420, width = 200, height = 50)

entry_for_start_radius = Entry(root)
entry_for_start_radius.place(x = 1450, y = 420, width = 50, height = 40)

entry_for_step_radius = Entry(root)
entry_for_step_radius.place(x = 1550, y = 420, width = 50, height = 40)

entry_for_count_circles = Entry(root)
entry_for_count_circles.place(x = 1650, y = 420, width = 50, height = 40)

btn_for_make_more_circles = Button(root, text = "Построить спектр\nконцентрических окружностей")
btn_for_make_more_circles.place(x = 1450, y = 480, width = 205, height = 60)

label_for_ellips_center = Label(root, text = "Введите центр эллипса")
label_for_ellips_center.place(x = 1200, y = 580, width = 200, height = 30)

entry_for_center_x_ellips = Entry(root)
entry_for_center_x_ellips.place(x = 1550, y = 580, width = 50, height = 30)

entry_for_center_y_ellips = Entry(root)
entry_for_center_y_ellips.place(x = 1700, y = 580, width = 50, height = 30)

label_for_ellips_center = Label(root, text = "Введите данные\nдля построения эллипса")
label_for_ellips_center.place(x = 1200, y = 640, width = 200, height = 30)

entry_for_ellips_a = Entry(root)
entry_for_ellips_a.place(x = 1430, y = 640, width = 50, height = 30)

entry_for_ellips_b = Entry(root)
entry_for_ellips_b.place(x = 1530, y = 640, width = 50, height = 30)

label_for_many_ellips = Label(root, text = "Введите данные\nдля построения спектра\nконцентрических эллипсов")
label_for_many_ellips.place(x = 1200, y = 700, width = 200, height = 50)

entry_for_ellips_start_a = Entry(root)
entry_for_ellips_start_a.place(x = 1430, y = 700, width = 50, height = 30)

entry_for_ellips_start_b = Entry(root)
entry_for_ellips_start_b.place(x = 1530, y = 700, width = 50, height = 30)

entry_for_ellips_step = Entry(root)
entry_for_ellips_step.place(x = 1630, y = 700, width = 50, height = 30)

entry_for_ellips_count = Entry(root)
entry_for_ellips_count.place(x = 1730, y = 700, width = 50, height = 30)

btn_for_make_ellips = Button(root, text = "Построить эллипс")
btn_for_make_ellips.place(x = 1600, y = 640, width = 170, height = 30)

btn_for_make_more_ellips = Button(root, text = "Построить спектр\nконцентрических эллипсов")
btn_for_make_more_ellips.place(x = 1500, y = 760, width = 230, height = 60)

btn_for_clear = Button(root, text = "Очистить всё")
btn_for_clear.place(x = 1500, y = 840, width = 230, height = 30)


mainloop()

root.mainloop()