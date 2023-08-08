"""Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
� Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
image1.jpg
� Программа должна использовать многопоточный, многопроцессорный и
асинхронный подходы.
� Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
� Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы."""
from threading import Thread
import requests
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('links', nargs='*')

threads: list[Thread] = []


def check_time(line):
    def deco(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            print(f'{line}: {time.time() - start_time:.4f}')

        return wrapper

    return deco


@check_time('Время загрузки файла')
def download(url):
    if not os.path.isdir('images'):
        os.mkdir('images')
    file = requests.get(url).content
    name = os.path.join('images', url.split('/')[-1])
    with open(name, 'wb') as f:
        f.write(file)


@check_time('Общее время загрузки')
def start_threads(lst):
    for link in lst:
        thread = Thread(target=download, args=(link,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    links = [
        'https://top10a.ru/wp-content/uploads/2019/12/iurqcrhno.jpg',
        'https://sun9-27.userapi.com/CSp_gNr-RgGp_aIeGpcVhWsr3JvwLYAXxmhurw/d64nz8fuPSE.jpg',
        'https://w.forfun.com/fetch/ff/fff71a274352eebcf2cfce840544b72d.jpeg',
        'http://s1.1zoom.ru/big3/328/France_Waterfalls_Stones_Crag_Moss_598471_4050x2700.jpg',
        'https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666390329_5-mykaleidoscope-ru-p-vodopad-gyudlfoss-oboi-7.jpg',
    ]

    urls = parser.parse_args()
    if urls.links:
        links = urls.links

    start_threads(links)
