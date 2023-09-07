
from flask import Flask, Response
from flask_login import LoginManager
import pymongo, json, sys
import sys

from app.controllers.mensagens import erro_msg

# Configura o Flask
app = Flask(__name__, template_folder='templates')
app.config.from_pyfile('config.py')

# Configura o MongoDB
try:   
    mongoClient = pymongo.MongoClient(app.config['MONGO_URI'])
    mongoDB = mongoClient["ARduck"]
   
except Exception as e:
    print(erro_msg("Ao conectar no Mongo DB", e))
    sys.exit(1)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.controllers import routes