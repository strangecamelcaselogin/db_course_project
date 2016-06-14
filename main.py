from functools import wraps

from flask import Flask
from flask import render_template, redirect, flash, \
    request, session, abort, g, url_for

from sql_core import login, register, add_box, close_box, add_mark, form_mark_list, delete_mark, rent_, refuse, update_box, \
    get_list_cwm, get_list_cde, form_ticket_list, get_list_c

from forms import LoginForm, RegistrationForm, RentForm, RefuseForm, AdminInfo, \
    NewBoxForm, CloseBoxForm, NewMarkForm, DeleteMarkForm, UpdateBoxForm, ClientMarkInfo, DateEndInfo

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
    posts = form_mark_list()
    return render_template('index.html', x=42, posts=posts)


# RENT BOX
@app.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    mark = dict()

    forms = dict()
    forms['RentForm'] = RentForm()
    forms['RefuseForm'] = RefuseForm()

    if request.method == 'POST':
        if 'rent' in request.form:
            forms['RentForm'] = RentForm(request.form)
            form = forms['RentForm']
            if form.validate():
                if rent_(form):
                    flash('Вы арендовали бокс')
                else:
                    flash('К сожалению, на данный момент свободных боксов нет')

            forms['RentForm'] = RentForm()

        elif 'refuse' in request.form: # ???
            forms['RefuseForm'] = RefuseForm(request.form)
            form = forms['RefuseForm']
            if form.validate():
                pass
                forms['RefuseForm'] = RefuseForm()

    return render_template('rent.html', f=forms)


# PERSONAL
@app.route('/personal', methods=['GET', 'POST'])
@login_required
def personal_area():
    ticket = form_ticket_list()

    return render_template('personal.html', ts = ticket)


# ADMIN STUFF
@app.route('/admin_info', methods=['GET', 'POST'])
@admin_required
def admin_info():
    info_cwm = dict()
    info_cde = dict()
    info_c = dict()

    forms = dict()
    forms['ClientMarkInfo'] = ClientMarkInfo()
    forms['DateEndInfo'] = DateEndInfo()

    if request.method == 'POST':
        if 'get_list_c' in request.form:
            info_c = get_list_c()

            return render_template('admin_info.html', f=forms, infs_c=info_c)

        if 'get_list_cwm' in request.form:
            forms['ClientMarkInfo'] = ClientMarkInfo(request.form)
            f = forms['ClientMarkInfo']
            if f.validate():
                info_cwm = get_list_cwm(f)

            forms['ClientMarkInfo'] = ClientMarkInfo()

            return render_template('admin_info.html', f=forms, infs_cwm=info_cwm)

        elif 'get_list_cde' in request.form:
            forms['DateEndInfo'] = DateEndInfo(request.form)
            f = forms['DateEndInfo']
            if f.validate():
                info_cde = get_list_cde(f)

            forms['DateEndInfo'] = DateEndInfo()

            return render_template('admin_info.html', f=forms, infs_cde=info_cde)


    return render_template('admin_info.html', f=forms)




@app.route('/admin_manage', methods=['GET', 'POST'])
@admin_required
def admin_manage():

    forms = dict()
    forms['NewBoxForm'] = NewBoxForm()
    forms['CloseBoxForm'] = CloseBoxForm()
    forms['UpdateBoxForm'] = UpdateBoxForm()
    forms['NewMarkForm'] = NewMarkForm()
    forms['DeleteMarkForm'] = DeleteMarkForm()

    if request.method == 'POST':
        if 'new_box' in request.form:
            forms['NewBoxForm'] = NewBoxForm(request.form)
            print('nb')
            f = forms['NewBoxForm']
            if f.validate():
                if add_box(f):
                    flash('Новый бокс добавлен')
                else:
                    flash('Такой марки нет в списке')

            forms['NewBoxForm'] = NewBoxForm()

        elif 'close_box' in request.form:
            forms['CloseBoxForm'] = CloseBoxForm(request.form)
            print('cb')
            f = forms['CloseBoxForm']
            if f.validate():
                if close_box(f):
                    flash('Бокс закрыт')
                else:
                    flash('Такого бокса нет в списке')

            forms['CloseBoxForm'] = CloseBoxForm()

        elif 'update_box' in request.form:
            forms['UpdateBoxForm'] = UpdateBoxForm(request.form)
            f = forms['UpdateBoxForm']
            if f.validate():
                if update_box(f):
                    flash('Маша не может в буковы')
                else:
                    flash('Такого бокса нет в списке')

            forms['UpdateBoxForm'] = UpdateBoxForm()

        elif 'new_mark' in request.form:
            forms['NewMarkForm'] = NewMarkForm(request.form)
            print('nm')
            f = forms['NewMarkForm']
            if f.validate():
                if add_mark(f.nm_mark_name.data):  # DONE
                    flash('Марка добавлена.')

                else:
                    flash('Такая марка уже существует')

            forms['NewMarkForm'] = NewMarkForm()

        elif 'del_mark' in request.form:
            forms['DeleteMarkForm'] = DeleteMarkForm(request.form)
            print('dm')
            f = forms['DeleteMarkForm']
            if f.validate():
                if delete_mark(f.dm_mark_name.data):  # DONE
                    flash('Марка удалена')

                else:
                    flash('Какой то косяк')

            forms['DeleteMarkForm'] = DeleteMarkForm()

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

