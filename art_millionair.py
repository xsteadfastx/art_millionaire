import random
import glob
import os
import os.path
from flask import Flask, render_template, session, redirect, send_from_directory
from flask_bootstrap import Bootstrap


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

    image_file = '%s/%s/%s.jpg' % ('questions', session['folder'],
                                   question_number)
    if os.path.isfile(image_file):
        session['image'] = True
    else:
        session['image'] = False

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


@app.route('/art_millionair/<folder>')
def folder(folder):
    session['folder'] = folder
    session['question_extract'] = get_questions()

    return render_template('folder.html')


@app.route('/art_millionair/<folder>/<int:question_number>/question')
def question_number(folder, question_number):
    session['answers'] = create_answer_list(question_number)

    return render_template('question.html', folder=folder,
                           question_number=question_number)


@app.route('/art_millionair/<folder>/<int:question_number>/result/<guess>')
def result(folder, question_number, guess):
    return render_template('result.html', folder=folder,
                           question_number=question_number,
                           guess=guess)


@app.route('/art_millionair/<folder>/<int:question_number>/joker/audience')
def joker_audience(folder, question_number):
    session['audience'] = True

    return render_template('question.html', folder=folder,
                           question_number=question_number)


@app.route('/art_millionair/<folder>/<int:question_number>/joker/phone')
def joker_phone(folder, question_number):
    session['phone'] = True

    return render_template('phone.html', folder=folder,
                           question_number=question_number)


@app.route('/art_millionair/<folder>/<int:question_number>/joker/5050')
def joker_5050(folder, question_number):
    session['5050'] = question_number
    session['answers'] = create_answer_list(question_number)

    return render_template('question.html', folder=folder,
                           question_number=question_number)


if __name__ == "__main__":
    app.run(debug=True)
