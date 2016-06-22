from datetime import date, datetime

from wtforms import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


Symbols = list('QWERTYUIOPASDFGHJKLZXCVBNM_ qwertyuiopasdfghjklzxcvbnm0123456789@')


def password_validator(form, field):
    password = field.data
    for symbol in password:
        if symbol not in Symbols:
            raise ValidationError('Недопустимый символ')


def datetime_validator(form, field):
    now = date.today()
    try:
        field_date = datetime.strptime(field.data, '%d.%m.%Y').date()
    except ValueError as e:
        raise ValidationError('Неверный формат даты.')

    if field_date < now:
        raise ValidationError('Выпьем за вчера! (нет)')


# REGISTER AND LOGIN
class LoginForm(Form):
    phone = StringField('Телефон', [DataRequired(), Length(min=5, max=15)], description="Введите логин")  #
    password = PasswordField('Пароль', [DataRequired(), Length(min=8, max=32), password_validator],
                             description="Минимальная длина - 8 символов. Максимальная длина - 32 символа")


class RegistrationForm(Form):
    phone = StringField('Телефон', [DataRequired(), Length(min=5, max=15)], description="Введите корректный номер")  # ???

    name = StringField('Имя', [DataRequired(), Length(min=4, max=32)])
    mid_name = StringField('Отчество', [DataRequired(), Length(min=4, max=32)])
    second_name = StringField('Фамилия', [DataRequired(), Length(min=4, max=32)])
    address = StringField('Адрес', [DataRequired(), Length(min=10, max=100)])

    password = PasswordField('Пароль', [DataRequired(), Length(min=8, max=32), password_validator],
                             description="Минимальная длина - 8 символов. Максимальная длина - 32 символа")
    confirm_password = PasswordField('Повторите пароль', [EqualTo('password', message='Пароль не совпадает')])


# RENT BOX AND REFUSE
class RentForm(Form):  # DATETIME VALIDATORS
    date_start = StringField('Дата начала аренды', [DataRequired(), datetime_validator], description="ДД.ММ.ГГГГ")
    date_end = StringField('Дата окончания аренды', [DataRequired(), datetime_validator], description="ДД.ММ.ГГГГ")
    number_auto = SelectField('Автомобиль', choices=[],
                              description='Выберите автомобиль, для которого вы хотите арендовать бокс.')


# ADMIN MANAGE
class NewBoxForm(Form):
    nb_mark_name = SelectField('Название марки', choices=[],
                               description="Принять новый бокс для этой марки автомобиля")

    cost = StringField('Цена', [DataRequired(), Length(min=1, max=32)],
                       description="Цена посуточной аренды")


class CloseBoxForm(Form):
    cb_box_code = StringField('Номер бокса', [DataRequired(), Length(min=1, max=32)],
                              description="Бокс с указанным номером будет закрыт")


class UpdateBoxForm(Form):
    u_cost = StringField('Число', [DataRequired()],
                         description="Число, в которое следует увеличить цену")


class NewMarkForm(Form):
    nm_mark_name = StringField('Название марки', [DataRequired(), Length(min=1, max=32)],
                               description="Указанная марка будет добавлена в перечень марок")


class DeleteMarkForm(Form):
    dm_mark_name = SelectField('Название марки', choices=[],
                               description="Указанная марка будет удалена из перечня марок")


# ADMIN INFO
class ClientMarkInfo(Form):
    mark_name = SelectField('Название марки', choices=[],
                            description="Получить список с указанной маркой")


class DateEndInfo(Form):
    date_end = StringField('Дата окончания аренды', [DataRequired(), datetime_validator],
                           description='ДД.ММ.ГГГГ')


class BoxList(Form):
    box_clients = SelectField('Номера занятых боксов', choices=[],
                              description="Получить список с указанным боксом", coerce=int)

