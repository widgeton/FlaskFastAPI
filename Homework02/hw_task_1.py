"""Создать страницу, на которой будет форма для ввода имени и электронной почты,
при отправке которой будет создан cookie-файл с данными пользователя, а также
будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с
данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты."""
from flask import Flask, render_template, flash, request, make_response

app = Flask(__name__)
app.secret_key = b'fd2da77e015cc34a72ad678e840404ae58d560f4f197042249c4f53f19c05b06'


def is_valid(mail: str, name: str):
    return mail.count('@') == 1 and \
        mail.count('.') == 1 and \
        mail.index('.') - mail.index('@') > 1 and \
        mail[-1] != '.' and name


@app.route('/', methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        mail = request.form.get('mail')
        name = request.form.get('name')
        if is_valid(mail, name):
            respond = make_response(render_template('hello.html', name=name))
            respond.set_cookie('mail', mail)
            respond.set_cookie('name', name)
            return respond
        else:
            flash('Неверно введено имя или email!', 'warning')
    return render_template('login.html')


@app.route('/logout/')
def logout():
    respond = make_response(render_template('login.html'))
    respond.delete_cookie('mail')
    respond.delete_cookie('name')
    return respond


if __name__ == '__main__':
    app.run(debug=True)
