from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import re
from app.models.userModel import *
from app.models.trilhaModel import *
from app.controllers import authenticate
from app.controllers.mensagens import erro_msg, normal_msg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

@app.route('/carregar_progresso_turma', methods=['GET'])
def carregar_progresso_turma():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")

    try:
        response = {}
        lista_permissoes = {}
        usuarios = buscar_usuarios_por_turma(current_user.turma)
        
        for usuario in usuarios:
            progresso_user = buscar_progresso_do_usuario(usuario['email'])
            lista_permissoes[usuario['email']] = progresso_user

        response = {
            'load':True,
            'progressos':lista_permissoes
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")
        
    except Exception as e:
        response = {}
        response['load'] = False
        response['Retorno'] = 'Erro ao buscar progressos'         
        response['erro'] = str(e)
        erro_msg('Erro ao buscar progressos',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
    
@app.route('/buscartrilha', methods=['POST'])
def buscartrilha():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    try:
        response = {}
        body = request.get_json()
        colecao = body['colecao']
        nome = body['trilha']

    except Exception as e:
        response['load'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:        
        trilhas = load_trilhas_por_colecao(turma=current_user.turma, colecao=colecao)
        if nome in trilhas:
            trilha = trilhas[nome]
            return Response(json.dumps({'load':True, 'trilha':trilha}), status=200, mimetype="application/json")
        else:
            response = {
                'load':False,
                'Retorno':'Trilhas não encontrada'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
    except Exception as e:
        response = {}
        response['load'] = False
        response['Retorno'] = 'Erro ao buscar trilha'         
        response['erro'] = str(e)
        erro_msg('Erro ao buscar trilha',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")

@app.route('/listartrilha_por_colecao/<colecao>', methods=['GET'])
def buscartrilha_por_colecao(colecao):
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    try:
        response = {}

    except Exception as e:
        response['load'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:        
        trilhas = load_trilhas_por_colecao(turma=current_user.turma, colecao=colecao)
        if len(trilhas) > 0:
            return Response(json.dumps({'load':True, 'trilhas':trilhas}), status=200, mimetype="application/json")
        else:
            response = {
                'load':False,
                'Retorno':'Trilhas não encontrada'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json") 
       
    except Exception as e:
        response = {}
        response['load'] = False
        response['Retorno'] = 'Erro ao buscar trilha'         
        response['erro'] = str(e)
        erro_msg('Erro ao buscar trilha',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
    
@app.route('/listartrilha_por_colecao_permitida/<colecao>', methods=['GET'])
def listartrilha_por_colecao_permitida(colecao):
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")

    try:
        trilhas_com_permissao = []
        usuarios = load_permissoes_por_colecao(turma=current_user.turma, colecao=colecao)
        for usuario in usuarios:
            email = usuario['usuario']
            permissoes = usuario['permissoes'][current_user.turma][colecao]
            print(permissoes)
            
            trilha = {
                'usuario': email,
                'permissao': permissoes
            }
            if trilha['usuario'] == current_user.email:
                trilhas_com_permissao.append(trilha)

        if len(trilhas_com_permissao) > 0:
            return Response(json.dumps({'load': True, 'trilhas': trilhas_com_permissao}), status=200, mimetype="application/json")
        else:
            response = {
                'load': False,
                'Retorno': 'Trilhas não encontradas'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json") 
       
    except Exception as e:
        response = {}
        response['load'] = False
        response['Retorno'] = 'Erro ao buscar trilha'         
        response['erro'] = str(e)
        erro_msg('Erro ao buscar trilha',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")

@app.route('/carregarquiz', methods=['POST'])
def carregarquiz():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    try:
        response = {}
        body = request.get_json()
        colecao = body['colecao']
        nome = body['trilha']

    except Exception as e:
        response['load'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:        
        trilhas = load_trilhas_por_colecao(turma=current_user.turma, colecao=colecao)
        if nome in trilhas:
            trilha = trilhas[nome]
            quiz = trilha['options']['quiz']
            return Response(json.dumps({'load':True, 'quiz':quiz}), status=200, mimetype="application/json")
        else:
            response = {
                'load':False,
                'Retorno':'Quiz não encontrado'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
    except Exception as e:
        response = {}
        response['load'] = False
        response['Retorno'] = 'Erro ao buscar quiz'         
        response['erro'] = str(e)
        erro_msg('Erro ao buscar quiz',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
    
@app.route('/listar_colecoes', methods=['GET'])
def listar_colecoes():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    colecoes = buscar_nomes_colecoes_por_turma_com_imagem(turma=current_user.turma)
    return Response(json.dumps({'busca':True, 'colecoes':colecoes}), status=200, mimetype="application/json")    