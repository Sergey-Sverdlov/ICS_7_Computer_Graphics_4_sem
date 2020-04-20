import tkinter.colorchooser
from tkinter import *
from tkinter import scrolledtext as tkst
from tkinter import messagebox as mb
from tkinter import colorchooser
import time
from math import *
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = Tk()
root.title("Сравнение методов построения отрезков")

var = IntVar()
canv = Canvas(root, width=1500, height=900, bg="white")
canv.place(x=0, y=0)

def sign(a):
    if a == 0:
        return 0
    return a / abs(a)

def print_pixel(x, y, colour):
    canv.create_line(round(x), round(y), round(
        x), round(y) + 1, width=1, fill=colour)

def select_colour():
    global colour, colour_line
    colour = tkinter.colorchooser.askcolor()
    canv.create_rectangle(1220, 250, 1270, 300, fill = colour[1])
    colour_line = colour
    colour = colour[1]

    return colour


def bresenham_int(start, stop, colour):
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]
    x, y = start[0], start[1]
    sx, sy = sign(dx), sign(dy)
    dx = fabs(dx)
    dy = fabs(dy)

    swap = 0

    if dy > dx:
        swap = 1
        dx, dy = dy, dx

    e = 2 * dy - dx

    for _ in range(int(dx + 1)):
        print_pixel(x, y, colour)


        if e >= 0:
            if swap == 0:
                y += sy
            else:
                x += sx
            e -= (2 * dx)

        if e < 0:
            if swap == 0:
                x += sx
            else:
                y += sy
            e += (2 * dy)


def bresenham_float(start, stop, colour):
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]
    x, y = start[0], start[1]
    sx, sy = sign(dx), sign(dy)
    dx = fabs(dx)
    dy = fabs(dy)

    swap = 0
    if dy > dx:
        swap = 1
        dx, dy = dy, dx
    m = dy / dx
    e = m - 0.5

    for _ in range(int(dx + 1)):
        print_pixel(x, y, colour)
        if e >= 0:
            if swap == 0:
                y += sy
            else:
                x += sx
            e -= 1

        if swap == 0:
            x += sx
        else:
            y += sy
        e += m

def parse_color(color):
    color_str = "#"
    for i in range(3):
        temp = hex(int(color[i]))
        temp = temp[2:]

        if int(temp, base=16) <= 15:
            temp = "0" + temp
        color_str += str(temp)
    return color_str


def print_pixel_color(x, y, intensity):
    global colour_line
    intensity = fabs(intensity)
    intensity_color = list(colour_line[0])
    for i in range(3):
        if fabs(round(intensity_color[i]) - 256) < 2:
            continue

        intensity_color[i] = (255 - intensity_color[i]) * intensity

    canv.create_line(round(x), round(y), round(
        x), round(y) + 1, width=1, fill=parse_color(intensity_color))




def bresenham_smooth(start, stop):
    global colour_line
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]
    x, y = start[0], start[1]
    sx, sy = sign(dx), sign(dy)
    dx = fabs(dx)
    dy = fabs(dy)

    swap = 0
    if dy > dx:
        swap = 1
        dx, dy = dy, dx
    m = dy / dx
    e = 0.5

    for _ in range(int(dx + 1)):
        print_pixel_color(x, y, 1 - e)

        if e >= 1:
            if swap == 0:
                y += sy
            else:
                x += sx
            e -= 1
        if swap == 0:
            x += sx
        else:
            y += sy
        e += m


def vu(start, stop):
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]
    x, y = start[0], start[1]
    sx, sy = sign(dx), sign(dy)
    dx = fabs(dx)
    dy = fabs(dy)

    swap = 0
    if dy > dx:
        swap = 1
        dx, dy = dy, dx
    m = dy / dx
    e = 0.5
    w = 1
    for _ in range(int(dx + 1)):
        if swap == 0:
            print_pixel_color(x, y, - e)
            print_pixel_color(x, y + sy, e - 1)
        else:
            print_pixel_color(x, y, e)
            print_pixel_color(x + sx, y, e - 1)

        if e >= w - m:
            if swap == 0:
                y += sy
            else:
                x += sx
            e -= 1
        if swap == 0:
            x += sx
        else:
            y += sy
        e += m


def differential_analyzer(start, stop):
    global colour
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]

    if fabs(dx) - fabs(dy) >= 0:
        l = fabs(dx)
    else:
        l = fabs(dy)

    dx, dy = dx / l, dy / l
    x, y = start[0], start[1]

    # print("l = ", l)
    for _ in range(int(l + 1)):
        print_pixel(x, y, colour)
        x += dx
        y += dy




