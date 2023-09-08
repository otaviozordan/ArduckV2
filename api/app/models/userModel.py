from app import mongoDB, erro_msg, login_manager
from flask_login import LoginManager, UserMixin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    # Consulte um documento de usuário no MongoDB com base no email (que é o user_id)
    usuario_data = mongoDB.Usuarios.find_one({"email": user_id})

    if usuario_data:
        # Se um usuário com o email especificado for encontrado, crie uma instância de Usuario
        return Usuario(user_data=usuario_data)
    else:
        return None

class Usuario(UserMixin):
    def __init__(self, user_data):
        self.nome = user_data["nome"]
        self.email = user_data["email"]
        self.turma = user_data["turma"]
        self.privilegio = user_data["privilegio"]
        self.password = user_data["password"]  # Não faça hash da senha aqui

    def save(self):
        # Gere o hash da senha antes de salvar o usuário
        self.password = generate_password_hash(self.password)
        # Salve o usuário no MongoDB
        mongoDB.Usuarios.insert_one(self.to_json())

    def delet(self):
        try:
            # Verifique se o usuário com o email especificado existe
            usuario = buscar_email(self.email)

            if usuario:
                # Se o usuário existe, exclua o documento correspondente no MongoDB
                mongoDB.Usuarios.delete_one({"email": self.email})
                return True
            else:
                # Se o usuário não existe, retorne False indicando que não foi possível excluir
                return False

        except Exception as e:
            erro_msg(f"Erro ao excluir usuário com email {self.email}", e)
            return False
        
    def to_json(self):
        # Converte um objeto de usuário em um dicionário JSON
        return {
            "nome": self.nome,
            "email": self.email,
            "turma": self.turma,
            "privilegio": self.privilegio,
            "password": self.password  # Agora, a senha está com hash
        }

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
    
    def get_id(self):
        # Retorna o email como identificador único
        return self.email
    
def listar_usuarios():
        try:
            # Consulte todos os documentos de usuários no MongoDB
            usuarios = mongoDB.Usuarios.find()

            # Inicialize uma lista para armazenar os emails dos usuários
            lista_emails_usuarios = []

            # Para cada documento de usuário encontrado, adicione o email à lista
            for usuario_data in usuarios:
                email = usuario_data["email"]
                lista_emails_usuarios.append(email)

            return lista_emails_usuarios

        except Exception as e:
            erro_msg("Erro ao listar emails de usuários", e)
            return []
        
def listar_usuarios_por_turma(turma):
        try:
            # Consulte todos os documentos de usuários no MongoDB que pertencem à turma especificada
            usuarios = mongoDB.Usuarios.find({"turma": turma})

            # Inicialize uma lista para armazenar os emails dos usuários
            lista_emails_usuarios = []

            # Para cada documento de usuário encontrado, adicione o email à lista
            for usuario_data in usuarios:
                email = usuario_data["email"]
                lista_emails_usuarios.append(email)

            return lista_emails_usuarios

        except Exception as e:
            erro_msg(f"Erro ao listar emails de usuários da turma {turma}", e)
            return []        

def buscar_email(email):
        try:
            # Consulte um documento de usuário no MongoDB com base no email
            usuario_data = mongoDB.Usuarios.find_one({"email": email})

            if usuario_data:
                # Se um usuário com o email especificado for encontrado, crie uma instância de Usuario
                return Usuario(user_data=usuario_data)
            else:
                return None

        except Exception as e:
            erro_msg(f"Erro ao encontrar usuário com email {email}", e)
            return None

def buscar_usuarios_por_turma(turma):
        try:
            # Realize a consulta com base na turma fornecida
            usuarios_na_turma = mongoDB.Usuarios.find({"turma": turma})
    
            # Crie uma lista para armazenar os documentos de usuários sem o campo "_id"
            lista_usuarios = []

            # Itere sobre os documentos e remova o campo "_id"
            for usuario in usuarios_na_turma:
                usuario.pop("_id", None)  # Remove o campo "_id" se estiver presente
                lista_usuarios.append(usuario)

            return lista_usuarios

        except Exception as e:
            erro_msg(f"Erro ao listar emails de usuários da turma {turma}", e)
            return []   

def email_existe(email):
    usuario = buscar_email(email)
    return usuario is not None