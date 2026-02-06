from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.users import User

from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
db_session.global_init("./db/mydatabase.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/nations')
def nantions():
    return render_template('narodi1.html')


@app.route('/nations2')
def nations2():
    return render_template('nations2.html')


@app.route('/monuments')
def monuments():
    return render_template('monuments.html')


@app.route('/facts')
def facts():
    return render_template('facts.html')


@app.route('/labyrinth', methods=['GET', 'POST'])
def labyrinth():
    if request.method == 'GET':
        return render_template('labyrinth.html')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        score = request.form.get('data')
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.score = max(user.score, int(score))
        db_sess.commit()
        return 'ok'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_repeat.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/leaderboard')
def leaderboard():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    a = []
    for el in users:
        a.append((el.score, el.surname + ' ' + el.name))
    a.sort(key=lambda x: (-x[0], x[1]))
    print(a)
    print(a[0][1])
    return render_template('leaderboard.html',b=a[0][1], a=a[1:10])


@app.route('/events')
def events():
    return render_template('events.html')


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
