art_millionair
==============

This is a webapp for playing a 'who wants to be a millionair'-like game with custom questions. 

![Screenshot](screenshot.png)

## Installation ##
1. `virtualenv -p /usr/bin/python3 art_millionair`
2. `cd art_millionair`
3. `. bin/activate`
4. `git clone https://github.com/xsteadfastx/art_millionair.git`
5. `cd art_millionair`
6. `pip install -r requirements.txt`

## Questions ##
1. create a folder in the questions-directory
2. put in text files from 0.txt to 5.txt.

### Images ###
if you want to add a question or a answer image or both: just drop a jpg-file in the folder. for example:
- for a image displayed on the question-page: **0-q.jpg**
- for a image displayed on the answer-page: **0-a.jpg**

### Fileformat ###
its just a text file
- first line: question
- second line: right answer
- third to fifth line: fake answers

## Running ##
1. `python art_millionair.py`
2. point your browser to http://localhost:5000

## Powered by ##
- [flask](http://flask.pocoo.org/)
- [flask_bootstrap](https://github.com/mbr/flask-bootstrap)
- [TimeCircles](https://github.com/wimbarelds/TimeCircles)
- Cola Light
