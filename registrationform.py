from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError


Symbols = list('QWERTYUIOPASDFGHJKLZXCVBNM_ qwertyuiopasdfghjklzxcvbnm0123456789@')


class RegistrationForm(Form):
    pass