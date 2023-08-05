from flask import Flask, render_template, request
import random as rnd
import string
import hashlib

from models import db, Student, Department, Mark, User, Author, Book, BookAuthor
from forms import Register

app = Flask(__name__)
app.secret_key = b'193a3d4788cc8d77843183d31965f4e507e859729b3cb9fddde950df6f255efa'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Таблицы созданы')


@app.cli.command("fill-db")
def fill_tables():
    count = 5
    for i in range(1, count + 1):
        db.session.add(Department(name=f'Department{i}'))
    db.session.commit()

    for i in range(1, count ** 2):
        dep = Department.query.filter_by(name=f'Department{i % count + 1}').first()
        name = f'name{i}'
        surname = f'surname{i}'
        age = rnd.randint(20, 30)
        gender = rnd.choice(['male', 'female'])
        group = rnd.randint(1, 10)
        email = f'{"".join(rnd.choices(string.ascii_letters + string.digits, k=rnd.randint(8, 16)))}@' \
                f'{"".join(rnd.choices(string.ascii_lowercase, k=rnd.randint(2, 5)))}.' \
                f'{"".join(rnd.choices(string.ascii_lowercase, k=rnd.randint(2, 3)))}'
        student = Student(name=name, surname=surname, age=age, gender=gender, group=group, email=email, department=dep)
        db.session.add(student)
    db.session.commit()

    subjects = 'Math', 'Physics', 'Thermodynamics', 'Philosophy', 'Logic'
    for i in range(1, count ** 2):
        student = Student.query.filter_by(name=f'name{i}').first()
        for subject in subjects:
            mark = Mark(subject=subject, mark=rnd.choice(['Acceptable', 'Well', 'Excellent']), student=student)
            db.session.add(mark)
    db.session.commit()

    for i in range(1, 6):
        author1 = Author(name=f'Name1_{i}', surname=f'Surname1_{i}')
        db.session.add(author1)
        author2 = Author(name=f'Name2_{i}', surname=f'Surname2_{i}')
        db.session.add(author2)
        for j in range(1, 6):
            book = Book(title=f'Book{5 * (i - 1) + j}', publish_year=rnd.randint(1800, 2023),
                        amount=rnd.randint(1, 100), authors=[author1, author2])
            db.session.add(book)
    db.session.commit()
    print('Таблицы заполнены')


@app.route('/')
def main():
    return render_template('base.html')


@app.route('/students/')
def get_students():
    students = Student.query.all()
    return render_template('students.html', students=students)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = Register()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = hashlib.sha256(form.password.data.encode()).hexdigest()
        db.session.add(User(name=name, email=email, password=password))
        db.session.commit()
        return f'<h1>Регистрация прошла успешно!</h1>'
    return render_template('register.html', form=form)


@app.route('/books/')
def get_books():
    books = Book.query.all()
    return render_template('books.html', books=books)
