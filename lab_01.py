from tkinter import *
from tkinter import messagebox
from math import *
from tkinter.simpledialog import askstring

max_coordinate = 400
radius_point = 2
root = Tk()
root.title('Свердлов Сергей ')
root.geometry("1500x900")
root.resizable(width = False,height = False)
root.configure(bg = "white")
array_with_points = list()
a = b = c = d = -1

center = None






def point_func():
    global entry_point
    try:
        x, y = entry_point.get().split(" ")
        x, y = int(x) + 400, 400 - int(y)
        entry_point.delete(0, END)
        array_with_points.append((x, y))
        listbox_pointer.insert(END, "{}     {}".format(int(x) - 400, 400 - int(y)))
    except:
        messagebox.showinfo("ОШИБКА", 'Некорректные данные')
        entry_point.delete(0, END)
        return
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                       fill="green", activefill='black')

def draw_from_file():
    array = ((72, 75), (120, 150), (55, 62), (70, 75), (100, 200), (71, 75), (50, 50), (200, 100), (170, 120), (51, 51), (52, 52), (170, 121), (170, 122), (120, 80), (100, 150), (150, 90))
    #array = ((50, 50), (100, 100), (150, 50))
    for x, y in array:
        array_with_points.append((400 + x, 400 - y))
        canvas.create_oval(x + 400 - 5, 400 - y - 5, x + 405, 400 - y + 5,
                           fill="green", activefill='black')


def is_triangle(x1, y1, x2, y2, x3, y3):
    ERROR = -1

    if (y2 - y1) * (x3 - x1) != (y3 - y1) * (x2 -x1):
        return True
    return ERROR



def is_point_inside_triangle(x, y, x1, y1, x2, y2, x3, y3):
    ERROR = -1
    a = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)
    b = (x2 - x) * (y3 - y2) - (x3 - x2) * (y2 - y)
    c = (x3 - x) * (y1 - y3) - (x1 - x3) * (y3 - y)

    if (a > 0 and b > 0 and c > 0 or a < 0 and b < 0 and c < 0):
        return TRUE
    return ERROR

def calculate_coefficient_A_B_C(x1, y1, x2, y2, x3, y3):
    A1 = y1 - (y3 + y2) / 2
    B1 = (x3 + x2) / 2 - x1
    C1 = x1 * (y3 + y2) / 2 - (x3 + x2) / 2 * y1

    A2 = y2 - (y1 + y3) / 2
    B2 = (x1 + x3) / 2 - x2
    C2 = x2 * (y1 + y3) / 2 - (x1 + x3) / 2 * y2

    A3 = y3 - (y1 + y2) / 2
    B3 = (x1 + x2) / 2 - x3
    C3 = x3 * (y1 + y2) / 2 - (x1 + x2) / 2 * y3

    return A1, B1, C1, A2, B2, C2, A3, B3, C3


