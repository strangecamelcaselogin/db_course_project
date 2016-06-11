from hashlib import sha256
from functools import wraps

import sqlite3 as lite

from flask import Flask
from flask import render_template, redirect, flash, \
    request, session, abort, g, url_for

from forms import LoginForm, RegForm, BoxForm, ServiceForm, MarkForm, RefForm, AdminForm

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


@app.route('/')
@app.route('/index')
def index():
    posts = [{'brand':'Mercedes', 'box': '1' }, {'brand':'Renault', 'box': '3'}]
    return render_template('index.html', x=42, posts=posts)


@app.route('/rent', methods=['GET', 'POST'])
@login_required
def service():
    form = ServiceForm(request.form)

    if request.method == 'POST':
        if form.validate():
            pass

        else:
            flash('not valid form: service')
    return render_template('rent.html', form=form)


@app.route('/personal', methods=['GET', 'POST'])
@login_required
def personal_area():
    return render_template('personal.html')


'''
@app.route('/info', methods=['GET', 'POST'])
@login_required
def ref():
    form = RefForm(request.form)
    if request.method == 'POST':
        if form.validate():
            pass

        else:
            flash('not valid form: reference')
    return render_template('info.html', form=form)
'''

@app.route('/admin_info', methods=['GET', 'POST'])
@admin_required
def admin_info():
    form = RefForm(request.form)
    if request.method == 'POST':
        if form.validate():
            pass

        else:
            flash('not valid form: reference')
    return render_template('admin_info.html', form=form)


@app.route('/admin_manage', methods=['GET', 'POST'])
@admin_required
def admin():
    form = AdminForm(request.form)
    if request.method == 'POST':
        if form.validate():
            pass

        else:
            flash('not valid form: box')
    return render_template('admin_manage.html', form=form)


'''
@app.route('/boxes', methods=['GET', 'POST'])
@admin_required
def box():
    form = BoxForm(request.form)
    if request.method == 'POST':
        if form.validate():
            pass

        else:
            flash('not valid form: box')
    return render_template('boxes.html', form=form)


@app.route('/brands', methods=['GET', 'POST'])
@admin_required
def mark():
    form = MarkForm(request.form)

    if request.method == 'POST':
        if form.validate():
            mark = form.mark_name.data

            con = lite.connect(DATABASE)
            with con:

                cur = con.cursor()

                cur.execute("SELECT * FROM Car_Brands WHERE Brand = :mark", {'mark': mark})

                if len(cur.fetchall()) == 0:
'''
                  #  cur.execute('''INSERT INTO Car_Brands (Brand)
                  #              VALUES (:mark)''',
                  #              {'mark': mark})
'''
                    flash('Марка добавлена.')
                    #return redirect('/index')

                else:
                    flash('Такая марка уже существует')

    return render_template('brands.html', form=form)
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():

            phone = form.phone.data
            hashed_password = sha256(form.password.data.encode('utf-8')).hexdigest()

            con = lite.connect(DATABASE)
            with con:
                cur = con.cursor()
                cur.execute('''SELECT  * FROM Clients WHERE Phone = :phone AND Password = :password''',
                            {'phone': phone, 'password': hashed_password})

                data = cur.fetchall()

                if len(data) == 1:
                    session['logged_in'] = True
                    session['phone'] = phone
                    if phone == ADMIN:
                        session['is_admin'] = True

                    flash('Вы вошли как {}'.format(phone))
                    return redirect('/index')

            flash('Неверное имя пользователя или пароль.')

        else:
            flash('Что-то пошло не так...')

    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)

    if request.method == 'POST':
        if form.validate():
            phone = form.phone.data
            hashed_password = sha256(form.password.data.encode('utf-8')).hexdigest()

            f_name = form.name.data
            s_name = form.second_name.data
            m_name = form.mid_name.data
            address = form.address.data

            con = lite.connect(DATABASE)
            with con:
                cur = con.cursor()

                cur.execute("SELECT * FROM Clients WHERE Phone = :phone", {'phone': phone})

                if len(cur.fetchall()) == 0:

                    cur.execute('''INSERT INTO Clients (Second_Name, First_Name, Middle_Name, Address, Phone, Password)
                                VALUES (:s_name, :f_name, :m_name, :address, :phone, :password)''',
                                {'s_name': s_name,
                                 'f_name': f_name,
                                 'm_name': m_name,
                                 'address': address,
                                 'phone': phone,
                                 'password': hashed_password})

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

