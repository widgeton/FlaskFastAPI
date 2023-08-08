"""Напишите программу на Python, которая будет находить сумму элементов массива из 1000000 целых чисел.
Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]. Массив должен быть заполнен случайными целыми числами
от 1 до 100. При решении задачи нужно использовать процессы. Нужно вывести время выполнения вычислений.
"""
import math
import timeit
from multiprocessing import Process, Value
import random as rnd
import time

processes: list[Process] = []


def part_sum(lst_part: list, sum_: Value):
    with sum_.get_lock():
        sum_.value += sum(lst_part)


def partition_and_start(lst: list[int], parts: int, sum_: Value):
    part_len = math.ceil(len(lst) / parts)
    start_time = time.time()
    for part in range(parts):
        process = Process(target=part_sum, args=(lst[part * part_len:part * part_len + part_len], sum_))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f'Сумма элементов: {sum_.value}\nВремя выполнения: {time.time() - start_time:.3f}с.')


if __name__ == '__main__':
    nums = [rnd.randint(1, 100) for _ in range(1_000_000)]
    partition_and_start(nums, 10, Value('i', 0))
    print(f'Сумма элементов посчитанных синхронно: {sum(nums)}',
          f'Время выполнения синхронной суммы: {timeit.timeit("sum(nums)", globals=globals(), number=1):.3f}c.',
          sep='\n')
