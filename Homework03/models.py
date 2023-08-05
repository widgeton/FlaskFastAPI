from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    group = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    marks = db.relationship('Mark', backref='student', lazy=True)

    def __repr__(self):
        return f'Student("{self.name}", "{self.surname}")'


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    students = db.relationship('Student', backref='department', lazy=True)

    def __repr__(self):
        return f'Department("{self.name}")'


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    mark = db.Column(db.Enum('Acceptable', 'Well', 'Excellent'), nullable=False)

    def __repr__(self):
        return f'Mark("{self.subject}", "{self.mark}")'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'User("{self.name}", "{self.email}")'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    books = db.relationship('Book', secondary='book_author', backref='authors', lazy=True)

    def __repr__(self):
        return f'Author("{self.name}", "{self.surname}")'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    publish_year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Book("{self.title}")'


class BookAuthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __repr__(self):
        return f'BookAuthor({self.author_id}, {self.book_id})'
