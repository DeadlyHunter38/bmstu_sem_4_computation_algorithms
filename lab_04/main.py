import sys
import matplotlib.pyplot as plt
import numpy as np

MIN_ITEM_MENU = '0'; MAX_ITEM_MENU = '4'


def print_menu():
    print('Меню:\n' + 
         '1. Загрузить данные из файла.\n' + 
         '2. Вывести таблицу.\n' +
         '3. Найти решение.\n' + 
         '4. Изменить вес точки.\n' +
         '0. Выйти из программы.\n')

def input_menu_item():
    menu_choice = ''
    print(f"Введите пункт меню: ", end='')
    menu_choice = input()
    while menu_choice < MIN_ITEM_MENU or menu_choice > MAX_ITEM_MENU:
        print(f"Некорректный пункт меню. Введите еще раз: ", end='')
        menu_choice = input()
    return menu_choice

def choose_menu_item(menu_choice, data, data_2, polynom_coeffs_a, a_equal_mass):
    if menu_choice == '1':
        file_name_1 = 'data.txt'
        file_name_2 = 'data_2.txt'
        data = read_data_from_file(file_name_1)
        data_2 = read_data_from_file(file_name_2)
        print(f"\nДанные загружены успешно.\n")
    elif menu_choice == '2':
        print_data(data)
    elif menu_choice == '3':
        degree_polynom = input_polynom_degree()
        polynom_coeffs_a = find_root(data, degree_polynom)
        a_equal_mass = find_root(data_2, degree_polynom)
        create_graph(data, polynom_coeffs_a, a_equal_mass, degree_polynom)
    elif menu_choice == '4': 
        data = change_mass_point(data)
        print(f"Изменение прошло успешно.\n")
    return data, data_2, polynom_coeffs_a, a_equal_mass

def read_data_from_file(file_name):
    file = open(file_name, 'r')

    #считывание х, у, p из файла
    data = [line.replace("\n", "").split() for line in file]
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            data[i][j] = int(data[i][j])

    return data

def print_data(data):
    if (data == []):
        print(f"Ошибка: данные еще не загружены.")
    else:
        print(f"x | y | p\n" +
                "----------")
        for i in range(len(data)):
            print(f"{data[i][0]} | {data[i][1]} | {data[i][2]}")

def create_graph(data, a, a_equal_mass, degree_polynom):
    dx = 10
    if (len(data) > 1):
        dx = data[1][0] - data[0][0]
        
    x = np.linspace(data[0][0] - dx, data[-1][0] + dx, 100)
    y = []
    for i in x:
        temp_value_y = 0
        for j in range(0, degree_polynom + 1):
            temp_value_y += f(i, j) * a[j]
        y.append(temp_value_y)
    plt.plot(x, y, label='разные веса точек')

    x = np.linspace(data[0][0] - dx, data[-1][0] + dx, 100)
    y = []
    for i in x:
        temp_value_y = 0
        for j in range(0, degree_polynom + 1):
            temp_value_y += f(i, j) * a_equal_mass[j]
        y.append(temp_value_y)
    plt.plot(x, y, label='одинаковые веса точек')

    x_table = [a[0] for a in data]
    y_table = [a[1] for a in data]

    plt.plot(x_table, y_table, 'ro', color='red', label='таблица')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend(loc = 'best')

    plt.show()

def f(x, n):
    return x ** n

def change_mass_point(data):
    if (data == []):
        print(f"Ошибка: данные еще не загружены.")
    else:
        i_change = input_index_change()
        new_mass = input_new_mass(data)
        change_mass_value(data[i_change], new_mass)
    return data

def input_index_change():
    print(f"Введите индекс элемента, который хоите изменить: ", end='')
    index_change = input()
    while index_change < '0' or index_change > '6':
        print(f"Некорректный пункт меню. Введите еще раз: ", end='')
        index_change = input()
    return int(index_change)

def input_new_mass(data):
    flag_is_digit = 0
    while flag_is_digit == 0:
        print(f"Введите новый вес: ", end='')
        new_mass = input()
        flag_is_digit = check_is_digit(new_mass)
        if flag_is_digit == 0:
            print(f"Некорректное значение.", end=' ')

    return new_mass

def check_is_digit(new_mass):
    flag_is_digit = False
    if new_mass.isdigit():
        flag_is_digit = True
    return flag_is_digit

def change_mass_value(point_change, new_mass):
    point_change[2] = int(new_mass)

def find_root(data, degree_polynom):
    if data == []:
        print(f"Ошибка: данные еще не загружены.")
    else:
        matrix, column = create_slau_matrix(data, degree_polynom)
        append_column_of_free_members(matrix, column)
        solve_matrix_by_gauss(matrix)
        a = find_polynomial_coeffs(matrix)
    return a

def create_slau_matrix(data, degree_polynom):
    len_data = len(data)
    matrix = [[0 for i in range(0, degree_polynom + 1)] for j in range (0, degree_polynom + 1)]
    column = [0 for i in range(0, degree_polynom + 1)]
    for m in range(0, degree_polynom + 1):
        for i in range(0, len_data):
            temp_value = data[i][2] * f(data[i][0], m)
            for k in range(0, degree_polynom + 1):
                matrix[m][k] += temp_value * f(data[i][0], k)
            column[m] += temp_value * data[i][1]
    return matrix, column 

def append_column_of_free_members(matrix, column):
    for i in range(len(column)):
        matrix[i].append(column[i])

def solve_matrix_by_gauss(matrix):
    len_matrix = len(matrix)
    for i in range(len_matrix):
        for j in range(i + 1, len_matrix):
            coeff = -(matrix[j][i] / matrix[i][i])
            for k in range(i, len_matrix + 1):
                matrix[j][k] += coeff * matrix[i][k]

def find_polynomial_coeffs(matrix_x_degree):
    len_matrix = len(matrix_x_degree)
    a = [0 for i in range(len_matrix)]
    for i in range(len_matrix - 1, -1, -1):
        for j in range(len_matrix - 1, i, -1):
            matrix_x_degree[i][len_matrix] -= a[j] * matrix_x_degree[i][j]
        a[i] = matrix_x_degree[i][len_matrix] / matrix_x_degree[i][i]
    return a
    
def input_polynom_degree():
    print(f"Введите степень полинома (от 0 до 6): ", end='')
    degree_polynom = input()
    while degree_polynom < '0':
        print(f"Некорректный ввод. Введите еще раз: ", end='')
        degree_polynom = input()
    return int(degree_polynom) 

def main():
    menu_choice = -1
    data = []; data_2 = []
    polynom_coeffs_a = []; a_equal_mass = []
    while menu_choice != '0':
        print_menu()
        menu_choice = input_menu_item()
        data, data_2, polynom_coeffs_a, a_equal_mass = choose_menu_item(menu_choice, data, data_2, polynom_coeffs_a, a_equal_mass)

if __name__ == "__main__":
    main()