from typing import List, Optional
#Рекурсивно находит выражение, используя + или -,равное требуемому значению.
def find_expression(numbers: List[int], target: int, index: int = 0, current_expression: str = "", current_sum: int = 0) -> Optional[str]:
    # Базовый случай: если мы достигли конца списка
    # Возращает строку выражения, если она найдена, в противном случае - None.
    if index == len(numbers):
        if current_sum == target:
            return current_expression
        else:
            return None
    # Текущее число
    number: int = numbers[index]
    # Пробуем добавить знак "+" перед текущим числом
    result_with_plus = find_expression(numbers, target, index + 1,
                                       current_expression + (f"+{number}" if current_expression else f"{number}"),
                                       current_sum + number)
    if result_with_plus is not None:
        return result_with_plus
    # Пробуем добавить знак "-" перед текущим числом
    result_with_minus = find_expression(numbers, target, index + 1,
                                        current_expression + f"-{number}",
                                        current_sum - number)
    if result_with_minus is not None:
        return result_with_minus
    return None

# Чтение входных данных из файла; N-количество чисел, numbers-список чисел, S-цель
with open("input.txt", "r") as f:
    data = list(map(int, f.read().strip().split()))
N: int = data[0]
numbers: List[int] = data[1:N + 1]
S: int = data[N + 1]
# Поиск выражения с помощью рекурсивной функции find_expression
result: Optional[str] = find_expression(numbers, S)
# Запись результата в файл
with open("output.txt", "w") as f:
    if result is not None:
        f.write(f"{result}={S}\n")
    else:
        f.write("no solution\n")