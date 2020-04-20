#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from copy import deepcopy
from math import *
from tkinter import *
from tkinter import messagebox as mb

import tkinter.messagebox as box

root = Tk()

root.title("Построение Кота Свердлов Сергей ИУ7 - 43Б")


win_size = 800
radius_point = 3
list_point = []
false = "-"
inverse_matrix = [[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]]


label_for_scale = Label(text = "Введите rx, ry, dx, dy и размер\nчерез пробел")
label_for_flip = Label(text = "Введите угол поворота\nи координаты точки через пробел")
label_for_transfer = Label(text = "Введите координаты\nдля переноса")


def scale():
    string = entry_for_scale.get()

    if len(string.split()) != 4:
        box.showinfo("Ошибка", "Введено неверное количество значений, необходимо ввести два вещественных и два целых числа")
        return 1


    try:
        string = string.split()

        kx = float(string[0])

        ky = float(string[1])


        xm = int(string[2])

        ym = int(string[3])
    except:
        box.showinfo("Ошибка", "Введены некорректные данные")
        return 1

    if kx == 0 and ky == 0:
        box.showinfo("Ошибка", "Введены rx = 0 и ry = 0, кот исчезнет")
        return 1

    matrix = [[kx, 0, 0],
              [0, ky, 0],
              [0, 0, 1]]

    matrix_mov = [[1, 0, 0],
                  [0, 1, 0],
                  [xm, ym, 1]]

    matrix_res = multiplication_matrix(matrix_mov, matrix)
    matrix_mov[2][0], matrix_mov[2][1] = -xm, -ym
    matrix_res = multiplication_matrix(matrix_res, matrix_mov)

    global inverse_matrix
    # inverse_matrix = inverse_func(matrix)
    inverse_matrix = inverse_func(matrix_res)

    for i in range(len(list_point)):
        list_point[i] = multiplication_vector(list_point[i], matrix_res)
        # list_point[i] = np.dot(list_point[i], matrix)

    print_scene()



def multiplication_matrix(matrix_a, matrix_b):
    matrix_res = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            temp = 0
            for k in range(3):
                temp += matrix_a[i][k] * matrix_b[k][j]
            matrix_res[i][j] = temp
    return matrix_res

def rotation():
    string = entry_for_flip.get()

    if len(string.split()) != 3:
        box.showinfo("Ошибка", "Введено неверное количество значений, необходимо ввести три целых числа")
        return 1

    try:
        string = string.split()

        angle = int(string[0])

        xm = int(string[1])

        ym = int(string[2])
    except:
        box.showinfo("Ошибка", "Введены не числовые значения")
        return 1


    dx = -xm
    dy = -ym

    # Переводим в радианы.
    angle *= pi / 180
    matrix = [[cos(angle), sin(angle), 0],
              [-sin(angle), cos(angle), 0],
              [0, 0, 1]]

    matrix_mov = [[1, 0, 0],
                  [0, 1, 0],
                  [dx, dy, 1]]

    matrix_res = multiplication_matrix(matrix_mov, matrix)
    matrix_mov[2][0], matrix_mov[2][1] = -dx, -dy
    matrix_res = multiplication_matrix(matrix_res, matrix_mov)

    global inverse_matrix

    for i in range(len(list_point)):
        list_point[i] = multiplication_vector(list_point[i], matrix_res)

    inverse_matrix = inverse_func(matrix_res)

    print_scene()

def func_x(t):
    size = 37
    return 2 * cos(t) * size

def func_y(t):
    size = 37
    return 2 * sin(t) * size + 200


def func_x_2(t):
    size = 6
    return 2 * cos(t) * size + 35

def func_y_2(t):
    size = 6
    return 2 * sin(t) * size + 230

def func_x_3(t):
    size = 6
    return 2 * cos(t) * size - 35

def func_y_3(t):
    size = 6
    return 2 * sin(t) * size + 230


def func_x_4(t):
    size = 37
    return 2.4 * cos(t) * size

