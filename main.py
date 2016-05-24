import os
from functools import wraps

from flask import Flask
from flask import render_template, redirect, flash, \
    request, session, g, url_for

import sqlite3 as lite

from loginform import LoginForm, RegForm, BoxForm, ServiceForm, MarkForm, RefForm


app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'base.db')


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
        if session['phone'] == '00000000':
            return f(*args, **kwargs)
        else:
            flash('Вы не админ')
            return redirect('/index')

    return wrapper


################################################


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    flash(vars(request))
    form = BoxForm(request.form)
    return render_template('admin.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():

            phone = form.phone.data
            password = form.password.data

            con = lite.connect(DATABASE)
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users WHERE Phone = :phone AND Password = :pass",
                                {'phone': phone, 'pass': password})

                data = cur.fetchall()

                if len(data) != 0:
                    session['logged_in'] = True
                    session['phone'] = phone

                    flash('Вошли как {}'.format(phone))
                    return redirect('/index')

            flash('Неверное имя пользователя или пароль.')

        else:
            flash('Что-то пошло не так...')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Вы вышли из системы.')

    return redirect('/index')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)

    if request.method == 'POST':
        if form.validate():
            phone = form.phone.data
            password = form.password.data

            con = lite.connect(DATABASE)
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users WHERE Phone = :phone", {'phone':phone})

                if len(cur.fetchall()) == 0:
                    cur.execute("INSERT INTO Users VALUES (?,?)", (phone, password))
                    flash('Вы зарегестрированы.')
                    return redirect('/index')

                else:
                    flash('Такой пользователь уже существует.')

    return render_template("registration.html", form=form)


@app.route('/box', methods=['GET', 'POST'])
@login_required
@admin_required
def box():
    form = BoxForm(request.form)
    if request.method == 'POST':
        if form.validate():
            flash('logined:')
            #print(request.form['cod_name'])

        else:
            flash('not valid form: box')
    return render_template('box.html', form=form)


@app.route('/mark', methods=['GET', 'POST'])
@login_required
@admin_required
def mark():
    form = MarkForm(request.form)

    if request.method == 'POST':

        try:
            if request.form.get('mark_name') is not None:
                print(request.form['mark_name'])
            else:
                print('nope mark name')

            if request.form.get('mark_list') is not None:
                print(request.form['mark_list'])
            else:
                print('nope mark list')
        except Exception as e:
            flash('error: ', e)

    return render_template('mark.html', form=form)


@app.route('/service', methods=['GET', 'POST'])
@login_required
def service():
    form = ServiceForm(request.form)

    if request.method == 'POST':
        if form.validate():
            print(request.form['cod_owner'])

        else:
            flash('not valid form: service')
    return render_template('service.html', form=form)


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


##########################################################


if __name__ == '__main__':
    app.secret_key = 'wtf_dude_its_a_public_secret_key!!'  # !!!!!!!!!
    app.run(debug=True)

