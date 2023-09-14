from app import app
from flask import request, Response
from flask_login import current_user, login_user
from werkzeug.utils import secure_filename
from app.controllers import authenticate
from app.models.userModel import buscar_email
from app.controllers.mensagens import erro_msg, normal_msg
import json
import os

@app.route('/upload_file/', methods=['POST'])
def upload_file():
    try:
        auth = authenticate('log')
        if auth:
            return Response(json.dumps(auth), status=401, mimetype="application/json")

        # Verifique se um arquivo foi enviado no formulário
        if 'file' not in request.files:
            response = {
                'upload': False,
                'Retorno': 'Arquivo não enviado',
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")

        file = request.files['file']

        # Verifique se o nome do arquivo é vazio
        if file.filename == '':
            response = {
                'upload': False,
                'Retorno': 'Nome do arquivo vazio',
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")

        # Verifique se o campo 'colecao' está presente no formulário
        if 'colecao' not in request.form:
            response = {
                'upload': False,
                'Retorno': 'colecao deve estar presente no form'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")

        # Verifique se o campo 'trilha' está presente no formulário
        if 'trilha' not in request.form:
            response = {
                'upload': False,
                'Retorno': 'trilha deve estar presente no form'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")

        colecao = json.loads(request.form['colecao'])
        trilha = json.loads(request.form['trilha'])
        turma = current_user.turma  # Substitua por como você obtém a turma do usuário
        user_email = current_user.email  # Substitua por como você obtém o email do usuário
        acao = json.loads(request.form['acao'])

        print("colecao:", colecao)
        print("trilha:", trilha)
        print("turma:", turma)
        print("user_email:", user_email)
        print("acao:", acao)

        return save_uploaded_file(file, acao, turma, colecao, trilha, user_email)

    except Exception as e:
        print("Erro:", str(e))
        response = {
            'upload': False,
            'Retorno': 'Erro',
            'erro': str(e)
        }
        erro_msg("Upload de imagem", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    except Exception as e:
        response = {
            'upload': False,
            'Retorno': 'Erro',
            'erro': str(e)
        }
        erro_msg("Upload de imagem", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")



@app.route('/render_test_upload_file', methods=['GET'])
def render_test_upload_file():
    user = buscar_email('otavio@outlook.com')
    login_user(user)  # Autenticar o usuário com o Flask-Login
    page = """

    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload de Arquivos</title>
    </head>
    <body>
        <h1>Envie um arquivo</h1>
        <form action="/upload_file/" method="post" enctype="multipart/form-data">
            <label for="file">Selecione um arquivo:</label>
            <input type="file" name="file" id="file" accept=".pdf, .jpg, .png, .gif"><!-- Defina as extensões de arquivo aceitáveis -->
            <br>
            <label for="acao">Selecione a ação:</label>
            <select name="acao" id="acao">
                <option value="icon">Icon</option>
                <option value="teoria">Teoria</option>
                <option value="validacao">Validação</option>
            </select>
            <br>
            <label for="colecao">Coleção:</label>
            <input type="text" name="colecao" id="colecao">
            <br>
            <label for="trilha">Trilha:</label>
            <input type="text" name="trilha" id="trilha">
            <br>
            <input type="submit" value="Enviar">
        </form>
    </body>
    </html>

    """
    return Response(page, status=200, mimetype="text/html")