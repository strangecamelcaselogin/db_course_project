from flask import Flask
from flask import render_template, redirect, \
    request, session, url_for, escape

from loginform import LoginForm, RegForm, BoxForm, ServiceForm, MarkForm, RefForm


app = Flask(__name__)



@app.route('/Index.html')
def main():
    return redirect('/')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/box', methods=['GET', 'POST'])
def box():
    form = BoxForm(request.form)
    if request.method == 'POST':
        if form.validate():
            print('logined:')
            print(request.form['cod_name'])

        else:
            print('not valid')
    return render_template('Box.html', form=form)


@app.route('/service', methods=['GET', 'POST'])
def service():
    form = ServiceForm(request.form)
    if request.method == 'POST':
        if form.validate():
            print('logined:')
            print(request.form['cod_owner'])

        else:
            print('not valid')
    return render_template('Service.html', form=form)

@app.route('/ref', methods=['GET', 'POST'])
def ref():
    form = RefForm(request.form)
    if request.method == 'POST':
        if form.validate():
            print('logined:')
            # print(request.form['cod_owner'])

        else:
            print('not valid')
    return render_template('Ref.html', form=form)


@app.route('/mark', methods=['GET', 'POST'])
def mark():
    form = MarkForm(request.form)
    #opt_list = list('345982')

    if request.method == 'POST':
        if form.validate():
            print('logined:')
            #print(request.form['cod_owner'])

        else:
            print('not valid')
    return render_template('Mark.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)
    if request.method == 'POST':
        if form.validate():
            print('logined:')
            print(request.form['name'], request.form['mid_name'], request.form['second_name'], request.form['adress'])

        else:
            print('not valid')
    return render_template("Registration.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():
            print('logined:')
            print(request.form['login'], request.form['password'])

        else:
            print('not valid')

    return render_template('Login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