def make_line():
    try:
        x1 = int(entry_first_x.get())
        y1 = int(entry_first_y.get())
        x2 = int(entry_second_x.get())
        y2 = int(entry_second_y.get())
        start = []
        start.append(x1)
        start.append(y1)
        stop = []
        stop.append(x2)
        stop.append(y2)
    except:
        mb.showinfo("Ошибка", "Введены некорректные значения")
        return

    if var.get() == 1:
            canv.create_line(x1, y1, x2, y2, fill = colour)

    if var.get() == 2:
        vu(start, stop)

    if var.get() == 3:
        bresenham_int(start, stop, colour)

    if var.get() == 4:
        bresenham_float(start, stop, colour)

    if var.get() == 5:
        bresenham_smooth(start, stop)

    if var.get() == 6:
        differential_analyzer(start, stop)


    if var.get() == 0:
        mb.showinfo("Ошибка", "Необходимо выбрать метод построения отрезка")


def library_method(a, b):
    global  colour_line
    canv.create_line(a[0], a[1], b[0], b[1], fill=colour_line[1])

def paint_lines():
    global colour

    method = var.get()

    try:

        length = int(entry_len_circle.get())


        step = int(entry_angle_pitch.get())
    except:
        mb.showinfo("Ошибка", "Введите целые числа для длины пучка и его шага")


    method = var.get()

    x, y = length + 800 / 2, 800 / 2
    t = step
    start = (800 / 2, 800 / 2)

    for _ in range(int(360 / step)):
        if method == 1:
            differential_analyzer(start, (round(x), round(y)))
        elif method == 2:
            bresenham_float(start, (round(x), round(y)), colour)
        elif method == 3:
            bresenham_int(start, (round(x), round(y)), colour)
        elif method == 4:
            # print(start, (round(x), round(y)))
            bresenham_smooth(start, (round(x), round(y)))
        elif method == 5:
            library_method(start, (round(x), round(y)))
        elif method == 6:
            vu(start, (round(x), round(y)))

        x = length * cos(t * pi / 180) + 800 / 2
        y = -(length * sin(t * pi / 180)) + 800 / 2
        t += step

def clear_all():
    global colour, colour_line
    canv.delete("all")
    entry_first_x.delete(0, END)
    entry_first_y.delete(0, END)
    entry_second_x.delete(0, END)
    entry_second_y.delete(0, END)
    entry_len_circle.delete(0, END)
    entry_angle_pitch.delete(0, END)
    var.set(1)
    canv.create_rectangle(1220, 250, 1270, 300, fill='black')
    colour = 'black'
    colour_line = ((0.0, 0.0, 0.0), '#000000')

def create_scene():
    label_choose_method = Label(root, text="Выберите метод построения отрезка", font = "Arial 20")
    label_choose_method.place(x = 1000, y = 10, width = 350, height=100)

    var.set(1)
    rbutton1 = Radiobutton(root, text='Библиотечный метод', variable=var, value=1)
    rbutton2 = Radiobutton(root, text='Метод ВУ', variable=var, value=2)
    rbutton3 = Radiobutton(root, text='Метод Брезенхема с int', variable=var, value=3)
    rbutton4 = Radiobutton(root, text='Метод Брезенхема с float', variable=var, value=4)
    rbutton5 = Radiobutton(root, text='Метод Брезенхема(сглаживание)', variable=var, value=5)
    rbutton6 = Radiobutton(root, text='Метод ЦДА', variable=var, value=6)



    button_colour = Button(root, text = "Выбрать цвет отрезка", command = select_colour)
    button_colour.place(x = 850, y = 250, width = 250, height = 50)
    canv.create_rectangle(1220, 250, 1270, 300, fill='black')


    label_input_first_point = Label(root, text = "Введите первую точку", font = "Arial 20")
    label_input_first_point.place(x = 850, y = 320, width = 250, height = 30)

    label_input_second_point = Label(root, text = "Введите вторую точку", font = "Arial 20")
    label_input_second_point.place(x = 850, y = 370, width = 250, height = 30)



    label_x = Label(root, text = "X")
    label_x.place(x = 1310, y = 290, width = 20, height = 20)

    label_y = Label(root, text="Y")
    label_y.place(x=1410, y=290, width=20, height=20)


    button_make_line = Button(root, text='Нарисовать отрезок', command = make_line, font = "Arial 20")

    button_make_line.place(x=970, y=420, width = 260, height = 30)

    label_len_circle = Label(root, text = "Введите длину пучка", font = "Arial 20")
    label_len_circle.place(x = 850, y = 480, width = 270, height = 30)

    label_angle_pitch = Label(root, text = "Введите шаг изменения угла", font = "Arial 20")
    label_angle_pitch.place(x = 850, y = 530, width = 270, height = 30)




    but_make_cirlce = Button(root, text = "Нарисовать пучок", font = "Arial 20", command = paint_lines)
    but_make_cirlce.place(x = 970, y = 600, width = 270, height = 30)

    but_check_time = Button(root, text = "Сравнить время", font = "Arial 20", command = diff_time)
    but_check_time.place(x = 970, y = 750, width = 270, height = 30)


    but_clear_all = Button(root, text = "Очистить всё", font = "Arial 20", command = clear_all)
    but_clear_all.place(x = 970, y = 800, width = 270, height = 30)

    rbutton1.place(x = 850, y = 100, width = 200, height = 30)
    rbutton2.place(x = 1150, y = 100, width = 200, height = 30)
    rbutton3.place(x = 850, y = 150, width = 200, height = 30)
    rbutton4.place(x = 1150, y = 150, width = 200, height = 30)
    rbutton5.place(x = 850, y = 200, width = 250, height = 30)
    rbutton6.place(x = 1150, y = 200, width = 200, height = 30)

