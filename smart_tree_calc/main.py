import os
from time import sleep
from objects import CalcTree

def clear_console():
    os.environ['TERM'] = 'xterm'
    os.system('cls' if os.name == 'nt' else 'clear')

def print_exception(text):
    clear_console()
    print(text)
    sleep(2)
    clear_console()

def input_variables(detected_vars):
    """Вспомогательная функция для интерактивного ввода переменных"""
    variables = {}
    if not detected_vars:
        return variables

    print("================================================================\n"
          "| Программа обнаружила переменные. Введите их числовые         |\n"
          "| значения для производства вычислений.                        |\n"
          "================================================================")
    for var in sorted(detected_vars):
        while True:
            try:
                val = input(f"> Введите значение для переменной '{var}': ").strip()
                # Переводим в float для поддержки как целых, так и дробных чисел
                variables[var] = float(val)
                break
            except ValueError:
                print("| Ошибка! Значение должно быть числом. Попробуйте еще раз.")
    return variables


print(
    fr"""
 ＿＿＿
//￣￣＼＼                  ／＞   フ Z
\\      \\      ＿＿＿＿＿＿|  n  n l z  
 ＼＼   //   ／            ヽ` ミ＿ωノ ~  (Спасибо что используете tree calc!)
   \/  \\ /             )       /       
       \\  ／＿_  ヽ     __ __／
        ￣ヽ＿______) ＿＿___)__)  
"""
)

close = False
while not close:
    try:
        options = int(input("================================================================\n"
                            "| Меню программы tree calc. Пожалуйста, выберете опцию!        |\n"
                            "================================================================\n"
                            "1) Ввести формулу и произвести вычисления\n"
                            "2) Выйти из программы\n"
                            "Ваш выбор: "))
        if not 1 <= options <= 2:
            raise ValueError
    except ValueError:
        print_exception("================================================================\n"
                        "| Неверная опция, перезапуск программы                         |\n"
                        "================================================================\n")
        continue

    clear_console()

    if options == 2:
        close = True
    elif options == 1:
        print("================================================================\n"
              "| Введите математическую формулу в инфиксной записи.           |\n"
              "| Допускаются: целые числа, однобуквенные переменные,          |\n"
              "| знаки +, -, *, /, унарные минусы и скобки (вложенность <=10).|\n"
              "| Пример: x * y + x * z                                        |\n"
              "================================================================")

        formula = input("> Формула: ").strip()

        if not formula:
            print_exception("================================================================\n"
                            "| Строка формулы не может быть пустой, перезапуск программы    |\n"
                            "================================================================\n")
            continue

        # Проверка степени вложенности скобок
        current_depth = 0
        max_depth = 0
        invalid_brackets = False
        for char in formula:
            if char == "(":
                current_depth += 1
                if current_depth > max_depth:
                    max_depth = current_depth
            elif char == ")":
                current_depth -= 1
                if current_depth < 0:
                    invalid_brackets = True
                    break

        if current_depth != 0 or invalid_brackets:
            print_exception("================================================================\n"
                            "| Ошибка: Нарушен баланс скобок, перезапуск программы          |\n"
                            "================================================================\n")
            continue

        if max_depth > 10:
            print_exception("================================================================\n"
                            "| Ошибка: Степень вложенности скобок превышает 10!              |\n"
                            "================================================================\n")
            continue

        # Построение дерева и вычисления
        try:
            # Построение дерева
            tree = CalcTree()
            tree.insert_infix(formula)
            print("\n> Дерево исходной формулы успешно построено:")
            print(f"  {tree.to_string()}")

            # Упрощение
            simplified_tree = tree.copy()
            simplified_tree.simplify()
            print("\n> Формула после алгебраического упрощения по дереву:")
            print(f"  {simplified_tree.to_string()}\n")

            # Запрос переменных и подсчет по упрощённому дереву
            detected_vars = simplified_tree.get_variables()
            user_vars = input_variables(detected_vars)

            result = simplified_tree.evaluate(variables=user_vars)

            print("================================================================\n"
                  f"| Результат вычисления по дереву: {result:<28} |\n"
                  "================================================================")
            input("\nНажмите Enter, чтобы вернуться в главное меню...")
            clear_console()

        except ZeroDivisionError:
            print_exception("================================================================\n"
                            "| Критическая ошибка: Обнаружено деление на ноль при расчете!  |\n"
                            "================================================================\n")
        except Exception as e:
            print_exception("================================================================\n"
                            "| Произошла синтаксическая ошибка при разборе формулы.         |\n"
                            "| Проверьте корректность ввода знаков операций.                |\n"
                            "================================================================\n")