def func_y_4(t):
    size = 32
    return 4 * sin(t) * size

def check(event):
    if event.char == '\r':
        pass
    if event.char=="\x08":
        pass

root.bind("<Key>",check)

entry_for_flip = Entry(root)

entry_for_scale = Entry(root)

entry_for_transfer = Entry(root)

y = []
b = 0
n = int()
flag = 1
# Настройка экрана
w = root.winfo_screenwidth()  # ширина экрана
h = root.winfo_screenheight()  # высота экрана
w = w // 2  # середина экрана
h = h // 2

def minor(m, i, j):
    return m[(i + 1) % 3][(j + 1) % 3] * m[(i + 2) % 3][(j + 2) % 3] - \
        m[(i + 1) % 3][(j + 2) % 3] * m[(i + 2) % 3][(j + 1) % 3]

def determinant(m):
    det = 0
    for i in range(3):
        det += m[0][i] * minor(m, 0, i)

    return det


def transpose(matrix):
    matrix_res = deepcopy(matrix)

    for i in range(3):
        for j in range(0, i):
            matrix_res[i][j], matrix_res[j][i] = matrix_res[j][i], matrix_res[i][j]

    return matrix_res

def multiplication_vector(vector, matrix):
    vector_res = [0, 0, 0]

    for i in range(3):
        temp = 0
        for k in range(3):
            temp += vector[k] * matrix[k][i]
        vector_res[i] = temp

    return vector_res


def inverse_func(matrix):
    matrix_res = transpose(matrix)
    matrix_copy = deepcopy(matrix_res)

    # Ищем определитель матрицы
    det = determinant(matrix_res)
    if det == 0:
        print("det = ", det)
        # det = 1
        return

    # Ищем алгебраич. доп.
    for i in range(3):
        for j in range(3):
            matrix_res[i][j] = minor(matrix_copy, i, j) / det

    return matrix_res

def moving_func(dx, dy):
    matrix_mov = [[1, 0, 0],
                  [0, 1, 0],
                  [dx, dy, 1]]

    global inverse_matrix

    inverse_matrix = inverse_func(matrix_mov)

    for i in range(len(list_point)):
        list_point[i] = multiplication_vector(list_point[i], matrix_mov)
        
    print_scene()


def moving():
    string = entry_for_transfer.get()

    if len(string.split()) != 2:
        box.showinfo("Ошибка", "Введено неверное количество значений, необходимо два целых числа")
        return 1


    try:
        string = string.split()

        dx = int(string[0])

        dy = int(string[1])

    except:
        box.showinfo("Ошибка", "Необходимо ввести два целых числа")
        return 1


    moving_func(dx, dy)

def paint_point(cordinate):
    r = 1
    t = win_size / 2
    x = cordinate[0]
    y = cordinate[1]
    canv.create_oval(x - r + t, -y - r + t,
                     x + r + t, -y + r + t, fill='black')


def paint_line(a, b):
    t = win_size / 2
    canv.create_line(a[0] + t, -a[1] + t, b[0] + t,
                     -b[1] + t, fill="black", width=3)

def cancel():
    global inverse_matrix
    for i in range(len(list_point)):
        list_point[i] = np.dot(list_point[i], inverse_matrix)
    inverse_matrix = [[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]]
    print_scene()


def print_scene():
    canv.delete(ALL)
    canv.create_line(win_size/2, win_size, win_size/2, 0, width=2, arrow=LAST)
    canv.create_line(0, win_size / 2, win_size,
                     win_size / 2, width=2, arrow=LAST)

    for i in range(len(list_point) - 2 - 8 - 6):
        paint_point(list_point[i])
        #paint_line(list_point[i], list_point[i + 1])


    paint_point(list_point[len(list_point) - 1 - 6 - 8])

    paint_line(list_point[len(list_point) - 14],
               list_point[len(list_point) - 13])
    paint_line(list_point[len(list_point) - 12],
               list_point[len(list_point) - 11])

    paint_line(list_point[len(list_point) - 10],
               list_point[len(list_point) - 9])
    paint_line(list_point[len(list_point) - 8],
               list_point[len(list_point) - 7])

    paint_line(list_point[len(list_point) - 6],
               list_point[len(list_point) - 5])

    paint_line(list_point[len(list_point) - 4],
               list_point[len(list_point) - 3])

    paint_line(list_point[len(list_point) - 2],
               list_point[len(list_point) - 1])

