from collections import namedtuple
from random import randint
import os

t_shirts = '/static/image/t_shirt', 'Футболка'
pants = '/static/image/pants', 'Штаны'
shoes = '/static/image/shoes', 'Обувь'
MIN_PRICE = 500
MAX_PRICE = 1000

Article = namedtuple('Article', 'name price path_image')


def get_article(path, name):
    lst = []
    for num, img in enumerate(os.listdir(os.getcwd() + path), 1):
        lst.append(Article(f'{name} {num}', randint(MIN_PRICE, MAX_PRICE), os.path.join(path, img)))
    return lst
