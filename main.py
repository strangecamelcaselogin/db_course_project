from flask import Flask
from flask import render_template
from flask import session, redirect, url_for, escape, request

from loginform import LoginForm
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate():
            print('logined:')
            print(request.form['login'], request.form['password'])

        else:
            print('not valid')

    return render_template('index.html', form=form)


@app.route('/Index.html')
def main():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

