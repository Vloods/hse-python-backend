def get_factorial(n: int) -> int:
    """Вычисление факториала числа n."""
    if n < 0:
        raise ValueError("Факториал отрицательного числа не существует.")
    result: int = 1
    for i in range(2, n + 1):
        result *= i
    return result


def get_fibonacci(n: int) -> int:
    """Вычисление фибоначчи числа n."""
    if n == 0:
        return 0
    if n in (1, 2):
        return 1
    return get_fibonacci(n - 1) + get_fibonacci(n - 2)


def get_mean(numbers: list) -> float:
    """Вычисление среднего значения."""
    return sum(numbers) / len(numbers)
