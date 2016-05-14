from flask import Flask
from flask import render_template, redirect, \
    request, session, url_for, escape

from loginform import LoginForm


app = Flask(__name__)
#app.secret_key = 'WarWARWar'


@app.route('/')
@app.route('/Index.html')
def index():
    return render_template('index.html')


@app.route('/Registration.html')
def registration():
    return render_template('Registration.html')


@app.route('/Login.html', methods=['GET', 'POST'])
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
    app.run(debug=True, host='0.0.0.0')

