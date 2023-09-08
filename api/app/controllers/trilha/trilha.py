from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models.userModel import Usuario, listar_usuarios_por_turma
from app.models.trilhaModel import *
from app.controllers import authenticate
import json

@app.route('/cadastrartrilha', methods=['GET', 'POST'])
def cadastrartrilha():
    auth = authenticate('professor')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")

    response = {}
    body = request.get_json()
    try:
        turma = body['turma']
        colecao = body['colecao']
        trilha = body['trilha']
        ordem = body['ordem']
        img_path = body['img_path']
        descricao = body['descricao']
        teoria = body['teoria']
        quiz = body['quiz']
        validacao_pratica = body['validacao_pratica']
        ar = body['ar']
        progressivo = body['progressivo']

        if turma != current_user.turma:
            return Response(json.dumps({'create':False, 'Retorno':'incoerencia de turmas'}), status=401, mimetype="application/json")
        autor = current_user.email

        trilha = Trilha(
            turma=turma,
            colecao=colecao,
            nome=trilha,
            ordem=ordem,
            img_path=img_path,
            descricao=descricao,
            teoria=teoria,
            quiz=quiz,
            validacao_pratica=validacao_pratica,
            ar=ar,
            progressivo=progressivo,
            autor=autor
        )

        if not trilha.validar_parametros:
            response['Retorno'] = 'Parametros invalidos para uma trilha'         
            response['erro'] = str(e)
            return Response(json.dumps(response), status=400, mimetype="application/json")


    except Exception as e:
        response['create'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    try:
        trilha.save()
        usuarios=listar_usuarios_por_turma(current_user.turma)
        for usuario in usuarios:
            if progressivo:
                trilha.syncpermissoes(usuario=usuario, habilitado=False)
            else:
                trilha.syncpermissoes(usuario=usuario, habilitado=True)
        
        response['create']=True
        response['trilha']=trilha.to_json()
        return Response(json.dumps(response), status=200, mimetype="application/json") 
       
    except Exception as e:
        response = {}
        response['busca'] = False
        response['Retorno'] = 'Erro ao cadastrar trilha'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=500, mimetype="application/json")

@app.route('/listar_colecoes', methods=['GET'])
def listar_colecoes():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    colecoes = listar_nomes_colecoes_por_turma(turma=current_user.turma)
    return Response(json.dumps({'busca':True, 'colecoes':colecoes}), status=200, mimetype="application/json")    


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
        return Response(json.dumps(response), status=500, mimetype="application/json")

@app.route('/listartrilha_por_colecao/<colecao>', methods=['GET'])
def buscartrilha_por_colecao(colecao):
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    try:
        response = {}
        body = request.get_json()
        colecao = body['colecao']

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
            quiz = trilha['opitions']['quiz']
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
        return Response(json.dumps(response), status=500, mimetype="application/json")
    
@app.route('/verifiacarquiz', methods=['POST'])
def verifiacarquiz():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    try:
        response = {}
        body = request.get_json()
        colecao = body['colecao']
        nome = body['trilha']
        numero = body['numero']
        resposta = body['resposta']

    except Exception as e:
        response['load'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:        
        trilhas = load_trilhas_por_colecao(turma=current_user.turma, colecao=colecao)
        if nome in trilhas:
            trilha = trilhas[nome]
            quiz = trilha['opitions']['quiz']
        else:
            response = {
                'load':False,
                'Retorno':'Quiz não encontrado'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
        if len(quiz)-1 >= numero:
            quiz = trilha['opitions']['quiz'][numero]
            if quiz['resposta certa'] == resposta:
                acerto = True
            else:
                acerto = False
            return Response(json.dumps({'load':True, 'quiz':quiz, 'acerto':acerto}), status=200, mimetype="application/json")
        
        else:
            response = {
                'load':False,
                'Retorno':'Numero de quiz não existe'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
    except Exception as e:
        response = {}
        response['load'] = False
        response['Retorno'] = 'Erro ao buscar quiz'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
    
    