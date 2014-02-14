import random
import glob
import os
import os.path
from flask import Flask, render_template, session, redirect, send_from_directory
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)


def get_questions():
    questions = []
    for i in sorted(glob.glob('questions/'+session['folder']+'/*.txt')):
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


@app.route('/<folder>')
def folder(folder):
    session['folder'] = folder
    session['question_extract'] = get_questions()

    return render_template('folder.html')


@app.route('/<folder>/<int:question_number>/question')
def question_number(folder, question_number):
    session['answers'] = create_answer_list(question_number)

    return render_template('question.html', folder=folder,
                           question_number=question_number)


@app.route('/<folder>/<int:question_number>/result/<guess>')
def result(folder, question_number, guess):
    return render_template('result.html', folder=folder,
                           question_number=question_number,
                           guess=guess)


@app.route('/<folder>/<int:question_number>/joker/<phone_or_audience>')
def joker_phone_audience(folder, question_number, phone_or_audience):
    if phone_or_audience == 'phone':
        session['phone'] = True
    elif phone_or_audience == 'audience':
        session['audience'] = True
    else:
        pass

    return render_template('question.html', folder=folder,
                           question_number=question_number)


@app.route('/<folder>/<int:question_number>/joker/5050')
def joker_5050(folder, question_number):
    session['5050'] = question_number
    session['answers'] = create_answer_list(question_number)

    return render_template('question.html', folder=folder,
                           question_number=question_number)


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
