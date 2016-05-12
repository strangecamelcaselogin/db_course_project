from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError


Symbols = list('QWERTYUIOPASDFGHJKLZXCVBNM_ qwertyuiopasdfghjklzxcvbnm')
print(Symbols)

class LoginForm(Form):
    def passValidator(self, field):
        password = field.data  # str
        for symbol in password:
            if symbol not in Symbols:
                print('nope')
                raise ValidationError('chmod')

    login = StringField('Логин', [DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Пароль', [DataRequired(), Length(min=8, max=32), passValidator])
