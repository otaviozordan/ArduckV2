from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from validate_email_address import validate_email
from app.models.userModel import *
from app.models.trilhaModel import *
from app.controllers import authenticate
from app.controllers.mensagens import erro_msg
import json

@app.route('/signup', methods=['POST'])
def signup():
    response = {}
    body = request.get_json()
    try:
        email = body['email']
        if not validate_email(email):
            response['login'] = False
            response['Retorno'] = 'Email invalido'                
            return Response(json.dumps(response), status=400, mimetype="application/json")
      
        # Verificar se o email já existe no banco de dados
        if email_existe(email):
            response['login'] = False
            response['Retorno'] = 'Email ja existe'
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
        password = body['password']
        nome = body['nome']

        if 'turma' in body:
            turma = body['turma']
        else:
            turma = 'demo'

        if 'privilegio' in body:
            privilegio = body['privilegio']
        else:
            privilegio = 'aluno'


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

    except Exception as e:
        response['login'] = False
        response['erro'] = str(e)   
        response['Retorno'] = 'Erro ao salvar usuario'
        usuario.delet()            
        return Response(json.dumps(response), status=500, mimetype="application/json")
    
    try:
        ##Sincroniza permissoes das trilhas existentes dependendo se a trilha tem progressivo
        #colecoes = listar_nomes_colecoes_por_turma(turma=turma)
        #for colecao in colecoes:
        #    trilhas = listar_trilhas_por_colecao(turma=turma, colecao=colecao)
        #    for trilha_nome in trilhas:
        #        trilha_obj = load_trilha_por_colecao_nome(turma=turma, colecao=colecao, nome=trilha_nome)
        #        trilha_obj.syncprogresso(usuario=email)
#
        #        if trilha_obj.progressivo:
        #            trilha_obj.syncpermissoes(usuario=email, habilitado=False)
        #        else:
        #            trilha_obj.syncpermissoes(usuario=email, habilitado=True)
        response = {'create':True, 'usuario':usuario.to_json()}
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response['login'] = False
        response['erro'] = str(e)   
        response['Retorno'] = 'Erro ao sincronizar usuario'
        erro_msg('Erro ao cadastar usuario',e)
        usuario.delet()            
        return Response(json.dumps(response), status=500, mimetype="application/json")


@app.route('/listarusuarios_turma_usuario', methods=['GET'])
def listarusuarios_turma_usuario():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    turma = current_user.turma
    usuarios = listar_usuarios_por_turma(turma=turma)
    return Response(json.dumps({'usuarios':usuarios}), status=200, mimetype="application/json")

@app.route('/listarusuarios', methods=['GET'])
def listarusuarios():
    usuarios = listar_usuarios()
    return Response(json.dumps({'usuarios':usuarios}), status=200, mimetype="application/json")

@app.route('/buscarusuarios_turma_usuario', methods=['GET'])
def buscarusuarios_turma_usuario():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    turma = current_user.turma
    usuarios = buscar_usuarios_por_turma(turma=turma)
    return Response(json.dumps({'usuarios':usuarios}), status=200, mimetype="application/json")

@app.route('/deletar_usuario', methods=['POST'])
def deletar_usuario():
    auth = authenticate('professor')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    try:
        response = {}
        body = request.get_json()
        email = body['email']

    except Exception as e:
        response['load'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    try:
        x = delete_usuario(email=email)
        if x.deleted_count:
            response = {
                'delet':True,
            }
        else:
            response = {
                'delet':False,
                'Retorno':'Usuario nao existe'
            }            
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response = {}
        response['delet'] = False
        response['Retorno'] = 'Usuario nao deletado'         
        response['erro'] = str(e)
        erro_msg('Elemento nao encontrado ao deletar trilha',e)
        return Response(json.dumps(response), status=400, mimetype="application/json")