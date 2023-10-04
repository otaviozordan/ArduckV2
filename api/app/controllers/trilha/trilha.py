from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import re
from app.models.userModel import *
from app.models.trilhaModel import *
from app.models.gerarRelatorio import *
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
        img = body['img']
        img_path = body['img_path'] 

        #img_path = f'/static/imgs/{turma}/{colecao}/{trilha}/icon.jpcdcg'

        descricao = body['descricao']
        temp_teoria = body['teoria']
        teoria = []
        for item in temp_teoria:
            if item.startswith('$'):
                novo_item = f'/static/imgs/{turma}/{colecao}/{trilha}/{item[1:]}.jpg'
            else:
                novo_item = item
            teoria.append(novo_item)

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
            img_colection=img,
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

        if not trilha_obj:
            response = {}
            response['set'] = False
            response['Retorno'] = 'Essa trilha nao existe'
            return Response(json.dumps(response), status=400, mimetype="application/json") 
        
        x = trilha_obj.setprogresso(usuario_email=current_user.email, elemento=elemento)
        if not x:
            response['set']=True
            return Response(json.dumps(response), status=200, mimetype="application/json")
        
        response = {'set':False, 'Erro':x}
        return Response(json.dumps(response), status=500, mimetype="application/json")
       
    except Exception as e:
        response = {}
        response['set'] = False
        response['Retorno'] = 'Erro ao cadastrar progresso'         
        response['erro'] = str(e)
        erro_msg('Erro ao cadastrar progresso',e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

@app.route('/verificarmedidas', methods=['POST'])
def verificarmedidas():
    auth = authenticate('log')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    def converte_para_SI(valor, unidade):
        if unidade.lower() == 'mv':
            return valor / 1000, "v"  # Converte de mV para V
        elif unidade.lower() == 'v':
            return valor, 'v'
        elif unidade.lower() == 'ma':
            return valor / 1000, 'a'  # Converte de mA para A
        elif unidade.lower() == 'a':
            return valor, "a"
        else:
            raise ValueError("Unidade de entrada inválida. Use 'mV' ou 'V' para tensao e 'mA' ou 'A' para corrente.")

    def separar_valor_escala(texto):
        # Use uma expressão regular para separar o valor e a escala
        padrao = r'([\d.]+)([A-Za-z]+)'
        correspondencia = re.match(padrao, texto)

        if correspondencia:
            valor = float(correspondencia.group(1))
            escala = correspondencia.group(2)
            return valor, escala
        else:
            raise ValueError("Formato de entrada inválido.")

    try:
        response = {}
        body = request.get_json()
        colecao = body['colecao']
        nome = body['trilha']
        medida_body = body['medidas']
        escala_body = body['escala']

    except Exception as e:
        response['load'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

    try:        
        trilhas = load_trilhas_por_colecao(turma=current_user.turma, colecao=colecao)
        if nome in trilhas:
            validacao = trilhas[nome]['options']['validacao_pratica']
            if validacao['tipo'] == 'multimetro':
                esperado = validacao['valor_esperado']
                valor_gab, escala_gab = separar_valor_escala(esperado)
                valor_gab, escala_gab = converte_para_SI(valor=valor_gab, unidade=escala_gab)
                medida_body, escala_body = converte_para_SI(valor=int(medida_body), unidade=escala_body) 

                if medida_body >= (valor_gab-10*valor_gab/100) and medida_body <= (valor_gab+10*valor_gab/100):
                    response = {
                    'validado':True,
                    'correto':True,
                    'valor_lido':str(medida_body)+escala_body,
                    'valor_correto':str(valor_gab)+escala_gab
                    }
                    return Response(json.dumps(response), status=200, mimetype="application/json")
                else:
                    response = {
                    'validado':True,
                    'correto':False,
                    'Retorno':'Medida nao correspondente',
                    'valor_lido':str(medida_body)+escala_body,
                    'valor_correto':str(valor_gab)+escala_gab
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

@app.route('/deletar_trilha', methods=['POST'])
def deletar_trilha():
    auth = authenticate('professor')
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
        delete_trilha(turma=current_user.turma, colecao=colecao, nome_trilha=nome)
        
        response = {
            'delet':True,
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        response = {}
        response['delet'] = False
        response['Retorno'] = 'Elemento nao encontrado ao deletar trilha'         
        response['erro'] = str(e)
        erro_msg('Elemento nao encontrado ao deletar trilha',e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
@app.route('/gerar_relatorio', methods=['POST'])
def gerar_relatorio():
    auth = authenticate('professor')
    if auth:
        return Response(json.dumps(auth), status=401, mimetype="application/json")
    
    # Dados de exemplo em formato JSON
    response = {}
    body = request.get_json()
    try:
        email_aluno = body['email_aluno']
        if 'send' in body and body['send'] == True:
            e_para_enviar = True
        else:
            e_para_enviar = False

    except Exception as e:
        response['create'] = False
        response['Retorno'] = 'Parametros invalidos ou ausentes'         
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    try:
        aluno = buscar_email(email_aluno)
        progresso = buscar_progresso_do_usuario(email=email_aluno)
        if not aluno or not progresso:
            return Response(json.dumps({'send':False, 'Retorno':'Usuario nao existe'}), status=400, mimetype="application/json")

        relatorio = RelatorioDeProgresso(aluno=aluno.nome, turma=aluno.turma, email=email_aluno)
        relatorio.gerar_relatorio(data=progresso)
        path = f'/static/reports/{email_aluno}.pdf'

    except Exception as e:
        response = {}
        response['send'] = False
        response['Retorno'] = 'Erro ao gerar relatorio'         
        response['erro'] = str(e)
        erro_msg('Erro ao gerar relatorio',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
    
    try:
        if 'email_professor' in body and e_para_enviar:
            email_professor = body['email_professor']
            relatorio.enviar_email_com_anexo(destinatario_email=email_professor)
            response = {
                'gen':True,
                'send':True,
                'email':email_professor,
                'path':path
            }
        elif e_para_enviar:
            relatorio.enviar_email_com_anexo(destinatario_email=current_user.email)
            response = {                
                'gen':True,
                'send':True,
                'email':current_user.email,
                'path':path

            }
        else:
            response = {                
                'gen':True,
                'send':False,
                'email':current_user.email,
                'path':path

            }
        return Response(json.dumps(response), status=200, mimetype="application/json")

    except Exception as e:
        response = {}
        response['send'] = False
        response['Retorno'] = 'Erro ao enviar email'         
        response['erro'] = str(e)
        erro_msg('Erro ao enviar email',e)
        return Response(json.dumps(response), status=500, mimetype="application/json")
       
