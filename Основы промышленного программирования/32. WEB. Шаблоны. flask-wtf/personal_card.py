import json
import os

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired

app = Flask(__name__)
secret_key = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = str(secret_key)


class LoginForm(FlaskForm):
    username_astro = StringField('Id астронавта', validators=[DataRequired()])
    password_astro = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username_cap = StringField('Id капитана', validators=[DataRequired()])
    password_cap = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/', defaults={'title': 'MarsOne'})
@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<profession>')
def training(profession):
    if 'инженер' in profession or 'строитель' in profession:
        profession_type = 'инженер'
    else:
        profession_type = 'ученый'
    return render_template('training.html', profession_type=profession_type)


@app.route('/list_prof/<list_type>')
def list_professions(list_type):
    professions = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
                   'инженер по терраформированию', 'климатолог', 'специалист по радиационной защите',
                   'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения', 'метеоролог',
                   'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов']
    return render_template('professions.html', list_type=list_type, professions=professions)


def get_answers():
    answers = {
        "title": "Анкета",
        "surname": "Watny",
        "name": "Mark",
        "education": "выше среднего",
        "profession": "штурман марсохода",
        "sex": "male",
        "motivation": "Всегда мечтал застрять на Марсе!",
        "ready": "True",
    }
    questions_to_display = {
        "surname": "Фамилия",
        "name": "Имя",
        "education": "Образование",
        "profession": "Профессия",
        "sex": "Пол",
        "motivation": "Мотивация",
        "ready": "Готовы остаться на марсе",
    }
    answers_display = {}
    for k, v in answers.items():
        k = questions_to_display.get(k, k)
        answers_display[k] = v
    return answers_display


@app.route('/auto_answer')
@app.route('/answer')
def answer():
    answers = get_answers()
    title = answers.pop('title')
    return render_template('auto_answer.html', title=title, answers=answers)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/distribution')
def distribute():
    astronauts = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни',
                  'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    return render_template('distribution.html', astronauts=astronauts)


@app.route('/table/<sex>/<int:age>')
def table(sex: str, age: int):
    return render_template('design.html', sex=sex, age=age)


def get_image_paths(base_path):
    # пути относительно static
    return [f"img/gallery/{i}" for i in os.listdir(base_path)]


class GalleryForm(FlaskForm):
    photo = FileField('Добавить картинку', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    image_base_path = 'static/img/gallery'
    if request.method == 'GET':
        form = GalleryForm()
        image_paths = get_image_paths(image_base_path)
        return render_template('gallery.html', image_paths=image_paths, form=form)
    elif request.method == 'POST':
        file = request.files['photo']
        with open(os.path.join(image_base_path, file.filename), 'wb') as f:
            f.write(file.stream.read())
        return redirect('/gallery')


@app.route('/member')
def member():
    with open('templates/members.json', 'r', encoding='utf8') as f:
        members = json.load(f)['members']
    return render_template('member.html', members=members)


if __name__ == '__main__':
    app.run("", 8080)
