from flask import Flask
from flask import render_template, redirect, \
    request, session, url_for, escape

from loginform import LoginForm


app = Flask(__name__)



@app.route('/Index.html')
def main():
    return redirect('/')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/box')
def box():
    return render_template('Box.html')


@app.route('/service')
def service():
    return render_template('Service.html')

@app.route('/ref')
def ref():
    return render_template('Ref.html')


@app.route('/mark')
def mark():
    return render_template('Mark.html')


@app.route('/registration')
def registration():
    return render_template("Registration.html")


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

