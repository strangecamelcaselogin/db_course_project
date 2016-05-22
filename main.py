from flask import Flask
from flask import render_template, redirect, flash, \
    request, session, url_for, escape

from loginform import LoginForm, RegForm, BoxForm, ServiceForm, MarkForm, RefForm


app = Flask(__name__)


# TODO LOGIN DECORATOR
# TODO MORE SHIT!


@app.route('/')
@app.route('/index')
def index():
    flash('Hey there! I am flash message!')
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)

    if request.method == 'POST':
        if form.validate():

            flash('registered')
            return redirect('/index')

        else:
            flash('form not valid')

    return render_template("Registration.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():
            flash('logined:')
            #print(request.form['login'], request.form['password'])
            redirect('/index')

        else:
            flash('Что-то пошло не так...')

    return render_template('Login.html', form=form)


@app.route('/box', methods=['GET', 'POST'])
def box():
    form = BoxForm(request.form)
    if request.method == 'POST':
        if form.validate():
            flash('logined:')
            #print(request.form['cod_name'])

        else:
            flash('not valid form: box')
    return render_template('Box.html', form=form)


@app.route('/mark', methods=['GET', 'POST'])
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

    return render_template('Mark.html', form=form)


@app.route('/service', methods=['GET', 'POST'])
def service():
    form = ServiceForm(request.form)

    if request.method == 'POST':
        if form.validate():
            print(request.form['cod_owner'])

        else:
            flash('not valid form: service')
    return render_template('Service.html', form=form)


@app.route('/ref', methods=['GET', 'POST'])
def ref():
    form = RefForm(request.form)
    if request.method == 'POST':
        if form.validate():
            pass

        else:
            flash('not valid form: reference')
    return render_template('Ref.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'wtf_dude_its_a_public_secret_key!!'  # !!!!!!!!!
    app.run(debug=True)

