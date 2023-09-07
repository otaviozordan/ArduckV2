from app import app
from flask import render_template, redirect, send_from_directory
from flask_login import current_user, login_required

@login_required
@app.route('/')
def index():
    return redirect("/login")

@app.route('/login', methods=['GET'])
def login_render():
    return render_template('auth/login.html') 

@app.route('/signup', methods=['GET'])
def signup_render():
    return render_template('auth/signup.html') 

@app.route('/home',  methods=['GET'])
def home_render():
    try:
        if current_user.privilegio not in ['administrador', 'professor']:
            return redirect("/login")
        return render_template('home/index.html')
    except:
        return redirect("/login")
