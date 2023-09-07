from app import app
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models.userModel import Usuario
from app.models.trilhaModel import Trilha
import json

@app.route('/cadastrartrilha', methods=['GET', 'POST'])
@login_required
def cadastrartrilha():
    response = {}
    if request.method == 'POST':

        if current_user.privilegio is not "administrador" or "professor":
            response = {'create':False, 'mensagem':"Não autorizado"}
            return Response(json.dumps(response), status=401, mimetype="application/json")
        
        body = request.get_json()
        try:
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

            turma = current_user.turma
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

        except Exception as e:
            response['create'] = False
            response['Retorno'] = 'Parametros invalidos ou ausentes'         
            response['erro'] = str(e)
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
        try:
            trilha.save()
            usuarios=Usuario.listar_usuarios_por_turma(current_user.turma)
            for usuario in usuarios:
                if progressivo:
                    trilha.syncpermissoes(usuario=usuario, habilitado=False)
                else:
                    trilha.syncpermissoes(usuario=usuario, habilitado=True)

        except Exception as e:
            response['create'] = False
            response['Retorno'] = 'Erro ao cadastrar trilha'         
            response['erro'] = str(e)
            return Response(json.dumps(response), status=500, mimetype="application/json")

    return render_template('home/cadastrartrilha.html')

