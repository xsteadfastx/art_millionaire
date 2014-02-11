import random
import glob
import sys
import os.path
from flask import Flask, render_template, session, redirect
from flask_bootstrap import Bootstrap


app = Flask(__name__, static_folder=sys.argv[1])
Bootstrap(app)

directory = sys.argv[1]

def get_questions():
    questions = []
    for file in sorted(glob.glob(directory+'/*.txt')):
        questions.append(open(file, 'r').read().splitlines())

    return questions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<int:question_number>/question')
def question_number(question_number):
    questions_extract = get_questions()[question_number]
    session['question'] = questions_extract[0]
    session['right_answer'] = questions_extract[1]
    answers = []
    for i in questions_extract[-4:]:
        answers.append(i)

    random.shuffle(answers)
    session['answers'] = answers

    session['image_file'] = '%s/%s.jpg' % (directory, question_number)
    if os.path.isfile(session['image_file']):
        session['image'] = True
    else:
        session['image'] = False

    return render_template('question.html', question_number=question_number) 


@app.route('/<int:question_number>/result/<guess>')
def result(question_number, guess):
    return render_template('result.html', question_number=question_number, 
                           guess=guess)


@app.route('/<int:question_number>/joker/<phone_or_audience>')
def joker_phone_audience(question_number, phone_or_audience):
    if phone_or_audience == 'phone':
        session['phone'] = True
    elif phone_or_audience == 'audience':
        session['audience'] = True
    else:
        pass

    url = '/%s/question' % (question_number)
    return redirect(url) 


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
