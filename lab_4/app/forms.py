from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Optional
import re
from app.models import User


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(message='Поле не может быть пустым')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Поле не может быть пустым')])
    submit = SubmitField('Войти')


class UserForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=5, message='Логин должен содержать не менее 5 символов'),
        Regexp(r'^[a-zA-Z0-9]+$', message='Логин должен состоять только из латинских букв и цифр')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=8, max=128, message='Пароль должен содержать от 8 до 128 символов')
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(message='Поле не может быть пустым')
    ])
    first_name = StringField('Имя', validators=[
        DataRequired(message='Поле не может быть пустым')
    ])
    middle_name = StringField('Отчество', validators=[Optional()])
    role_id = SelectField('Роль', coerce=int, validators=[Optional()])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models import Role
        self.role_id.choices = [(0, 'Без роли')] + [(r.id, r.name) for r in Role.query.all()]

    def validate_login(self, field):
        user = User.query.filter_by(login=field.data).first()
        if user:
            raise ValidationError('Пользователь с таким логином уже существует')

    def validate_password(self, field):
        password = field.data

        if len(password) < 8:
            raise ValidationError('Пароль должен содержать не менее 8 символов')
        if len(password) > 128:
            raise ValidationError('Пароль должен содержать не более 128 символов')
        if not re.search(r'[A-ZА-ЯЁ]', password):
            raise ValidationError('Пароль должен содержать как минимум одну заглавную букву')
        if not re.search(r'[a-zа-яё]', password):
            raise ValidationError('Пароль должен содержать как минимум одну строчную букву')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Пароль должен содержать как минимум одну цифру')
        if ' ' in password:
            raise ValidationError('Пароль не должен содержать пробелы')
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9~!?@#$%^&*_\-+()\[\]{}><\\/|"\',.:;]+$', password):
            raise ValidationError('Пароль содержит недопустимые символы')


class EditUserForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[
        DataRequired(message='Поле не может быть пустым')
    ])
    first_name = StringField('Имя', validators=[
        DataRequired(message='Поле не может быть пустым')
    ])
    middle_name = StringField('Отчество', validators=[Optional()])
    role_id = SelectField('Роль', coerce=int, validators=[Optional()])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models import Role
        self.role_id.choices = [(0, 'Без роли')] + [(r.id, r.name) for r in Role.query.all()]


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[
        DataRequired(message='Поле не может быть пустым')
    ])
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=8, max=128, message='Пароль должен содержать от 8 до 128 символов')
    ])
    confirm_password = PasswordField('Повторите новый пароль', validators=[
        DataRequired(message='Поле не может быть пустым'),
        EqualTo('new_password', message='Пароли не совпадают')
    ])
    submit = SubmitField('Сменить пароль')

    def validate_new_password(self, field):
        password = field.data

        if len(password) < 8:
            raise ValidationError('Пароль должен содержать не менее 8 символов')
        if len(password) > 128:
            raise ValidationError('Пароль должен содержать не более 128 символов')
        if not re.search(r'[A-ZА-ЯЁ]', password):
            raise ValidationError('Пароль должен содержать как минимум одну заглавную букву')
        if not re.search(r'[a-zа-яё]', password):
            raise ValidationError('Пароль должен содержать как минимум одну строчную букву')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Пароль должен содержать как минимум одну цифру')
        if ' ' in password:
            raise ValidationError('Пароль не должен содержать пробелы')
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9~!?@#$%^&*_\-+()\[\]{}><\\/|"\',.:;]+$', password):
            raise ValidationError('Пароль содержит недопустимые символы')