def count_points_inside(array_with_points, x1, y1, x2, y2, x3, y3):

    array_with_points_inside = list()

    A4, B4, C4, A5, B5, C5, A6, B6, C6 = calculate_coefficient_A_B_C(x1, y1, x2, y2, x3, y3)


    if (B4 < 0):
        A4 = -A4
        C4 = -C4
        B4 = -B4

    if (B5 < 0):
        A5 = -A5
        C5 = -C5
        B5 = -B5

    if (B6 < 0):
        A6 = -A6
        C6 = -C6
        B6 = -B6

    count = [0] * 8


    for x,y in array_with_points:
        check = is_point_inside_triangle(x, y, x1, y1, x2, y2, x3, y3)
        if (check == TRUE):

            if (A5 * x + B5 * y + C5 >= 0 and A4 * x + B4 * y + C4 >= 0 and A6 * x + B6 * y + C6 >= 0):
                count[0] += 1

            if (A5 * x + B5 * y + C5 >= 0 and A4 * x + B4 * y + C4 >= 0 and A6 * x + B6 * y + C6 <= 0):
                count[1] += 1

            if (A5 * x + B5 * y + C5 >= 0 and A4 * x + B4 * y + C4 <= 0 and A6 * x + B6 * y + C6 >= 0):
                count[2] += 1


            if (A5 * x + B5 * y + C5 >= 0 and A4 * x + B4 * y + C4 <= 0 and A6 * x + B6 * y + C6 <= 0):
                count[3] += 1

            if (A5 * x + B5 * y + C5 <= 0 and A4 * x + B4 * y + C4 >= 0 and A6 * x + B6 * y + C6 >= 0):
                count[4] += 1

            if (A5 * x + B5 * y + C5 <= 0 and A4 * x + B4 * y + C4 >= 0 and A6 * x + B6 * y + C6 <= 0):
                count[5] += 1

            if (A5 * x + B5 * y + C5 <= 0 and A4 * x + B4 * y + C4 <= 0 and A6 * x + B6 * y + C6 >= 0):
                count[6] += 1

            if (A5 * x + B5 * y + C5 <= 0 and A4 * x + B4 * y + C4 <= 0 and A6 * x + B6 * y + C6 <= 0):
                count[7] += 1

            array_with_points_inside.append(x - 400)
            array_with_points_inside.append(400 - y)


    count.sort()

    return count, count[7] - count[2], array_with_points_inside


def general_func(array_with_points):
    flag = 0
    max_diff = -1
    max_count = list()
    matrix_triangle = list()
    for x1, y1 in array_with_points:
        for x2, y2 in array_with_points:
            if (x2 != x1 or y2 != y1):
                for x3, y3 in array_with_points:
                    if(x3 != x2 or y3 != y2):
                        if (x3 != x1 or y3 != y1):
                            check = is_triangle(x1, y1, x2, y2, x3, y3)
                            if (check != -1 and matrix_triangle.count((x1,y1, x2, y2, x3, y3)) == 0 and matrix_triangle.count((x1,y1, x3, y3, x2, y2)) == 0 \
                                   and matrix_triangle.count((x2, y2, x1, y1, x3, y3)) == 0 and matrix_triangle.count((x2,y2, x3, y3, x1, y1)) == 0 \
                                    and matrix_triangle.count((x3,y3, x2, y2, x1, y1)) == 0 and matrix_triangle.count((x3,y3, x1, y1, x2, y2)) == 0):
                                matrix_triangle.append((x1, y1, x2, y2, x3, y3))
                                count, diff, array_with_points_inside = count_points_inside(array_with_points, x1, y1, x2, y2, x3, y3)
                                if (diff > max_diff or flag == 0):
                                    max_diff = diff
                                    x1_max = x1
                                    y1_max = y1
                                    x2_max = x2
                                    y2_max = y2
                                    x3_max = x3
                                    y3_max = y3
                                    flag = 1
                                    max_count = count
                                    max_array_with_points_inside = array_with_points_inside

    try:
        messagebox.showinfo("Решение задания", "Треугольник найден!\nКоординаты его вершин:\nA({} {})\nB({} {})\nC({} {})\n".format(x1_max - 400, 400 - y1_max, x2_max - 400, 400 - y2_max, x3_max - 400, 400 - y3_max, ) +
                           "Самое большое количество в одном из шести треугольников: {}\nСамое маленькое количество в одном из шести треугольников: {}\
                                               Разница: {}".format(max_count[7], max_count[2], max_diff))
        canvas.create_line(x1_max, y1_max, x2_max, y2_max)
        canvas.create_line(x1_max, y1_max, x3_max, y3_max)
        canvas.create_line(x2_max, y2_max, x3_max, y3_max)
        print(x1_max, y1_max, x2_max, y2_max, x3_max, y3_max, max_diff)
        print(max_count)
        canvas.delete("all")
        show_result(x1_max - 400, 400 - y1_max, x2_max - 400, 400 - y2_max, x3_max - 400, 400 - y3_max, max_array_with_points_inside)

    except:
        messagebox.showinfo("Ошибка", "Три точки лежат на одной прямой")



