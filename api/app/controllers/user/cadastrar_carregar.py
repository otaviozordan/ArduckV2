from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from validate_email_address import validate_email
from app.models.userModel import Usuario
from app.models.trilhaModel import Trilha, buscar_trilhas_por_colecao, listar_nomes_colecoes_por_turma
import json

@app.route('/signup', methods=['POST'])
def signup():
    response = {}
    body = request.get_json()
    try:
        email = body['email']
        if not validate_email(email):
            response['login'] = False
            response['Retorno'] = 'Email inválido'                
            return Response(json.dumps(response), status=400, mimetype="application/json")
      
        password = body['password']
        nome = body['nome']
        turma = body['turma']
        privilegio = body['privilegio']

    except Exception as e:
        response['login'] = False
        response['erro'] = str(e)   
        response['Retorno'] = 'Parametros invalidos ou ausentes'                
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    try:
        user_data = {
            'nome':nome,
            'email':email,
            'password':password,
            'privilegio':privilegio,
            'turma':turma
        }
        usuario = Usuario(user_data=user_data)
        usuario.save()

        #Sincroniza permissoes das trilhas existentes dependendo se a trilha tem progressivo
        colecoes = listar_nomes_colecoes_por_turma(turma=turma)
        for colecao in colecoes:
            trilhas = buscar_trilhas_por_colecao(turma=turma, colecao=colecao)
            for trilha in trilhas:
                trilha_obj = Trilha.load_trilha_nome(
                    turma=turma, 
                    colecao=colecao,
                    nome=trilha
                    )
                if trilha.options.progressivo:
                    trilha_obj.syncpermissoes(usuario=email, habilitado=False)
                else:
                    trilha_obj.syncpermissoes(usuario=email, habilitado=True)

        return Response(json.dumps(response), status=400, mimetype="application/json")

    except Exception as e:
        response['login'] = False
        response['erro'] = str(e)   
        response['Retorno'] = 'Erro ao salvar usuário'                
        return Response(json.dumps(response), status=500, mimetype="application/json")

@login_required
@app.route('/buscarusuarios_turma', methods=['GET'])
def buscarusuarios_turma():
    turma = current_user.turma
    usuarios = Usuario.listar_usuarios_por_turma(turma=turma)
    return Response(json.dumps({'usuarios':usuarios}), status=500, mimetype="application/json")

@app.route('/buscarusuarios', methods=['GET'])
def buscarusuarios():
    usuarios = Usuario.listar_usuarios()
    return Response(json.dumps({'usuarios':usuarios}), status=500, mimetype="application/json")