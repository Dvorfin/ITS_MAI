#  Разработать функцию для определения класса к
# которому относится объект, определенный при помощи
# гистограммы при помощи метода ближайших соседей

# 1) создать три класа хранения изображений: чб, фиолетового, голубого
# 2) создать метод рандомного создания изображения в каждом из классов
# 3) создать класс генерации одного изображения, которое будет относиться либо
#     к одному из трех, либо случайным
# 4) применить гистограмму
# self.blank_image[0:self.height, 0:self.width] = (self.B, self.G, self.R) # B G R
import numpy as np
import cv2 as cv
import random


class GrayImg:  # класс создания чб изображения

    def __init__(self):
        self.height = 200
        self.width = 200
        # создаетсся двумерный массив изображения глубиной три пикселя
        self.blank_image = np.zeros((self.height, self.width, 3), np.uint8)

        for i in range(self.height):  # массив заполняется случайными значениями
            for j in range(self.width):
                self.R = random.randint(80, 170)
                self.G = self.R
                self.B = self.R
                self.blank_image[i, j] = (self.B, self.G, self.R)  # (B, G, R)
        # к изображению применяется размытие гаусса kernel = (11, 11), sigma = 50
        self.blank_image = cv.GaussianBlur(self.blank_image, (11, 11), 50)

    def show_img(self):  # метод вывода изображения
        cv.imshow('gray_img', self.blank_image)
        cv.waitKey(0)

    def get_info(self, n, m, k):       # метод получения значений B G R для пикселя (n, m)
        return self.blank_image.item((n, m, k))


class PurpleImg:

    def __init__(self):
        self.height = 200
        self.width = 200

        self.blank_image = np.zeros((self.height, self.width, 3), np.uint8)

        for i in range(self.height):
            for j in range(self.width):
                self.R = random.randint(100, 150)
                self.G = random.randint(0, 20)
                self.B = random.randint(200, 250)
                self.blank_image[i, j] = (self.B, self.G, self.R)  # (B, G, R)

        self.blank_image = cv.GaussianBlur(self.blank_image, (11, 11), 50)

    def show_img(self):
        cv.imshow('purple_img', self.blank_image)
        cv.waitKey(0)

    def get_info(self, n, m, k):
        return self.blank_image.item((n, m, k))


class BlueImg:

    def __init__(self):
        self.height = 200
        self.width = 200

        self.blank_image = np.zeros((self.height, self.width, 3), np.uint8)

        for i in range(self.height):
            for j in range(self.width):
                self.R = random.randint(0, 50)
                self.G = random.randint(0, 50)
                self.B = random.randint(180, 250)
                self.blank_image[i, j] = (self.B, self.G, self.R)  # (B, G, R)

        self.blank_image = cv.GaussianBlur(self.blank_image, (11, 11), 50)

    def show_img(self):
        cv.imshow('blue_img', self.blank_image)
        cv.waitKey(0)

    def get_info(self, n, m, k):
        return self.blank_image.item((n, m, k))


class RandImg:

    def __init__(self):
        self.height = 200
        self.width = 200

        self.blank_image = np.zeros((self.height, self.width, 3), np.uint8)

        for i in range(self.height):
            for j in range(self.width):
                self.R = random.randint(0, 255)
                self.G = random.randint(0, 255)
                self.B = random.randint(0, 255)
                self.blank_image[i, j] = (self.B, self.G, self.R)  # (B, G, R)

        self.blank_image = cv.GaussianBlur(self.blank_image, (3, 3), 15)

    def show_img(self):
        cv.imshow('rand_img', self.blank_image)
        cv.waitKey(0)

    def get_info(self, n, m, k):
        return self.blank_image.item((n, m, k))


def calc_hist(data):  # вычисление гистограммы

    hist = [0]*255  # гистограмма цветов 0-255
    for n in range(200):    # итерируемся по пискселям
        for m in range(200):
            for k in range(3):  # проверяем B G R составляющую пикселя
                t = data.get_info(n, m, k)  # получаем значение B G R
                hist[t] = hist[t] + 1       # увличиваем полученный цвет
    return hist


def hist_distance(hist1, hist2):  # вычисление расстояний между гистограммами
    d = 0
    if len(hist1) == len(hist2):  # проверка на совпадение размерности гистограмм
        for i in range(len(hist1)):
            d += (hist2[i] - hist1[i])**2
        return d**0.5
    else:
        print('sizes of hist are different!')


def analyze_class(rnd):  # функция анализа класса, к которому относится объект
    purple = []  # списки объектов классов
    gray = []
    blue = []

    purple_hist = []  # списки гистограмм объектов классов
    gray_hist = []
    blue_hist = []

    rnd_hist = calc_hist(rnd)  # гистограмма поданного объекта

    for i in range(4):  # создаем по 4 объекта классов и для каждого вычисляется гистограмма
        purple.append(PurpleImg())
        gray.append(GrayImg())
        blue.append(BlueImg())

        purple_hist.append(calc_hist(purple[i]))
        gray_hist.append(calc_hist(gray[i]))
        blue_hist.append(calc_hist(blue[i]))

    prev_min_dist = 100000.0
    for i in range(4):  # вычисляем расстояние между случайным изображением и другими
        d1 = round(hist_distance(purple_hist[i], rnd_hist), 3)
        d2 = round(hist_distance(gray_hist[i], rnd_hist), 3)
        d3 = round(hist_distance(blue_hist[i], rnd_hist), 3)

        dict_class_dist = {'purple': d1, 'gray': d2, 'blue': d3}  # помещаем в словрь {имя класса : расстояние до него}

        min_dist = min(d1, d2, d3)  # минимальное расстояние

        print(f'purple: {d1} gray: {d2} blue: {d3} min_dist: {min_dist}')

        for key, value in dict_class_dist.items():  # итерируемся по словарю и находим минимальное расстояние
            if min_dist == value:                   # проверяем с каким ключом свопало минимальное расстояние
                if min_dist <= prev_min_dist:       # если это минимальное расстояние меньше предыдущего минимального
                    wich_class = key                # то запоминаем название класса
                    prev_min_dist = min_dist        # обновляем предыдущее минимальное

    print(f'Object relates to class {wich_class}')  # возвращаем название класса, к которому относится объект


def foo():  # функция чисто для тестов 
    height = 200
    width = 200
    blank_image = np.zeros((height, width, 3), np.uint8)

    for i in range(height):
        for j in range(width):
            R = random.randint(0, 255)
            # G = random.randint(10, 50)
            # B = random.randint(0, 255)
            G = R
            B = R
            blank_image[i, j] = (B, G, R)  # (B, G, R)

    blank_image = cv.GaussianBlur(blank_image, (11, 11), 50)

    print(blank_image[10, 45])
    spl = blank_image.item((10, 45, 2))
    print(spl)
    cv.waitKey(0)


def main():
    rnd = RandImg()
    analyze_class(rnd)

if __name__ == '__main__':
    main()