def delete_point():
    global entry_point
    try:
        selection = listbox_pointer.curselection()
        string = listbox_pointer.get(selection[0])
        string = string.split()
        string[0] = int(string[0])
        string[1] = int(string[1])

        answer = messagebox.askyesno("Внимание", "Вы уверены, что хотите удалить точку с координатами x = {} y = {}".format(string[0], string[1]))

        if (answer != TRUE):
            return

        listbox_pointer.delete(selection[0])
        print(array_with_points)
        array_with_points.remove((400 + string[0], 400 - string[1]))
        print(array_with_points)
        canvas.delete("all")
        schedule()
        for x, y in array_with_points:
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                               fill="green", activefill='black')
    except:
        messagebox.showinfo("ОШИБКА", 'Для удаления точки выберите необходимую точку из списка всех точек\n и нажмите на нее мышкой, чтобы координаты\n точки подсвечивались')
        entry_point.delete(0, END)
        return

def change_point():
    try:
        selection = listbox_pointer.curselection()
        string = listbox_pointer.get(selection[0])
        string = string.split()
        string[0] = int(string[0])
        string[1] = int(string[1])

        try:

            coord = askstring("Изменение точки", "Введите новые координаты для точки\nСтарые координаты {} {}".format(string[0], string[1]))

            if (coord == None):
                return

            try:

                coord = coord.split()

                x = int(coord[0])

                y = int(coord[1])
            except:
                messagebox.showinfo("Ошибка", "Необходимо ввести два целых числа через пробел")
                return
        except:
            return

        print(x, y)

        listbox_pointer.insert(selection[0], "{}     {}".format(x, y))
        listbox_pointer.delete(selection[0] + 1)
        array_with_points.remove((400 + string[0], 400 - string[1]))
        array_with_points.append((400 + x, 400 - y))
        canvas.delete("all")
        schedule()
        for x, y in array_with_points:
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                               fill="green", activefill='black')


    except:
        messagebox.showinfo("ОШИБКА", 'Для изменения точки выберите необходимую точку из списка всех точек\n и нажмите на нее мышкой, чтобы координаты\n точки подсвечивались, затем введите два целых числа через пробел')
        entry_point.delete(0, END)
        return


def func():
    general_func(array_with_points)

def delete():
    global a, b, c, d
    canvas.delete("all")
    schedule()
    array_with_points.clear()
    if (a != -1):
        canvas.delete(a)
        canvas.delete(b)
        canvas.delete(c)
        canvas.delete(d)
    listbox_pointer.delete(1, END)


canvas = Canvas(root, width = 800, height = 600, bg = '#FFE4E1')
canvas.place(x = 100, y = 100)

listbox_pointer = Listbox()

listbox_pointer.place(x = 930, y = 200, width = 200, height=300)

listbox_pointer.insert(END, "X       Y")



label_point = Label(root, text='Введите x y \nточки через пробел', fg='green').place(x=20, y=15, width=190, height = 35)
entry_point = Entry(root, bg='white')
entry_point.place(x = 20, y = 50, width=190, height = 30)
draw_point = Button(root, text="Нарисовать точку\n на графике", fg='red', command=point_func)
draw_point.place(x=230, y=40, width=190, height = 50)

draw_point_from_file = Button(root, text="Изменить точку", fg='red', command=change_point)
draw_point_from_file.place(x=1150, y=300, width = 190, height = 50)


delete_point = Button(root, text = "Удалить данную точку", fg='red', command=delete_point)
delete_point.place(x =  1150, y=200, width = 190, height = 50)

button_calculate= Button(root, text="Найти треугольник", fg='red', command = func)
button_calculate.place(x=930, y=40, width=190, height = 50)

button_clear= Button(root, text="Очистить поле",fg='red', command=delete)
button_clear.place(x = 20, y = 750, width=190, height = 50)