def diff_time():
    global colour
    try:
        x1 = int(entry_first_x.get())
        y1 = int(entry_first_y.get())
        x2 = int(entry_second_x.get())
        y2 = int(entry_second_y.get())
        start = []
        start.append(x1)
        start.append(y1)
        stop = []
        stop.append(x2)
        stop.append(y2)
    except:
        mb.showinfo("Ошибка", "Введите корректные координаты начала и конца отрезка")
        return


    start_time_library = time.time()
    for i in range(300):
        canv.create_line(x1, y1, x2, y2)

    end_time_library = time.time()

    start_time_vu = time.time()

    for i in range(300):

        vu(start, stop)

    end_time_vu = time.time()

    start_time_bresenham_int = time.time()

    for i in range(300):

        bresenham_int(start, stop, colour)

    end_time_bresenham_int = time.time()


    start_time_bresenham_float = time.time()

    for i in range(300):

        bresenham_float(start, stop, colour)

    end_time_bresenham_float = time.time()

    start_time_bresenham_smooth = time.time()

    for i in range(300):

        bresenham_smooth(start, stop)

    end_time_bresenham_smooth = time.time()

    start_time_differential_analyzer = time.time()

    for i in range(300):

        differential_analyzer(start, stop)

    end_time_differential_analyzer = time.time()

    time_library = end_time_library - start_time_library

    time_bresenham_int = end_time_bresenham_int - start_time_bresenham_int

    time_bresenham_float = end_time_bresenham_float - start_time_bresenham_float

    time_bresenham_smooth = end_time_bresenham_smooth - start_time_bresenham_smooth

    time_vu = end_time_vu - start_time_vu

    time_differential_analyzer = end_time_differential_analyzer - start_time_differential_analyzer

    clear_all()




    y = []

    y.append(time_library)
    y.append(time_bresenham_float)
    y.append(time_bresenham_int)
    y.append(time_bresenham_smooth)
    y.append(time_differential_analyzer)
    y.append(time_vu)

    window = Tk()
    window.geometry('750x750')
    window.title('Времянные характеристики')

    fig = Figure(figsize=(10, 10))
    ax = fig.add_subplot(111)


    ax.set_ylabel('Время (t) [секунды]')

    ind = ("Библиотечный", "Брезенхем\n(float)", "Брезенхем\n(int)",
           "Брезенхем\n(сглаживание)", "ЦДУ", "ВУ")
    ax.bar(ind, y, 0.4)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=RIGHT)

    window.mainloop()







entry_first_x = Entry(root)
entry_first_x.place(x = 1300, y = 320, width = 50, height = 30)

entry_first_y = Entry(root)
entry_first_y.place(x = 1400, y = 320, width = 50, height = 30)

entry_second_x = Entry(root)
entry_second_x.place(x = 1300, y = 370, width = 50, height = 30)

entry_second_y = Entry(root)
entry_second_y.place(x = 1400, y = 370, width = 50, height = 30)

entry_len_circle = Entry(root)
entry_len_circle.place(x=1150, y=480, width=270, height=30)

entry_angle_pitch = Entry(root)
entry_angle_pitch.place(x=1150, y=530, width=270, height=30)


colour = 'black'
colour_line = ((0.0, 0.0, 0.0), '#000000')
create_scene()

root.geometry('1500x900')

root.mainloop()
