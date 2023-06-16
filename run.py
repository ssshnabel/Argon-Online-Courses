from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
# from wtforms import 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask('__Argon_Online_Courses__')
app.config['SECRET_KEY'] = os.urandom(16)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Argon-online-courses.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
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

    def set_hashed_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def make_login():
    if request.method == 'POST':
        user_email = request.form['userEmail']
        password = request.form['password']

        user = User.query.filter_by(email=user_email).first()
        if user and user.check_password(password):
            if user.role == 'teacher':
                login_user(user)
                return redirect(url_for('show_teacher_main_page'))
            else:
                login_user(user)
                return redirect(url_for('show_student_main_page'))
        else:
            return render_template('sign_in.html', error="Invalid email or password")
    
    return render_template('sign_in.html')


@app.route('/logout')
@login_required
def make_logout():
    logout_user()
    return redirect(url_for('make_login'))


@app.route('/teacher_main_page', methods=['GET', 'POST'])
@login_required
def show_teacher_main_page():
    return render_template('sign_up.html', user=current_user)


@app.route('/student_main_page', methods=['GET', 'POST'])
@login_required
def show_student_main_page():
    return render_template('sign_up.html', user=current_user)

app.run(host="0.0.0.0", port="81")
 