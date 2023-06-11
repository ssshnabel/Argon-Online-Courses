from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask('__Argon_Online_Courses__')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Argon-online-courses.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fisrt_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    theme = db.Column(db.String(10), nullable=True)
    notifications = db.Column(db.String(5), nullable=True)
    role = db.Column(db.String(50),nullable=False)


@app.route('/', methods=['GET', 'POST'])
def show_sign_in():

    if request.method == 'POST':
        # testing_teacher = User(
        #     fisrt_name = 'John',
        #     last_name = 'Doe',
        #     patronymic = None,
        #     email ='john.doe@example.com',
        #     password_hash ='hashed_password',
        #     birthday ='1990-01-01',
        #     city = 'New York',
        #     theme = 'light',
        #     notifications = 'off',
        #     role = 'teacher'
        # )
        # db.session.add(testing_teacher)
        # db.session.commit()

        user_email = request.form['userEmail']
        password = request.form['password']

        user = User.query.filter_by(email=user_email).first()
        if user:
            hashed_password = user.password_hash

        return render_template('sign_up.html', password=hashed_password)
    
    if request.method =="GET":
        return render_template('sign_in.html')
app.run(host="0.0.0.0", port="81")
 