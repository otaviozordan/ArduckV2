from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user
from app.models.userModel import Usuario, buscar_email
import json

@app.route('/login', methods=['POST'])
def login():
    response = {}
    body = request.get_json()
    try:
        email = body['email']
        password = body['password']
    except Exception as e:
        response['login'] = False
        response['erro'] = str(e)   
        response['Retorno'] = 'Parametros invalidos ou ausentes'                
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    # Consultar o usuário no MongoDB com base no email
    user = buscar_email(email)
    if user and user.verify_password(password):
        login_user(user)  # Autenticar o usuário com o Flask-Login
        response['login'] = True
        response['usuario'] = user.to_json()
        return Response(json.dumps(response), status=200, mimetype="application/json")
    else:
        response['login'] = False
        response["mensagem"] = "Usuario ou senha incorreta"
        return Response(json.dumps(response), status=401, mimetype="application/json")
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    response = {"login": False, "Mensagem:":"Usuario desconectado"}
    return Response(json.dumps(response), status=200, mimetype="application/json")
