import cv2
import numpy as np

from face_recognition import face_encodings

import face_recognition
from flask import Flask, request, render_template, redirect, session, Response
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from camera import Video

import face_recognition

from simple_facerec import SimpleFacerec

sfr = SimpleFacerec()
df = Video()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)

    return redirect('/login')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type:  image/jpeg\r\n\r\n' + frame +
               b'\r\n\r\n')


@app.route('/Face Detection')
def face_detection():
    return render_template('Face Detection.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    return Response(gen(Video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html', face_names=df.name())


if __name__ == '__main__':
    app.run(debug=False)
