from app import app
from flask import request, Response
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.controllers import authenticate
from app.controllers.mensagens import erro_msg, normal_msg
import json
import os

@app.route('/upload_file/<acao>', methods=['POST'])
def upload_file(acao):
    try:
        auth = authenticate('professor')
        if auth:
            return Response(json.dumps(auth), status=401, mimetype="application/json")
        # Verifica se um arquivo foi enviado no formulário
        if 'file' not in request.files:
            response = {
                'upload': False,
                'Retorno': 'Arquivo não enviado',
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")

        file = request.files['file']

        # Verifica se o nome do arquivo é vazio
        if file.filename == '':
            response = {
                'upload': False,
                'Retorno': 'Nome do arquivo vazio',
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")
        
        # Verifica se o campo 'metadata' está presente no formulário
        if 'metadata' not in request.form:
            response = {
                'upload': False,
                'Retorno': 'Metadata deve estar presente no form'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")            
        
        # Analisa o JSON enviado no formulário
        form_data = json.loads(request.form['metadata'])

        # Verifica se as chaves 'colecao' e 'trilha' estão presentes no JSON
        if 'colecao' not in form_data or 'trilha' not in form_data:
            response = {
                'upload': False,
                'Retorno': 'JSON incompleto! Deve conter as chaves "colecao" e "trilha".'
            }
            return Response(json.dumps(response), status=400, mimetype="application/json")

        # Constrói o novo nome do arquivo com base nas chaves do JSON
        
        if acao is 'icon':
            new_filename = f"{current_user.turma}{form_data['colecao']}/{form_data['trilha']}/icon.{os.path.splitext(file.filename)[1]}"
        elif acao is 'teoria': #codigo para salvar o numero de arquivos na pasta colecao/trilha/teoria +1
            # Determine the current count of files in the directory
            directory = os.path.join(app.config['UPLOAD_FOLDER'], current_user.turma, form_data['colecao'], form_data['trilha'], 'teoria')
            current_file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

            # Increment the count
            new_file_count = current_file_count + 1

            # Create the new filename with the incremented count
            new_filename = f"{current_user.turma}/{form_data['colecao']}/{form_data['trilha']}/teoria/{new_file_count}.{os.path.splitext(file.filename)[1]}"

        new_filename = secure_filename(new_filename)

        # Salva o arquivo na pasta de upload
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        response = {
            'upload': True,
            'message': f'Arquivo "{file.filename}" renomeado para "{new_filename}" e salvo com sucesso!',
            'new_filename': new_filename
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")

    except Exception as e:
        response = {
            'upload': False,
            'Retorno': 'Erro',
            'erro': str(e)
        }
        erro_msg("Upload de imagem", e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
