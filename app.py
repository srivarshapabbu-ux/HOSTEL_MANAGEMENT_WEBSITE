from flask import Flask, render_template, request,jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # (Optional) Replace with your actual secret key

# For creating or updating database if you want to add new user
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.String(30), primary_key=True)  # Unique ID for each student/parent/staff
#     password = db.Column(db.String(20), nullable=False)
    
# # Initialize Database within Application Context
# with app.app_context():
#     db.create_all()
    
# Database Configuration
def get_db():
    conn = sqlite3.connect('sru_hostel.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
# This route serves the main page (mandatory for any web page)
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_page():
    role = request.args.get('role')
    if role not in ['student', 'warden', 'parent']:
        return redirect(url_for('index'))

    return render_template('login.html', role=role)


@app.route('/login', methods=['POST'])
def login():
    identifier = request.form['identifier'] # email OR ID
    password = request.form['password']
    
    role = request.form.get('role')

    if role not in ['student', 'warden', 'parent']:
        return redirect(url_for('index'))

    # Check: Validate user credentials from DB
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE (LOWER(email) = LOWER(?) OR LOWER(id) = LOWER(?)) AND password=? AND role=?",
        (identifier, identifier, password, role)
    ).fetchone()
    conn.close()

    if not user:
        flash("Invalid ID/Email or Password!", "error")  # flash message
        return redirect(url_for('login_page', role=role))

    session['role'] = role
    session['user'] = identifier

    if role == 'student':
        return redirect(url_for('student'))
    elif role == 'warden':
        return redirect(url_for('warden'))
    else:
        return redirect(url_for('parent'))


@app.route('/student')
def student():
    if session.get('role') != 'student':
        return redirect(url_for('index'))
    return render_template('student.html')


@app.route('/warden')
def warden():
    if session.get('role') != 'warden':
        return redirect(url_for('index'))
    return render_template('warden.html')


@app.route('/parent')
def parent():
    if session.get('role') != 'parent':
        return redirect(url_for('index'))
    return render_template('parent.html')

@app.route('/logout')
def logout():
    session.clear()          # removes all session data
    return redirect(url_for('index'))

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000)