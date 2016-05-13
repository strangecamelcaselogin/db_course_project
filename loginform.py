from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError


Symbols = list('QWERTYUIOPASDFGHJKLZXCVBNM_ qwertyuiopasdfghjklzxcvbnm')


class LoginForm(Form):
    @staticmethod
    def pass_validator(field):
        password = field.data
        for symbol in password:
            if symbol not in Symbols:
                raise ValidationError('Недопустимый символ')

    login = StringField('Логин', [DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Пароль', [DataRequired(), Length(min=8, max=32), pass_validator])
