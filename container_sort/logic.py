from objects import Noisy
from objects import file_path
from random import randint
import os
from time import sleep

def clear_console():
    os.environ['TERM'] = 'xterm'
    os.system('cls' if os.name == 'nt' else 'clear')

def print_exception(text):
    clear_console()
    print(text)
    sleep(2)
    clear_console()

def is_sorted(stacks):
    if any(any(str(container) != str(container.nxt) and container.nxt is not None for container in stack) for stack in stacks):
        return False
    return True

def numerate_stacks(stacks): # Нумерует стеки, нумерация нужна стеку для вывода
    for i, stack in enumerate(stacks):
        stack.stack_id = str(i + 1)

def sort_containers(stacks, types):
    with open(file_path, "w") as _:
        pass

    if is_sorted(stacks):
        # print("> Контейнеры уже отсортированы!")
        return

    if len(stacks) == 2: # Большинство стопок длины 2 c двумя видами контейнеров невозможно отсортировать, за исключением стопок вида: Стек 1: 2 1 1 Стек 2: 1, эта часть кода разбирается с такими ситуациями, а если не может, то так и пишет
        with Noisy():

            numerate_stacks(stacks)
            top = str(stacks[0].top)
            for container in stacks[0]:
                if str(container) == top:
                    stacks[0].move(stacks[1])
                else:
                    break
            if is_sorted(stacks):
                return
            top = str(stacks[1].top)
            for container in stacks[1]:
                if str(container) == top:
                    stacks[1].move(stacks[0])
                else:
                    break
            if is_sorted(stacks):
                return
            else:
                #print_exception("================================================================\n"
                #                "| Контейнеры невозможно отсортировать, перезапуск программы    |\n"
                #                "================================================================\n")
                print_exception("0")
                return

    types_c = types.copy()
    types = sorted(types_c, key=lambda digit : int(digit))
    list_pos = {types[i] : i for i in range(len(types))}
    matching = (len(stacks) == len(types))
    numerate_stacks(stacks)

    dump = len(types) - 1 if matching else len(types) # Индекс мусорки
    second_dump = 0 # Вторая мусорка для ситуации len(types) = len(stacks)

    with Noisy():
        for i in range(len(stacks) - 1): # Собираем контейнеры со всех стопок и засовываем в мусорку
            stacks[dump] += stacks[i]
            stacks[i].top = None
        stacks = stacks[0:dump+1]

        if not matching:
            for container in stacks[dump]: # Просто разгружаем мусорку по стопкам, место куда поставить контейнер найдётся всегда
                where = list_pos[str(container)]
                stacks[dump].move(stacks[where])
        else:
            for container in stacks[dump]: # Разгружаем то, что можем распределить из мусорки, если не можем распределить (контейнер должен быть в мусорке, но мы не можем его там оставить т.к под ним ещё неотсортированные контейнеры), то разгружаем во 2-ую мусорку
                where = list_pos[str(container)]
                where = second_dump if where == dump else where
                stacks[dump].move(stacks[where])

            sorted_stack = randint(second_dump + 1, dump - 1) # После предыдущего этапа между мусоркой и 2-ой мусоркой должны появится отсортированные контейнеры, берём любой
            for container in stacks[second_dump]: # Разгружаем то, что можем распределить из 2-ой мусорки, если не можем распределить, то разгружаем в отсортированный стек
                where = list_pos[str(container)]
                where = sorted_stack if where == second_dump else where
                stacks[second_dump].move(stacks[where])

            for container in stacks[sorted_stack]: # Разгружаем из отсортированного стека все элементы принадлежащие 2-ой мусорке
                if list_pos[str(container)] == second_dump:
                    stacks[sorted_stack].move(stacks[second_dump])
                else:
                    break
    clear_console()