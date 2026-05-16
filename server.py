from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from sqlalchemy import func

import json
from data import db_session
from data.users import User
from data.tasks import Task

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.taskadd import CreateTaskForm

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


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
        db_sess = db_session.create_session()
        voprosi = db_sess.query(Task).order_by(func.random()).limit(5).all()
        print(voprosi)
        questions = [{"question": q.question, "answers": [q.answer1, q.answer2, q.answer3], "correct": q.correct} for q
                     in voprosi]
        db_sess.close()
        return render_template('labyrinth.html', voprosi=questions)
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


@login_required
@app.route('/createtask', methods=["GET", "POST"])
def createtask():
    form = CreateTaskForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        task = Task(
            question=form.question.data,
            answer1=form.answer1.data,
            answer2=form.answer2.data,
            answer3=form.answer3.data,
            correct=form.correct.data,
            tag_id=form.tag_id.data,
            user_id=current_user.id
        )
        db_sess.add(task)
        db_sess.commit()
        return redirect('/')
    return render_template('createtask.html', form=form)


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
    return render_template('leaderboard.html', b=a[0][1], a=a[1:10])


@app.route('/events')
def events():
    with open("./data/events.json", encoding='utf-8') as f:
        events = json.load(f)
    return render_template('events.html', events=events)


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
