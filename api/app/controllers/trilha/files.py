from app import app
from flask import request, Response
from flask_login import current_user, login_user
from werkzeug.utils import secure_filename
from app.controllers import authenticate
from app.models.userModel import buscar_email
from app.controllers.mensagens import erro_msg, normal_msg
from app.config import UPLOAD_FOLDER
import json
import os

@app.route('/upload_file/icon', methods=['POST'])
def upload_file_icon():
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

        # Diretório base onde os arquivos serão salvos
        base_dir = UPLOAD_FOLDER
        
        # Crie o diretório para a turma do usuário, se não existir
        turma_dir = os.path.join(base_dir, turma)
        if not os.path.exists(turma_dir):
            os.makedirs(turma_dir)
        
        # Crie o diretório para a coleção do usuário, se não existir
        colecao_dir = os.path.join(turma_dir, colecao)
        if not os.path.exists(colecao_dir):
            os.makedirs(colecao_dir)
        
        # Crie o diretório para a trilha do usuário, se não existir
        trilha_dir = os.path.join(colecao_dir, trilha)
        if not os.path.exists(trilha_dir):
            os.makedirs(trilha_dir)
        
        filename = 'icon' + os.path.splitext(file.filename)[-1]

        # Caminho completo para salvar o arquivo
        file_path = os.path.join(trilha_dir, filename)

        # Salve o arquivo
        file.save(file_path)

        new_filename = filename  # Você precisa definir como deseja obter o novo nome

        response = {
            'upload': True,
            'message': f'Arquivo "{file.filename}" renomeado para "{new_filename}" e salvo com sucesso!',
            'new_filename': new_filename
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")


    except Exception as e:
        print("Erro:", str(e))
        response = {
            'upload': False,
            'Retorno': 'Erro',
            'erro': str(e)
        }
        erro_msg("Upload de imagem", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
    

@app.route('/upload_file/teoria', methods=['POST'])
def upload_file_teoria():
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

        # Diretório base onde os arquivos serão salvos
        base_dir = UPLOAD_FOLDER
        
        # Crie o diretório para a turma do usuário, se não existir
        turma_dir = os.path.join(base_dir, turma)
        if not os.path.exists(turma_dir):
            os.makedirs(turma_dir)
        
        # Crie o diretório para a coleção do usuário, se não existir
        colecao_dir = os.path.join(turma_dir, colecao)
        if not os.path.exists(colecao_dir):
            os.makedirs(colecao_dir)
        
        # Crie o diretório para a trilha do usuário, se não existir
        trilha_dir = os.path.join(colecao_dir, trilha)
        if not os.path.exists(trilha_dir):
            os.makedirs(trilha_dir)
        
        # Conte o número de arquivos de teoria na pasta trilha
        existing_theories = len([f for f in os.listdir(trilha_dir) if f.startswith('teoria')])
        filename = f'teoria{existing_theories + 1}' + os.path.splitext(file.filename)[-1]

        # Caminho completo para salvar o arquivo
        file_path = os.path.join(trilha_dir, filename)

        # Salve o arquivo
        file.save(file_path)

        new_filename = filename  # Você precisa definir como deseja obter o novo nome

        response = {
            'upload': True,
            'message': f'Arquivo "{file.filename}" renomeado para "{new_filename}" e salvo com sucesso!',
            'new_filename': new_filename
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")


    except Exception as e:
        print("Erro:", str(e))
        response = {
            'upload': False,
            'Retorno': 'Erro',
            'erro': str(e)
        }
        erro_msg("Upload de imagem", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")

@app.route('/upload_file/validacao', methods=['POST'])
def upload_file_validacao():
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

        # Diretório base onde os arquivos serão salvos
        base_dir = UPLOAD_FOLDER
        
        # Crie o diretório para a turma do usuário, se não existir
        turma_dir = os.path.join(base_dir, turma)
        if not os.path.exists(turma_dir):
            os.makedirs(turma_dir)
        
        # Crie o diretório para a coleção do usuário, se não existir
        colecao_dir = os.path.join(turma_dir, colecao)
        if not os.path.exists(colecao_dir):
            os.makedirs(colecao_dir)
        
        # Crie o diretório para a trilha do usuário, se não existir
        trilha_dir = os.path.join(colecao_dir, trilha)
        if not os.path.exists(trilha_dir):
            os.makedirs(trilha_dir)
        
        filename = 'validacao' + os.path.splitext(file.filename)[-1]

        # Caminho completo para salvar o arquivo
        file_path = os.path.join(trilha_dir, filename)

        # Salve o arquivo
        file.save(file_path)

        new_filename = filename  # Você precisa definir como deseja obter o novo nome

        response = {
            'upload': True,
            'message': f'Arquivo "{file.filename}" renomeado para "{new_filename}" e salvo com sucesso!',
            'new_filename': new_filename
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")


    except Exception as e:
        print("Erro:", str(e))
        response = {
            'upload': False,
            'Retorno': 'Erro',
            'erro': str(e)
        }
        erro_msg("Upload de imagem", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")


@app.route('/render_test_upload_file/icon', methods=['GET'])
def render_test_upload_file_icon():
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
        <form action="/upload_file/icon" method="post" enctype="multipart/form-data">
            <label for="file">Selecione um arquivo:</label>
            <input type="file" name="file" id="file" accept=".pdf, .jpg, .png, .gif"><!-- Defina as extensões de arquivo aceitáveis -->
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

@app.route('/render_test_upload_file/teoria', methods=['GET'])
def render_test_upload_file_teoria():
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
        <form action="/upload_file/teoria" method="post" enctype="multipart/form-data">
            <label for="file">Selecione um arquivo:</label>
            <input type="file" name="file" id="file" accept=".pdf, .jpg, .png, .gif"><!-- Defina as extensões de arquivo aceitáveis -->
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

@app.route('/render_test_upload_file/validacao', methods=['GET'])
def render_test_upload_file_validacao():
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
        <form action="/upload_file/validacao" method="post" enctype="multipart/form-data">
            <label for="file">Selecione um arquivo:</label>
            <input type="file" name="file" id="file" accept=".pdf, .jpg, .png, .gif"><!-- Defina as extensões de arquivo aceitáveis -->
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