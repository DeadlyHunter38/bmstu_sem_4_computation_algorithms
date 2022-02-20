import numpy as np
import matplotlib.pyplot as plt

def f(x, n):
    return x ** n

def readfile(data, filename):
    f = open(filename, 'r')
    linecount = 0
    for line in f:
        linecount += 1
        line = line.split()
        x = float(line[0])
        y = float(line[1])
        p = float(line[2])
        data.append([x, y, p])
    f.close()
    return linecount

# Создание матрицы
def get_slau_matrix(table, n):
    N = len(table)
    matrix = [[0 for i in range(0, n + 1)] for j in range (0, n + 1)]
    col = [0 for i in range(0, n + 1)]

    for m in range(0, n + 1):
        for i in range(0, N):
            tmp = table[i][2] * f(table[i][0], m)
            for k in range(0, n + 1):
                matrix[m][k] += tmp * f(table[i][0], k)
            col[m] += tmp * table[i][1]
    return matrix, col    


def Gauss(matr):
    n = len(matr)
    for k in range(n):
        for i in range(k+1,n):
            coeff = -(matr[i][k]/matr[k][k])
            for j in range(k,n+1):
                matr[i][j] += coeff*matr[k][j]
    a = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):
            matr[i][n] -= a[j]*matr[i][j]
        a[i] = matr[i][n] / matr[i][i]
    return a

def get_approx_coef(table, n):

    m, z = get_slau_matrix(table, n)
    print(f"m = {m}")

    for i in range(len(z)):
        m[i].append(z[i])
    
    print(f"m = {m}")
    a_array = Gauss(m)
    print(f"a_array = {a_array}")
    return a_array

# Вывод графика аппроксимирующей функции и исходных точек
def print_result(table, A, b, n):
    dx = 10
    if len(table) > 1:
        dx = (table[1][0] - table[0][0])
   
    x = np.linspace(table[0][0] - dx, table[-1][0] + dx, 100)
    y = []
    print(f"A = {A}")
    print(f"b = {b}")
    for i in x:
        tmp = 0;
        for j in range(0, n + 1):
            tmp += f(i, j) * A[j]
        y.append(tmp)

    print(f"x = {x}")
    print(f"y = {y}")

    plt.plot(x, y)
    
    x = np.linspace(table[0][0] - dx, table[-1][0] + dx, 100)
    y = []
    for i in x:
        tmp = 0;
        for j in range(0, n + 1):
            tmp += f(i, j) * b[j]
        y.append(tmp)

    print(f"x = {x}")
    print(f"y = {y}")

    #plt.plot(x, y)
    
    

    x1 = [a[0] for a in table]
    y1 = [a[1] for a in table]

    print(f"x1 = {x1}")
    print(f"y1 = {y1}")


    plt.plot(x1, y1, 'kD', color = 'red', label = '$таблица$')
    plt.grid(True)
    plt.legend(loc = 'best')
    miny = min(min(y), min(y1))
    maxy = max(max(y), max(y1))
    dy = (maxy - miny) * 0.03
    plt.axis([table[0][0] - dx, table[-1][0] + dx, miny - dy, maxy + dy])

    plt.show()
    return 

data = []
data2 = []
readfile(data, "lab4.txt")
readfile(data2, "lab4_2.txt")
n = int(input("Введите степень полинома n = "))
A = get_approx_coef(data, n)
b = get_approx_coef(data2, n)

print_result(data, A, b, n)