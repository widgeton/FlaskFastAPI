"""Напишите программу на Python, которая будет находить сумму элементов массива из 1000000 целых чисел.
Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]. Массив должен быть заполнен случайными целыми числами
от 1 до 100. При решении задачи нужно использовать асинхронность. Нужно вывести время выполнения вычислений.
"""
import math
import timeit
import asyncio
import random as rnd
import time

tasks = []
all_sum = 0


async def part_sum(lst_part: list):
    global all_sum
    all_sum += sum(lst_part)


async def partition_and_start(lst: list[int], parts: int):
    part_len = math.ceil(len(lst) / parts)
    start_time = time.time()
    for part in range(parts):
        task = asyncio.create_task(part_sum(lst[part * part_len:part * part_len + part_len]))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f'Сумма элементов: {all_sum}\nВремя выполнения: {time.time() - start_time:.3f}с.')


if __name__ == '__main__':
    nums = [rnd.randint(1, 100) for _ in range(1_000_000)]
    asyncio.run(partition_and_start(nums, 1000))
    print(f'Сумма элементов посчитанных синхронно: {sum(nums)}',
          f'Время выполнения синхронной суммы: {timeit.timeit("sum(nums)", globals=globals(), number=1):.3f}c.',
          sep='\n')
