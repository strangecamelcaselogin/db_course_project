from wtforms import Form
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from sql_core import form_mark_list


Symbols = list('QWERTYUIOPASDFGHJKLZXCVBNM_ qwertyuiopasdfghjklzxcvbnm0123456789@')


mark = form_mark_list()



def password_validator(self, field):
    password = field.data
    for symbol in password:
        if symbol not in Symbols:
            raise ValidationError('Недопустимый символ')




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
class RentForm(Form):
    mark_list = SelectField('Марка', choices=[(i, i) for i in mark.keys()])  # (list(mappers.keys())[i], list(mappers.keys())[i]) for i in range(len(mappers.keys()))
   # box_list = SelectField('Бокс', choices=[('', '1'), ('', '2'), ('', '3')])

    date_start = StringField('Дата начала аренды', [DataRequired(), Length(min=1, max=32)], description="ДД.ММ.ГГГГ")
    date_end = StringField('Дата окончания аренды', [DataRequired(), Length(min=1, max=32)], description="ДД.ММ.ГГГГ")
    number_auto = StringField('Номер авто', [DataRequired(), Length(min=1, max=32)])


class RefuseForm(Form):  # отказаться от бокса ???
    cod_receipt = StringField('Номер квитанции', [DataRequired(), Length(min=1, max=32)])


# PERSONAL (BDSM)
class PersonalForm(Form):  # Личный кабинет
    pass


# ADMIN MANAGE
class NewBoxForm(Form):
    nb_mark_name = StringField('Название марки', [DataRequired(), Length(min=1, max=32)],
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
    dm_mark_name = SelectField('Название марки', choices=[(i, i) for i in mark.keys()],
                               description="Указанная марка будет удалена из перечня марок")


# ADMIN INFO ????
class AdminInfo(Form):
    pass

class ClientMarkInfo(Form):
    mark_name = SelectField('Название марки', choices=[(i, i) for i in mark.keys()],
                            description="Получить список с указанной маркой")
    #box_code = StringField('Код бокса', [DataRequired(), Length(min=1, max=32)])

class DateEndInfo(Form):
    date_end = StringField('Дата окончания аренды', [DataRequired(), Length(min=1, max=32)])