def schedule():
    canvas.create_line(400, 800, 400, 0, fill='black',
                    width=2, arrow=LAST,
                    arrowshape="10 20 10")
    canvas.create_line(0, 400, 800, 400, fill='black',
                    width=2, arrow=LAST,
                    arrowshape="10 20 10")
    for i in range(50, 800, 50):
        if i == 400:
            canvas.create_text(385, 385 , text=400 - i,
                               justify=CENTER)
            continue

        canvas.create_line(0, i, 800, i, fill='white',width=2)
        canvas.create_line(i, 0, i, 800, fill='white', width=2)
        canvas.create_line(i, 395, i, 405, fill='black', width=2)
        canvas.create_line(395, i, 405, i, fill='black', width=2)
        canvas.create_text(i, 420, text= i - 400, justify=CENTER)
        canvas.create_text(420, i , text= 400 - i, justify=CENTER)

def paint_point(a):
    canvas.create_oval(a[0] - radius_point + 400, fabs(a[1] - radius_point - 400),
                     a[0] + radius_point + 400, fabs(a[1] + radius_point - 400),
                     width=2, fill='red', outline='black')


def paint_line(a, b):
    canvas.create_line(a[0] + 400, fabs(a[1] - 400), b[0] +
                     400, fabs(b[1] - 400), fill="black", width=2)


def show_result(x1, y1, x2, y2, x3, y3, array_with_points_inside):
    canvas.delete(ALL)
    # Рисуем координатные оси.
    canvas.create_line(0, 400, 800, 400, fill="gray", width=2, arrow=LAST,
                     arrowshape="10 20 10")
    canvas.create_line(400, 0, 400, 800, fill="gray", width=2, arrow=FIRST,
                     arrowshape="10 20 10")

    # Делаем рисонок больше.
    p_copy = [x1, y1, x2, y2, x3, y3]
    p = [x1, y1, x2, y2, x3, y3, 0, 0]
    name_point = ["A", "B", "C"]
    max_x = p[0]
    max_y = p[1]

    for i in range(0, len(p), 2):
        if fabs(p[i]) > fabs(max_x):
            max_x = p[i]
        if fabs(p[i + 1]) > fabs(max_y):
            max_y = p[i + 1]
    if fabs(max_x) > fabs(max_y):
        maximum = max_x
    else:
        maximum = max_y

    coefficient = fabs((max_coordinate - 140) / maximum)


    if coefficient == 0:
        coefficient = 1

    for i in range(len(p)):
        p[i] *= coefficient

    for i in range(len(array_with_points_inside)):
        array_with_points_inside[i] *= coefficient



    for i in range(0, 6, 2):
        paint_point((p[i], p[i + 1]))

        canvas.create_text(p[i] + 330, fabs(p[i + 1] - 400),
            text = name_point[int(i / 2)] + "(" + str(round(p_copy[i], 2)) +
            ";" + str(round(p_copy[i + 1], 2)) + ")",
            font="Verdana 12", fill="red")



    for i in range(0, len(array_with_points_inside), 2):
        #print("{} {}".format(array_with_points_inside[i], array_with_points_inside[i + 1]))
        paint_point((array_with_points_inside[i], array_with_points_inside[i + 1]))

    paint_line((p[0], p[1]), (p[2], p[3]))
    paint_line((p[0], p[1]), (p[4], p[5]))
    paint_line((p[2], p[3]), (p[4], p[5]))

    paint_line((p[0],p[1]), ((p[2] + p[4]) / 2, (p[3] + p[5]) / 2))

    paint_line((p[2], p[3]), ((p[0] + p[4]) / 2, (p[1] + p[5]) / 2))

    paint_line((p[4], p[5]), ((p[0] + p[2]) / 2, (p[1] + p[3]) / 2))



schedule()

#draw_from_file()

messagebox.showinfo("Инструкция", "Построить треугольник,\nу которого разность максимального\nи минимального кол-ва точек, попавших в каждый из 6 -ти\n треугольников, образованных пересечением медиан,\nмаксимальна")

root.mainloop()
