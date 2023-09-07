from app.controllers.site import routes
from app.controllers.trilha import trilha
from app.controllers.user import cadastrar_carregar
from app.controllers.user import login

from app import app
from flask import Response
from flask_login import login_manager
import json
@app.errorhandler(401)
def unauthorized(error):
    response = {'login':False, 'mensagem':"Não autorizado"}
    return Response(json.dumps(response), status=401, mimetype="application/json")

@app.route('/listar_rotas', methods=['GET'])
def listar_rotas():
    rotas = []
    for rule in app.url_map.iter_rules():
        if not rule.endpoint.startswith('static'):
            rotas.append({
                'endpoint': rule.endpoint,
                'methods': ','.join(rule.methods),
                'path': rule.rule
            })
    return Response(json.dumps({'rotas':rotas}), status=401, mimetype="application/json")
