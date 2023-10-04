from app import app
from flask import render_template, redirect, send_from_directory
from flask_login import current_user, login_required
from app.controllers import authenticate

@app.route('/')
def index():
    auth = authenticate("professor")
    if auth:
        return redirect("/login")
    return redirect("/home")

@app.route('/login', methods=['GET'])
def login_render():
    return render_template('auth/login.html') 

@app.route('/signup', methods=['GET'])
def signup_render():
    return render_template('auth/signup.html') 

@app.route('/home',  methods=['GET'])
def home_render():
    auth = authenticate("professor")
    if auth:
        return redirect("/login")

    return render_template('home/index.html')

@app.route('/build',  methods=['GET'])
def build_trilha():
    auth = authenticate("professor")
    if auth:
        return redirect("/login")

    return render_template('src/index.html')
