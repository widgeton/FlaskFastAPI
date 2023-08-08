"""Напишите программу на Python, которая будет находить сумму элементов массива из 1000000 целых чисел.
Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]. Массив должен быть заполнен случайными целыми числами
от 1 до 100. При решении задачи нужно использовать многопоточность. Нужно вывести время выполнения вычислений.
"""
import math
import timeit
from threading import Thread, Lock
import random as rnd
import time

all_sum = 0
lock = Lock()
threads: list[Thread] = []


def part_sum(lst_part: list):
    global all_sum
    with lock:
        all_sum += sum(lst_part)


def partition_and_start(lst: list[int], parts: int):
    part_len = math.ceil(len(lst) / parts)
    start_time = time.time()
    for part in range(parts):
        thread = Thread(target=part_sum, args=(lst[part * part_len:part * part_len + part_len],))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f'Сумма элементов: {all_sum}\nВремя выполнения: {time.time() - start_time:.3f}с.')


if __name__ == '__main__':
    nums = [rnd.randint(1, 100) for _ in range(1_000_000)]
    partition_and_start(nums, 1000)
    print(f'Сумма элементов посчитанных синхронно: {sum(nums)}',
          f'Время выполнения синхронной суммы: {timeit.timeit("sum(nums)", globals=globals(), number=1):.3f}c.',
          sep='\n')