def return_all():
    global inverse_matrix
    inverse_matrix = [[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]]
    for i in range(len(list_point) - 1, -1, -1):
        del list_point[i]
    create_scene()

def create_scene():
    for i in np.arange(0, 2 * pi * 2, 0.01): #голова
        x = func_x(i)
        y = func_y(i)
        list_point.append([x, y, 1])



    for i in np.arange(0, 2 * pi * 2, 0.1): #правый глаз
        x = func_x_2(i)
        y = func_y_2(i)
        list_point.append([x, y, 1])

    for i in np.arange(0, 2 * pi * 2, 0.1): #левый глаз
        x = func_x_3(i)
        y = func_y_3(i)
        list_point.append([x, y, 1])

    for i in np.arange(0, 2 * pi * 2, 0.01): #тело
        x = func_x_4(i)
        y = func_y_4(i)
        list_point.append([x, y, 1])




    list_point.append([0, 0, 1])

    list_point.append([-90, 200, 1])
    list_point.append([90, 200, 1])

    list_point.append([-90, 180, 1])
    list_point.append([90, 220, 1])

    list_point.append([-90, 220, 1])
    list_point.append([90, 180, 1])

    list_point.append([-57, 250, 1])
    list_point.append([-45, 290, 1])


    list_point.append([-45, 290, 1])
    list_point.append([-35, 267, 1])


    list_point.append([57, 250, 1])
    list_point.append([45, 290, 1])

    list_point.append([45, 290, 1])
    list_point.append([35, 267, 1])



    print_scene()



root.geometry('800x800+{}+{}'.format(w, h))

canvas = Canvas(root, width = 800, height = 800, bg = '#FFE4E1')
canvas.place(x = 0, y = 0)

canv = Canvas(root, width=800, height=800, bg="white")

canv.place(x=0, y=0)


create_scene()



btn_for_flip = Button(root, text = "Перевернуть", command = rotation)
btn_for_flip.place(relx = 0.63, rely=0.17, relwidth=0.09, relheight=0.02)
label_for_flip.place(relx=0.6, rely=0.03, relwidth=0.15, relheight=0.07)
entry_for_flip.place(relx=0.6, rely=0.1, relwidth=0.15, relheight=0.05)


btn_for_flip = Button(root, text = "Масштабировать", command = scale)
btn_for_flip.place(relx = 0.63, rely=0.37, relwidth=0.09, relheight=0.02)
label_for_scale.place(relx = 0.6, rely = 0.23, relwidth=0.15, relheight=0.07)
entry_for_scale.place(relx = 0.6, rely = 0.3, relwidth=0.15, relheight=0.05)


btn_for_flip = Button(root, text = "Перенести", command = moving)
btn_for_flip.place(relx = 0.63, rely=0.57, relwidth=0.09, relheight=0.02)
label_for_transfer.place(relx=0.6, rely=0.43, relwidth=0.15, relheight=0.07)
entry_for_transfer.place(relx = 0.6, rely = 0.5, relwidth=0.15, relheight=0.05)





btn_for_flip = Button(root, text = "Вернуть всё", command = return_all)
btn_for_flip.place(relx = 0.63, rely=0.67, relwidth=0.09, relheight=0.02)

btn_for_flip = Button(root, text = "Один шаг назад", command =cancel)
btn_for_flip.place(relx = 0.63, rely=0.77, relwidth=0.09, relheight=0.02)

root.mainloop()
