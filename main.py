from functools import wraps

from flask import Flask
from flask import render_template, redirect, flash, \
    request, session, abort, g, url_for

from sql_core import login, register, add_box, close_box, add_mark, form_mark_list, delete_mark, rent_, refuse, update_box, \
    get_list_cwm, get_list_cde, form_ticket_list, get_list_c, get_name_client, get_client, get_list_box_mark, form_box_list, \
    count_mark

from forms import LoginForm, RegistrationForm, RentForm, RefuseForm, AdminInfo, \
    NewBoxForm, CloseBoxForm, NewMarkForm, DeleteMarkForm, UpdateBoxForm, ClientMarkInfo, DateEndInfo, BoxList

import xlrd, xlwt


import matplotlib.pyplot as plt

from settings import *


app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Сначала необходимо войти.')
            return redirect('/login')

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'is_admin' in session:
            return f(*args, **kwargs)
        else:
            abort(404)

    return wrapper


################################################


# ITS INDEX PAGE (CAP)
@app.route('/')
@app.route('/index')
def index():
    #posts = [{'brand': 'Mercedes', 'box': '1' }, {'brand': 'Renault', 'box': '3'}]
    brands = form_mark_list()


    box = {brand: get_list_box_mark(brand) for brand in brands}
    path = count_mark()
    print(box)
    return render_template('index.html', x=42, posts=brands, box=box, path_img=path)


# RENT BOX
@app.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    form = RentForm(request.form)
    form.mark_list.choices = [(i, i) for i in form_mark_list().keys()]

    if request.method == 'POST':
        if form.validate():
            try:
                if rent_(form):
                    flash('Вы арендовали бокс')
                    return redirect('/personal')

                else:
                    flash('К сожалению, на данный момент свободных боксов нет (не факт)')
                    return redirect('/index')

            except Exception as e:
                flash('Возникла ошибка: {}'.format(e))

    return render_template('rent.html', f=form)


# PERSONAL
@app.route('/personal', methods=['GET', 'POST'])
@login_required
def personal_area():
    ticket = form_ticket_list()
    client = get_name_client()
    print(ticket)


    if request.method == 'POST':
        ticket_id = int(request.form['ticket_id'])
        phone = session['phone']

        if refuse(phone, ticket_id):
            print('thats ok')
        else:
            print('thats bad')

        return redirect('/personal')

    return render_template('personal.html', ts=ticket, client=client)


# ADMIN STUFF
@app.route('/admin_info', methods=['GET', 'POST'])  # не работает :/
@admin_required
def admin_info():
    forms = dict()
    forms['ClientMarkInfo'] = ClientMarkInfo(request.form)
    forms['ClientMarkInfo'].mark_name.choices = [(i, i) for i in form_mark_list().keys()]

    forms['DateEndInfo'] = DateEndInfo(request.form)

    forms['BoxList'] = BoxList(request.form)
    forms['BoxList'].box_clients.choices = [(i, i) for i in form_box_list().keys()]

    if request.method == 'POST':
        if 'get_list_c' in request.form:
            info_c = get_list_c()

            wb = xlwt.Workbook()
            ws = wb.add_sheet('Test')
            for i in range(len(info_c)):
                for j in range(len(info_c[i])):
                    ws.write(i, j, info_c[i][j])
            wb.save('report/client.xls')



            return render_template('admin_info.html', f=forms, infs_c=info_c)

        if 'get_list_cwm' in request.form:
            f = forms['ClientMarkInfo']
            if f.validate():
                info_cwm = get_list_cwm(f)

                return render_template('admin_info.html', f=forms, infs_cwm=info_cwm)

        elif 'get_list_cde' in request.form:
            f = forms['DateEndInfo']
            if f.validate():
                info_cde = get_list_cde(f)

                return render_template('admin_info.html', f=forms, infs_cde=info_cde)

        if 'get_client' in request.form: #получить владельца указанного бокса
            f = forms['BoxList']
            if f.validate():
                info_box = get_client(f)

                return render_template('admin_info.html', f=forms, infs_box=info_box)

    return render_template('admin_info.html', f=forms)


@app.route('/admin_manage', methods=['GET', 'POST'])
@admin_required
def admin_manage():

    forms = dict()
    forms['NewBoxForm'] = NewBoxForm(request.form)
    forms['CloseBoxForm'] = CloseBoxForm(request.form)
    forms['UpdateBoxForm'] = UpdateBoxForm(request.form)
    forms['NewMarkForm'] = NewMarkForm(request.form)
    forms['DeleteMarkForm'] = DeleteMarkForm(request.form)

    marks_list = [(i, i) for i in form_mark_list().keys()]
    forms['NewBoxForm'].nb_mark_name.choices = marks_list
    forms['DeleteMarkForm'].dm_mark_name.choices = marks_list

    if request.method == 'POST':
        if 'new_box' in request.form:
            f = forms['NewBoxForm']
            if f.validate():
                if add_box(f):
                    flash('Новый бокс добавлен')
                    return redirect('/admin_manage')

            else:
                flash('Проблема')

        elif 'close_box' in request.form:
            f = forms['CloseBoxForm']
            if f.validate():
                if close_box(f):
                    flash('Бокс закрыт')
                    return redirect('/admin_manage')

                else:
                    flash('Такого бокса нет в списке')

        elif 'update_box' in request.form:
            f = forms['UpdateBoxForm']

            if f.validate():
                if update_box(f):
                    flash('Маша не может в буковы')
                    return redirect('/admin_manage')

                else:
                    flash('Такого бокса нет в списке')

        elif 'new_mark' in request.form:
            f = forms['NewMarkForm']

            if f.validate():
                if add_mark(f.nm_mark_name.data):
                    flash('Марка добавлена.')
                    return redirect('/admin_manage')

                else:
                    flash('Такая марка уже существует')

        elif 'del_mark' in request.form:
            f = forms['DeleteMarkForm']

            if f.validate():
                if delete_mark(f.dm_mark_name.data):
                    flash('Марка удалена')
                    return redirect('/admin_manage')

                else:
                    flash('Не удалилась')

        else:
            flash('что то совсем странное')

    return render_template('admin_manage.html', f=forms)


# LOGIN AND REGISTER
@app.route('/login', methods=['GET', 'POST'])
def login_():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():

            if login(form):
                flash('Вы вошли как {}'.format(form.phone.data))
                return redirect('/index')

            else:
                flash('Неверное имя пользователя или пароль.')

    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)

    if request.method == 'POST':
        if form.validate():
            if register(form):
                flash('Вы зарегестрированы.')
                return redirect('/index')

            else:
                flash('Такой пользователь уже существует.')

    return render_template("registration.html", form=form)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Вы вышли из системы.')

    return redirect('/index')


################################################


if __name__ == '__main__':
    app.secret_key = 'wtf_dude_its_a_public_secret_key!!'  # !!!!!!!!!
    app.run(debug=True)

