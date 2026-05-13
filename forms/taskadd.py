from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class CreateTaskForm(FlaskForm):
    question = StringField("Вопрос", validators=[DataRequired()])
    answer1 = StringField("Вариант ответа 1", validators=[DataRequired()])
    answer2 = StringField("Вариант ответа 2", validators=[DataRequired()])
    answer3 = StringField("Вариант ответа 3", validators=[DataRequired()])
    correct = IntegerField("Индекс правильного ответа(от нуля)", validators=[DataRequired()])
    tag_id = IntegerField("Индекс тега", validators=[DataRequired()])
    submit = SubmitField("Создать задание")