from enum import Enum
from Utils import *

""" Перечисление ячеек поля"""


class Field(Enum):
    VOID = 0,  # пустая клетка
    WALL = 1,  # стена
    BOX = 2,  # коробка


""" Класс точки """


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    # метод сравнения точек
    def equals(self, p):
        if self._x == p._x and self._y == p._y:
            return True
        else:
            return False


class SokobanGame:
    def __init__(self):
        self.now_point = None  # хранит координаты игрока
        self.finish_points = []  # хранит финишные точки поля (куда надо поставить коробку)
        self.fields = None  # игровое поле
        self.was_moved_box = None  # двигали ли коробку

    """Создаём новый уровень игры. Считываем с файла поле, точки. 
    Создаём поле, расставляем на нём игрока, точки, коробки"""

    def new_level(self, path):
        file_level = open(path, 'r')
        height = count_lines_in_file(path)
        width = count_words_in_line(path)

        self.fields = [[0] * width for _ in range(height)]

        """ 0 - пустая клетка
            1 - стена
            2 - коробка
            3 - коробка, которая уже стоит на точке
            4 - спавн игрока
            5 - точка
            6 - спавн игрока + точка """

        for i in range(height):
            for j in range(width):
                v = file_level.read(2)
                v = v.strip()
                if int(v) == 4:
                    self.now_point = Point(i, j)
                    self.fields[i][j] = Field.VOID
                elif int(v) == 6:
                    self.now_point = Point(i, j)
                    self.fields[i][j] = Field.VOID
                    self.finish_points.append(Point(i, j))
                elif int(v) == 5:
                    self.finish_points.append(Point(i, j))
                    self.fields[i][j] = Field.VOID
                elif int(v) == 3:
                    self.fields[i][j] = Field.BOX
                    self.finish_points.append(Point(i, j))
                else:
                    self.fields[i][j] = self.convert_to_field(v)

        file_level.close()

    """ Перемещение игрока. """

    def move(self, dx, dy):
        if dx != 0:
            if self.fields[self.now_point.get_x() + dx][self.now_point.get_y()] == Field.VOID:
                self.now_point.set_x(self.now_point.get_x() + dx)
                self.was_moved_box = False
            else:
                if (self.in_range(self.now_point.get_x() + 2 * dx, 0, len(self.fields)) and
                        self.fields[self.now_point.get_x() + dx][self.now_point.get_y()] == Field.BOX and
                        self.fields[self.now_point.get_x() + 2 * dx][self.now_point.get_y()] == Field.VOID):
                    self.fields[self.now_point.get_x() + dx][self.now_point.get_y()] = Field.VOID
                    self.fields[self.now_point.get_x() + 2 * dx][self.now_point.get_y()] = Field.BOX
                    self.now_point.set_x(self.now_point.get_x() + dx)
                    self.was_moved_box = True
        elif dy != 0:
            if self.fields[self.now_point.get_x()][self.now_point.get_y() + dy] == Field.VOID:
                self.now_point.set_y(self.now_point.get_y() + dy)
                self.was_moved_box = False
            else:
                if (self.in_range(self.now_point.get_y() + 2 * dy, 0, len(self.fields)) and
                        self.fields[self.now_point.get_x()][self.now_point.get_y() + dy] == Field.BOX and
                        self.fields[self.now_point.get_x()][self.now_point.get_y() + 2 * dy] == Field.VOID):
                    self.fields[self.now_point.get_x()][self.now_point.get_y() + dy] = Field.VOID
                    self.fields[self.now_point.get_x()][self.now_point.get_y() + 2 * dy] = Field.BOX
                    self.now_point.set_y(self.now_point.get_y() + dy)
                    self.was_moved_box = True

    """ Проверка: стоит ли коробка на финишной точке. """

    def is_finish_point(self, x, y):
        for p in range(len(self.finish_points)):
            if self.finish_points[p].get_x() == x and self.finish_points[p].get_y() == y:
                return True
        return False

    """ Проверка окончания игры. """

    def is_win(self):
        for i in range(len(self.fields)):
            for j in range(len(self.fields[i])):
                if self.fields[i][j] == Field.BOX and not self.is_finish_point(i, j):
                    return False
        return True

    """ Получение поля игры. """

    def get_field(self, x, y):
        return self.fields[x][y]

    """ Конвертирование числа в элемент перечисления поля """

    @staticmethod
    def convert_to_field(x):
        if int(x) == 0:
            return Field.VOID
        elif int(x) == 1:
            return Field.WALL
        else:
            return Field.BOX

    """ Конвертирования поля в число """

    @staticmethod
    def convert_to_int(f):
        if f == Field.VOID:
            return 0
        elif f == Field.WALL:
            return 1
        else:
            return 2

    """ Проверка на предел """

    @staticmethod
    def in_range(x, a, b):
        if (x > a) and (x < b):
            return True
        else:
            return False

    """ Получить высоту """

    def get_height(self):
        return len(self.fields)

    """ Получить ширину """

    def get_width(self):
        return len(self.fields[0])

    """ Запуск новой игры """

    def new_game(self, path):
        self.new_level(path)
