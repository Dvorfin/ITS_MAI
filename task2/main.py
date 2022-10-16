

def triangle(a):
    if (a - int(a) != 0) or (a <= 0): # check float and <= 0
        print('incorrect input!')
    else:
        for i in range(0, a+2):
            print(' '*(a+1-i) + '*'*i + '*'*(i-1))


def hist_distance(hist1, hist2): 
    d = 0
    if (len(hist1) == len(hist2)): # проверка на совпадение размерности гистограмм
        for i in range(10):
            d += (hist2[i] - hist1[i])**2
        # print("(" + str(hist2[i]) + " - " + str(hist1[i]) + ")^2 = " + str((hist2[i] - hist1[i])**2) )
        return d**0.5
    else:
        print('sizes of hist are different!')


def write_to_file(file_name, input_lst): # функция записи в файл
    file = open(file_name, 'w') # ключ на запись
    for i in range(len(input_lst)): 
        if (i == (len(input_lst) - 1)): # не записываем пробел после последнего символа
            file.write(str(input_lst[i]))
        else:
            file.write(str(input_lst[i]) + ' ')
    file.close()


def read_from_file(file_name): # функция чтения из файла
    file = open(file_name, 'r')
    content = file.readline()
    file.close()
    content = content.split(' ')  #разделяем строку по пробелам в список
    return list(map(int, content))  #преобразуем в список интов


def main():
    # тесты задания 1
    triangle(3)
    triangle(5)
    triangle(-5)
    triangle(-5.5)
    triangle(5.2)

    # тест задания 2
    hist1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hist2 = [3, 5, 8, 4, 9, 6, 7, 15, 6, 4]
    print(round(hist_distance(hist1, hist2), 4))

    # тест задания 3 и 4
    write_to_file("hist_info.txt", hist1)
    content = read_from_file("hist_info.txt")
    print(f'content from file: {content}')


if __name__ == '__main__':
    main()
    
    