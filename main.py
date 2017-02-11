from functools import wraps
from datetime import datetime
from flask import Flask
from flask import render_template, redirect, flash, \
    request, session, abort, g, url_for

from sql_core import *

from forms import *

import xlrd, xlwt

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
    brands = get_mark_list()

    box = {brand[0]: get_list_box_mark(brand[0]) for brand in brands}

    get_marks_statistic()

    return render_template('index.html', x=42, posts=brands, box=box, path_img='static/pie_brand.png')


# RENT BOX
@app.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    form = RentForm(request.form)
    form.number_auto.choices = get_client_cars()

    if request.method == 'POST':
        if form.validate():
            try:
                date_start = datetime.strptime(form.date_start.data, '%d.%m.%Y').date()
                date_end = datetime.strptime(form.date_end.data, '%d.%m.%Y').date()
                number = form.number_auto.data

                t = rent_box(date_start, date_end, number)
                if t == True:
                    flash('Вы арендовали бокс')
                    return redirect('/personal')

                else:
                    flash(t)
                    return redirect('/rent')

            except Exception as e:
                flash('Возникла ошибка: {}'.format(e))

    return render_template('rent.html', f=form)


# PERSONAL
@app.route('/personal', methods=['GET', 'POST'])
@login_required
def personal_area():
    client = get_client_name()

    tickets = get_tickets_list()

    ticket_active = []
    ticket_not_active = []
    for ticket in tickets:
        if ticket[6] == 'YES':
            ticket_active.append(ticket)
        else:
            ticket_not_active.append(ticket)

    forms = {'AddCar': AddCar(request.form),
             'DeleteCar': DeleteCar(request.form)}

    forms['AddCar'].mark_name.choices = get_mark_list()
    forms['DeleteCar'].car_number.choices = get_client_cars()

    if request.method == 'POST':

        if 'new_car' in request.form:
            f = forms['AddCar']
            if f.validate():
                if add_car(f.mark_name.data, f.car_number.data):
                    flash('Новая машина добавлена')
                    return redirect('/personal')

        if 'del_car' in request.form:
            f = forms['DeleteCar']
            if f.validate():
                if delete_car(f.car_number.data):
                    flash('Новый бокс добавлен')
                    return redirect('/personal')

        if 'ticket_id_refuse' in request.form:
            phone = session['phone']
            ticket_id = int(request.form['ticket_id_refuse'])

            refuse_box(phone, ticket_id)

            return redirect('/personal')

    return render_template('personal.html', f=forms, tickets_active=ticket_active, tickets_not_active=ticket_not_active, client=client)


# ADMIN STUFF
@app.route('/admin_info', methods=['GET', 'POST'])
@admin_required
def admin_info():
    forms = {'ClientMarkInfo': ClientMarkInfo(request.form),
             'DateEndInfo': DateEndInfo(request.form),
             'BoxList': BoxList(request.form)}

    forms['ClientMarkInfo'].mark_name.choices = get_mark_list()
    forms['BoxList'].box_clients.choices = get_box_list()

    if request.method == 'POST':
        if 'get_list_c' in request.form:
            info_c = get_list_c()

            wb = xlwt.Workbook()
            ws = wb.add_sheet('Test')
            for i in range(len(info_c)):
                for j in range(len(info_c[i])):
                    ws.write(i, j, info_c[i][j])

            wb.save(PROJECT_ROOT + '\\report\\client.xls')

            return render_template('admin_info.html', f=forms, infs_c=info_c)

        elif 'get_list_cwm' in request.form:
            f = forms['ClientMarkInfo']
            if f.validate():
                info_cwm = get_list_cwm(f.mark_name.data)

                return render_template('admin_info.html', f=forms, infs_cwm=info_cwm)

        elif 'get_list_cde' in request.form:
            f = forms['DateEndInfo']
            if f.validate():
                info_cde = get_list_cde(datetime.strptime(f.date_end.data, '%d.%m.%Y').date())

                return render_template('admin_info.html', f=forms, infs_cde=info_cde)

        elif 'get_client' in request.form:  # получить владельца указанного бокса
            f = forms['BoxList']
            if f.validate():
                info_box = get_client_by_box(f.box_clients.data)

                return render_template('admin_info.html', f=forms, infs_box=info_box)

    return render_template('admin_info.html', f=forms)


@app.route('/admin_manage', methods=['GET', 'POST'])
@admin_required
def admin_manage():
    forms = {'NewBoxForm': NewBoxForm(request.form),
             'CloseBoxForm': CloseBoxForm(request.form),
             'UpdateBoxForm': UpdateBoxForm(request.form),
             'NewMarkForm': NewMarkForm(request.form),
             'DeleteMarkForm': DeleteMarkForm(request.form)}

    marks_list = get_mark_list()
    forms['NewBoxForm'].nb_mark_name.choices = marks_list
    forms['DeleteMarkForm'].dm_mark_name.choices = marks_list

    if request.method == 'POST':
        if 'new_box' in request.form:
            f = forms['NewBoxForm']
            if f.validate():
                if add_box(f.nb_mark_name.data, f.cost.data):
                    flash('Новый бокс добавлен')
                    return redirect('/admin_manage')

            else:
                flash('Проблема')

        elif 'close_box' in request.form:
            f = forms['CloseBoxForm']
            if f.validate():
                if close_box(f.cb_box_code.data):
                    flash('Бокс закрыт')
                    return redirect('/admin_manage')

                else:
                    flash('Такого бокса нет в списке')

        elif 'update_box' in request.form:
            f = forms['UpdateBoxForm']

            if f.validate():
                if update_box(float(f.u_cost.data.replace(',', '.'))):
                    flash('Цена обновлена.')
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

def set_sec_key(path):
    with open(path, 'r') as f:
        tmp = f.read()

    return tmp


if __name__ == '__main__':
    app.secret_key = 'true_sec_key'
    app.run(debug=True)

