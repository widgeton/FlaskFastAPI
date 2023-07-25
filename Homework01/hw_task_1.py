"""Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал),
и дочерние шаблоны для страниц категорий товаров и отдельных товаров. Например, создать страницы "Одежда",
"Обувь" и "Куртка", используя базовый шаблон.
"""
from flask import Flask, render_template
import articles as art

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/t-shirts/')
def t_shirts():
    return render_template('t_shirts.html', articles=art.get_article(*art.t_shirts))


@app.route('/shoes/')
def shoes():
    return render_template('shoes.html', articles=art.get_article(*art.shoes))


@app.route('/pants/')
def pants():
    return render_template('pants.html', articles=art.get_article(*art.pants))


if __name__ == '__main__':
    app.run(debug=True)
