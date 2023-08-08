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
from multiprocessing import Process
import requests
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('links', nargs='*')

processes: list[Process] = []


def download(url):
    start_time = time.time()
    if not os.path.isdir('images'):
        os.mkdir('images')
    file = requests.get(url).content
    name = os.path.join('images', url.split('/')[-1])
    with open(name, 'wb') as f:
        f.write(file)
    print(f'Время загрузки файла: {time.time() - start_time:.4f}')


def start_threads(lst):
    start_time = time.time()
    for link in lst:
        process = Process(target=download, args=(link,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f'Общее время загрузки: {time.time() - start_time:.4f}')


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
