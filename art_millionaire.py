import random
import glob
import os
import os.path
from flask import Flask, render_template, session, redirect, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import TextField, FileField
from wtforms.validators import Required
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)


def get_questions():
    question_files = glob.glob('questions/'+session['folder']+'/*.txt')
    session['question_len'] = len(question_files)
    questions = []
    for i in sorted(question_files):
        questions.append(open(i, 'r').read().splitlines())

    return questions


def create_answer_list(question_number):
    questions_extract = session['question_extract'][question_number]
    session['question'] = questions_extract[0]
    session['right_answer'] = questions_extract[1]
    answers = []
    answers.append(session['right_answer'])
    if '5050' in session and session['5050'] == question_number:
        answers.append(random.choice(questions_extract[-3:]))
    else:
        for i in questions_extract[-3:]:
            answers.append(i)

    random.shuffle(answers)

    image_question = '%s/%s/%s-q.jpg' % ('questions', session['folder'],
                                         question_number)
    if os.path.isfile(image_question):
        session['image_question'] = True
    else:
        session['image_question'] = False

    image_answer = '%s/%s/%s-a.jpg' % ('questions', session['folder'],
                                       question_number)
    if os.path.isfile(image_answer):
        session['image_answer'] = True
    else:
        session['image_answer'] = False

    return answers


@app.route('/images/<filename>')
def images(filename):
    return send_from_directory(app.root_path + '/questions/' + session['folder'],
                               filename)


@app.route('/')
def index():
    session.clear()
    folders = os.listdir('questions')

    return render_template('index.html', folders=folders)


@app.route('/art_millionaire/<folder>')
def folder(folder):
    session['folder'] = folder
    session['question_extract'] = get_questions()

    return render_template('folder.html')


@app.route('/art_millionaire/<folder>/<int:question_number>/question')
def question_number(folder, question_number):
    session['answers'] = create_answer_list(question_number)

    return render_template('question.html', folder=folder,
                           question_number=question_number)


@app.route('/art_millionaire/<folder>/<int:question_number>/result/<guess>')
def result(folder, question_number, guess):
    return render_template('result.html', folder=folder,
                           question_number=question_number,
                           guess=guess)


@app.route('/art_millionaire/<folder>/<int:question_number>/joker/audience')
def joker_audience(folder, question_number):
    session['audience'] = True

    return render_template('question.html', folder=folder,
                           question_number=question_number)


@app.route('/art_millionaire/<folder>/<int:question_number>/joker/phone')
def joker_phone(folder, question_number):
    session['phone'] = True

    return render_template('question.html', folder=folder,
                           question_number=question_number)


@app.route('/art_millionaire/<folder>/<int:question_number>/joker/5050')
def joker_5050(folder, question_number):
    session['5050'] = question_number
    session['answers'] = create_answer_list(question_number)

    return render_template('question.html', folder=folder,
                           question_number=question_number)


''' CREATOR '''


def write_question(directory, question_number, content):
    question_file = '%s/%s.txt' % (directory, question_number)
    file = open(question_file, 'w+')
    for i in content:
        file.write(i+'\n')
    file.close()


class CreateForm(Form):
    titel = TextField('Titel', validators=[Required()])


@app.route('/create', methods=('GET', 'POST'))
def create():
    form = CreateForm()
    if form.validate_on_submit():
        new_folder = form.titel.data

        if os.path.exists('questions/'+new_folder):
            return render_template('create.html', form=form)

        else:
            url = '/create/%s/0' % new_folder
            return redirect(url)

    return render_template('create.html', form=form)


class CreateQuestionForm(Form):
    question = TextField('Frage', validators=[Required()])
    right_answer = TextField('Richtige Antwort', validators=[Required()])
    fake_answer_1 = TextField('Falsche Antwort', validators=[Required()])
    fake_answer_2 = TextField('Falsche Antwort', validators=[Required()])
    fake_answer_3 = TextField('Falsche Antwort', validators=[Required()])


@app.route('/create/<titel>/<int:question_number>', methods=('GET', 'POST'))
def create_question(titel, question_number):
    form = CreateQuestionForm()
    if form.validate_on_submit():
        if question_number == 0:
            os.makedirs('questions/'+titel)

        question_content = []
        question_content.append(form.question.data)
        question_content.append(form.right_answer.data)
        question_content.append(form.fake_answer_1.data)
        question_content.append(form.fake_answer_2.data)
        question_content.append(form.fake_answer_3.data)

        write_question('questions/'+titel, question_number, question_content)

        url = '/create/%s/%s/upload_images' % (titel, question_number)
        return redirect(url)

    return render_template('create_question.html', titel=titel,
                           question_number=question_number,
                           form=form)


''' ALL THE UPLOAD FOO '''


class UploadImagesForm(Form):
    question_image = FileField('Bild zur Frage')
    answer_image = FileField('Bild zur Antwort')


@app.route('/create/<titel>/<int:question_number>/upload_images', methods=('GET', 'POST'))
def upload_images(titel, question_number):
    form = UploadImagesForm()
    UPLOAD_FOLDER = 'questions/%s' % titel
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if form.validate_on_submit():
        question_image = secure_filename(form.question_image.data.filename)
        if question_image:
            form.question_image.data.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                                       str(question_number)+'-q.jpg'))

        answer_image = secure_filename(form.answer_image.data.filename)
        if answer_image:
            form.answer_image.data.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                                     str(question_number)+'-a.jpg'))

        url = '/create/%s/%s' % (titel, question_number + 1)
        return redirect(url)

    return render_template('upload_images.html', titel=titel,
                           question_number=question_number,
                           form=form)


if __name__ == "__main__":
    app.run(debug=True)
