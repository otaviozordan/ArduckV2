from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import re
from app.models.userModel import *
from app.models.trilhaModel import *
from app.controllers import authenticate
from app.controllers.mensagens import erro_msg, normal_msg
import json

@app.route('/cadastrartrilha', methods=['POST'])
def cadastrartrilha():
    auth = authenticate('professor')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")

    response = {}
    body = request.get_json()
    try:
        turma = current_user.turma
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
            
            trilha.syncprogresso(usuario=usuario)
        
        response['create']=True
        response['trilha']=trilha.to_json()
        return Response(json.dumps(response), status=200, mimetype="application/json") 
       
    except Exception as e:
        response = {}
        response['busca'] = False
        response['Retorno'] = 'Erro ao cadastrar trilha'         
        response['erro'] = str(e)
        erro_msg('Erro ao cadastrar trilha',e)
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
        erro_msg('Erro ao buscar trilha',e)
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
        erro_msg('Erro ao buscar trilha',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
    

@app.route('/listartrilha_por_colecao_permitida/<colecao>', methods=['GET'])
def listartrilha_por_colecao_permitida(colecao):
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
            quiz = trilha['options']['quiz']
        else:
            response = {
                'load':False,
                'Retorno':'Quiz não encontrado'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
        if len(quiz)-1 >= numero:
            quiz = trilha['options']['quiz'][numero]
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
        erro_msg('Erro ao verificar quiz',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
    

@app.route('/cadastrarprogresso', methods=['POST'])
def cadastrarprogresso():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")

    response = {}
    body = request.get_json()
    try:
        colecao = body['colecao']
        trilha = body['trilha']
        elemento = body['elemento']

    except Exception as e:
        response['create'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    try:
        trilha_obj = load_trilha_por_colecao_nome(current_user.turma, colecao=colecao, nome=trilha)
        trilha_obj.setprogresso(usuario=current_user.email, elemento=elemento)
        
        response['set']=True
        return Response(json.dumps(response), status=200, mimetype="application/json") 
       
    except Exception as e:
        response = {}
        response['set'] = False
        response['Retorno'] = 'Elemento nao encontrado'         
        response['erro'] = str(e)
        erro_msg('Erro ao regs=istrar progresso',e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

@app.route('/verificarmedidas', methods=['POST'])
def verificarmedidas():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    def converte_para_SI(valor, unidade):
        if unidade.lower() == 'mv':
            return valor / 1000  # Converte de mV para V
        elif unidade.lower() == 'v':
            return valor  # Já está em V
        elif unidade.lower() == 'ma':
            return valor / 1000  # Converte de mV para V        elif unidade.lower() == 'v':
        elif unidade.lower() == 'a':
            return valor  # Já está em V
        else:
            raise ValueError("Unidade de entrada inválida. Use 'mV' ou 'V' para tensao e 'mA' ou 'A' para corrente.")

    try:
        response = {}
        body = request.get_json()
        colecao = body['colecao']
        nome = body['trilha']
        medida = body['medidas']
        escala = body['escala']

    except Exception as e:
        response['load'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:        
        trilhas = load_trilhas_por_colecao(turma=current_user.turma, colecao=colecao)
        if nome in trilhas:
            validacao = trilhas[nome]['options']['validacao_pratica']
            print(validacao)
            if validacao['tipo'] == 'multimetro':
                esperado = validacao['valor_esperado']
                
                if verifica_gabarito(gabarito=esperado, escala=escala, valor=medida):
                    response = {
                    'validado':True,
                    'correto':True,

                    }
                    return Response(json.dumps(response), status=200, mimetype="application/json")
                else:
                    response = {
                    'validado':True,
                    'correto':False,
                    'Retorno':'Medida nao correspondente'
                    }
                    return Response(json.dumps(response), status=200, mimetype="application/json")                    

            else:
                response = {
                    'validado':False,
                    'Retorno':'Tipo de medida nao encontrada'
                }
                return Response(json.dumps(response), status=400, mimetype="application/json")
        
        else:
            response = {
                'load':False,
                'Retorno':'Trilha nao encontrada'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
    except Exception as e:
        response = {}
        response['load'] = False
        response['Retorno'] = 'Erro ao buscar trilha'         
        response['erro'] = str(e)
        erro_msg('Erro ao buscar trilha',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")