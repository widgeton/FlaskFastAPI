import string

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

from models import User


class Register(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birthdate = DateField('Birthdate', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    assent = BooleanField('Consent to the processing of personal data', validators=[DataRequired()])

    def validate_name(self, name):
        if User.query.filter_by(name=self.name.data).first():
            raise ValidationError('Пользователь с таким именем уже существует.')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Пользователь с такой почтой уже существует.')

    def validate_password(self, password):
        if not set(self.password.data) & set(string.ascii_letters) and set(self.password.data) & set(string.digits):
            raise ValidationError('Пароль должен содержать хотя бы одну букву и хотя бы одну цифру')
