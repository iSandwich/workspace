text = input('Введите выражение в Польской нотации:')
list = text.split(' ')
assert list[0] in ['+', '-', '*', '/'], 'Ошибка: выбрана недопустимая операция'

try:
    arg1, arg2 = int(list[1]), int(list[2])
except TypeError:
    print('Ошибка: введены некорректные аргументы')

try:
    if list[0] == '+':
        output = arg1 + arg2
    elif list[0] == '-':
        output = arg1 - arg2
    elif list[0] == '*':
        output = arg1 * arg2
    elif list[0] == '/':
        output = arg1 / arg2
except ZeroDivisionError:
    print('Ошибка: деление на 0 запрещено')

print(f'Ответ: {output}')
