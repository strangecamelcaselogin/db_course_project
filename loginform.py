from wtforms import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


Symbols = list('QWERTYUIOPASDFGHJKLZXCVBNM_ qwertyuiopasdfghjklzxcvbnm0123456789@')


mappers = {
    "A": '1',
    "B": '2',
    "C": '3'
}


def password_validator(self, field):
    password = field.data
    for symbol in password:
        if symbol not in Symbols:
            raise ValidationError('Недопустимый символ')


class LoginForm(Form):
    phone = StringField('Телефон', [DataRequired(), Length(min=8, max=11)], description="Желаемое число активных колонок (не меньше)")  # ???
    password = PasswordField('Пароль', [DataRequired(), Length(min=8, max=32), password_validator])


class RegForm(Form):
    phone = StringField('Телефон', [DataRequired(), Length(min=8, max=11)])  # ???

    name = StringField('Имя', [DataRequired(), Length(min=2, max=32)])
    mid_name = StringField('Отчество', [DataRequired(), Length(min=2, max=32)])
    second_name = StringField('Фамилия', [DataRequired(), Length(min=2, max=32)])
    address = StringField('Адрес', [DataRequired(), Length(min=10, max=100)])

    password = PasswordField('Пароль', [DataRequired(), Length(min=8, max=32), password_validator])
    confirm_password = PasswordField('Повторите пароль', [EqualTo('password', message='Пароль не совпадает')])


class BoxForm(Form):
    cod_box_open = StringField('Код бокса', [DataRequired(), Length(min=1, max=32)])
    cod_box_close = StringField('Код бокса', [DataRequired(), Length(min=1, max=32)])
    mark_name = StringField('Марка', [DataRequired(), Length(min=1, max=32)])
    prise = StringField('Цена', [DataRequired(), Length(min=1, max=32)])


class ServiceForm(Form):
    cod_owner = StringField('Код владельца', [DataRequired(), Length(min=1, max=32)])
    date_end = StringField('Дата окончания аренды', [DataRequired(), Length(min=1, max=32)])
    date_start = StringField('Дата начала аренды', [DataRequired(), Length(min=1, max=32)])
    number_auto = StringField('Номер авто', [DataRequired(), Length(min=1, max=32)])
    cod_receipt = StringField('Номер квитанции', [DataRequired(), Length(min=1, max=32)])


class MarkForm(Form):
    mark_name = StringField('Название марки', []) # later - validators
    mark_list = SelectField('Марка', choices=[(list(mappers.keys())[i], list(mappers.keys())[i]) for i in range(len(mappers.keys()))])


class RefForm(Form):
    mark_name = StringField('Марка', [DataRequired(), Length(min=1, max=32)])
    cod_box = StringField('Код бокса', [DataRequired(), Length(min=1, max=32)])
    date_end = StringField('Дата окончания аренды', [DataRequired(), Length(min=1, max=32)])