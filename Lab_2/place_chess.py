from typing import Generator

# Функция для вывода нынешнего состояния доски: "#" - фигура, "0" - свободная клетка, '*' - клетка под боем(число указывает сколько фигур бьют на эту клетку)
def print_field(field: list[list[int]]) -> None:
    for i in range(side):
        for j in field[i]:
            if j==-1:
                print('#', sep='', end=' ')
            elif j>0:
                print('*', sep='', end=' ')
            else:
                print('0', sep='', end=' ')
        print()
    print('-' * (2 * len(field[0]) - 1))

# Генератор, отсекающий ходы фигуры, выходящие за рамки игрового поля
def figure_moves(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for i in ((x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1), (x, y + 2), (x, y - 2), (x - 2, y), (x + 2, y)):
        if not (i[0] > side - 1 or i[1] > side - 1 or i[0] < 0 or i[1] < 0):
            yield i

# Функция, ставящая фигуру на указанную клетку
def place_figure(x: int, y: int, field: list[list[int]])-> list[list[int]]:
    # Расстановка клеток боя на поле
    for i in figure_moves(x, y):
        field[i[1]][i[0]] += 1
    # Ставим саму фигуру
    field[y][x] = -1
    return field

# Функция, убирающая фигуру с указанной клетки
def remove_figure(x: int, y: int, field: list[list[int]]) -> list[list[int]]:
    # Убираем бой этой фигуры с тех клеток, на которых он был
    for i in figure_moves(x, y):
        field[i[1]][i[0]] -= 1
    # Убираем саму фигуру
    field[y][x] = 0
    return field

# Рекуррентная функция, с точкой остановки "Все дополнительные фигуры поставлены"
def recursion(place: int, current_pos: int, field: list[list[int]], figures:list = [])-> None:

    # Точка остановки, если нам не нужно больше ставить фигуры на поле, мы записываем нынешнюю расстановку в файл и выходим из этой ветки рекурсии
    if place==0:
        # Здесь мы выводим удачные расстановки в консоль, по умолчанию закоментированно для большей оптимизации
        print_field(field)
        file.write(",".join(map(str, const_figures + figures)) + '\n')
        return

    # Тело рекурсии
    else:

        # Представляем нашу шахматную доску в виде последовательности клеток, избавляясь от двумерности. Идти по доске мы начинаем с "Нулевой позиции"
        for pos in range(current_pos, side ** 2):

            #Если мы находим пустую клетку, то ставим на неё фигуру, записываем её местоположение, меняем значение "Нулевой позиции" на следующую клетку после той, на которую мы поставили фигуру
            if field[pos // side][pos % side] == 0:
                field = place_figure(pos % side, pos // side, field)
                figures.append((pos % side, pos // side))
                recursion(place - 1, pos + 1, field, figures)

                # По достижению точки остановки мы возвращаемся сюда и переходим в другую ветку, снимая поставленную ранее на эту клетку фигуру
                figures.pop(len(figures) - 1)
                field = remove_figure(pos % side, pos // side, field)
               

# Объявление глобальных переменных. 1)side - Сторона поля 2)file - Само шахматное поле 3)const_figures - Фигуры, которые я не могу двигать
global side
global file
global const_figures
const_figures: list = list()
    
# Считывание данных из файла
with open('input.txt','r') as f:
    side, place, field_side = map(int, f.readline().split())

    # Генерация поля, расстановка фигур из файла
    field: list[list[int]] = [[0] * side for i in range(side)]
    for i in range(field_side):
        x, y = map(int, f.readline().split())
        const_figures.append((x, y))
        field: list[list[int]] = place_figure(x, y, field)
#Запуск рекурсии, запись всех возможных расстановок в файл
file = open("output.txt", 'w')
recursion(place, 0, field)
file.close()

#Вывод no solutions в файл если нет решений
with open("output.txt",'r') as f:
    file = f.readlines()
    if len(file) == 0:
        with open("output.txt", 'w') as f:
            f.write('no solutions')