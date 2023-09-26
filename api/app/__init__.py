
from flask import Flask, Response
from flask_login import LoginManager
import pymongo, json, sys
from flask_cors import CORS
import sys

from app.controllers.mensagens import erro_msg, normal_msg

# Configura o Flask
app = Flask(__name__, template_folder='templates')
app.config.from_pyfile('config.py')
CORS(app)

# Configura o MongoDB
try:   
    mongoClient = pymongo.MongoClient(app.config['MONGO_URI'])
    mongoDB = mongoClient["ARduck"]
    normal_msg('Banco conectado', mongoDB)
    normal_msg('Conexoes:', mongoDB.list_collection_names())
   
except Exception as e:
    erro_msg("Ao conectar no Mongo DB", e)
    sys.exit(1)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

from app.controllers import redirect