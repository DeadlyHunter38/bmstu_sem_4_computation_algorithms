from math import pow

class Differentiation:
    def __init__(self, x, y, h):
        """
        Конструктор
        """
        self.h = h
        self.x = x
        self.y = y
        self._len_x = len(x)
        self._len_y = len(y)
        self.diff_y_1 = [0 for i in range (self._len_x)]
        self.diff_y_2 = [0 for i in range (self._len_x)]
        self.diff_y_3 = [0 for i in range (self._len_x)]
        self.diff_y_4 = [0 for i in range (self._len_x)]
        self.diff_y_5 = [0 for i in range (self._len_x)]

    def calculate_diffenrece(self):
        self.left_differnece()
        self.center_diffenerce()
        self.second_runge_diffenrence(1)
        self.aligned_variable()
        self.second_left_diffenrece()

    def left_differnece(self):
        """
        Левая разностная производная
        """
        self.diff_y_1[0] = 0
        for i in range(1, self._len_y):
            self.diff_y_1[i] = (self.y[i] - self.y[i - 1]) / self.h

    def center_diffenerce(self):
        """
        Центральная разностная производная
        """
        self.diff_y_2[0] = self.diff_y_2[-1] = 0
        for i in range(1, self._len_y - 1):
            self.diff_y_2[i] = (self.y[i + 1] - self.y[i - 1]) / 2 * self.h

    def second_runge_diffenrence(self, p):
        """
        Вторая формула Рунге с использованием односторонней производной
        """
        y_temp = [0, 0]
        for i in range(2, self._len_y):
            y_temp.append((self.y[i] - self.y[i - 2]) / (2 / self.h))
        
        self.diff_y_3[0] = self.diff_y_3[1] = 0
        for i in range(2, len(self.diff_y_1)):
            self.diff_y_3[i] = self.diff_y_1[i] + (self.diff_y_1[i] - y_temp[i]) / (pow(2, p) - 1)
        
    def aligned_variable(self):
        """
        Выравнивающие переменные
        """
        for i in range(self._len_y - 1):
            k = pow(self.y[i], 2) / pow(self.x[i], 2)
            self.diff_y_4[i] = k * (((-1 / self.y[i + 1]) - (-1 / self.y[i])) / ((-1 / self.x[i + 1]) - (-1 / self.x[i])))
        self.diff_y_4[-1] = 0

    def second_left_diffenrece(self):
        """
        Вторая одностороняя производная (левая)
        """
        self.diff_y_5[0] = self.diff_y_5[-1] = 0
        for i in range(1, self._len_y - 1):
            self.diff_y_5[i] = (self.y[i - 1] - 2 * self.y[i] + self.y[i + 1]) / pow(self.h, 2)

    def output(self):
        """
        Вывод таблицы производных на экран
        """
        print("  x   |   y   |     1    |     2    |     3    |     4    |     5")
        print("-" * 70)
        for i in range(self._len_x):
            print("   {0}  |{1:7.3f}|{2:10.3f}|{3:10.3f}|{4:10.3f}|{5:10.3f}|{6:10.3f}". format(self.x[i], self.y[i], \
                    self.diff_y_1[i],  self.diff_y_2[i], self.diff_y_3[i], self.diff_y_4[i], self.diff_y_5[i]))



if __name__ == "__main__":
    h = 1
    x = [1, 2, 3, 4, 5, 6]
    y = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
    object = Differentiation(x, y, h)
    object.calculate_diffenrece()
    object.output()
