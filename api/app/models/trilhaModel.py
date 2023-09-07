from app import mongoDB
from app.controllers.mensagens import erro_msg
from flask_login import LoginManager, UserMixin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from jsonschema import validate, ValidationError

#{
#   'turma': {
#        'nome da coleção':{
#            'nome trilha 1':{
#                'ordem':1,
#                'img_path':'/path',
#                'decricao':'Seja bem vindo ao ARduck, aqui você aprende de verdade. Essa trilha sumirá quando você criar outra.',
#                'opitions':{
#                    'quiz':[
#                        {
#                            'pergunta 1':'Quem é mais bonito',
#                            'resposta certa':'Otavio',
#                            'alternativas':{
#                                'opcao 1':'Athos',
#                                'opcao 2':'Kayque',
#                                'opcao 3':'Otavio'
#                            }
#                        },
#                        {
#                            'pergunta 2':'Quem é mais estranho',
#                            'resposta certa':'Athos',
#                            'alternativas':{
#                                'opcao 1':'Athos',
#                                'opcao 2':'Kayque',
#                                'opcao 3':'Otavio'
#                            }
#                        }
#                    ],
#                    'teoria':[
#                        'Loren ipson',
#                        '/path1',
#                        'Bla bla bla',
#                        '/path'
#                    ],
#                    'ar':True,
#                    'validacao_pratica':{
#                        'tipo':'multimetro',
#                        'valor_esperado':'1.23V'
#                    },
#                    'progressivo':True
#                }
#            }
#        }
#    }
#}

class Trilha():
    def __init__(self, turma, colecao, nome, ordem, img_path, descricao, quiz, teoria, ar, validacao_pratica, progressivo, autor):
        self.turma = turma
        self.colecao = colecao
        self.nome = nome
        self.ordem = ordem
        self.img_path = img_path
        self.descricao = descricao
        self.quiz = quiz
        self.teoria = teoria
        self.ar = ar
        self.validacao_pratica = validacao_pratica
        self.progressivo = progressivo
        self.autor = autor

        self.parametros = {
            'ordem':ordem,
            'img_path':img_path,
            'decricao': descricao,
            'opitions':{
                'quiz':quiz,
                'teoria':teoria,
                'ar':ar,
                'validacao_pratica':validacao_pratica,
                'progressivo':progressivo
            },
            'autor':autor
        }

    # Defina um esquema JSON para os parâmetros da trilha
    parametros_schema = {
        "type": "object",
        "properties": {
            "ordem": {"type": "integer"},
            "img_path": {"type": "string"},
            "descricao": {"type": "string"},
            "opitions": {
                "type": "object",
                "properties": {
                    "quiz": {"type": "array"},
                    "teoria": {"type": "array"},
                    "ar": {"type": "boolean"},
                    "validacao_pratica": {"type": "object"},
                    "progressivo": {"type": "boolean"},
                },
                "required": ["quiz", "teoria", "ar", "validacao_pratica", "progressivo"]
            },
            "autor": {"type": "string"}
        },
        "required": ["ordem", "img_path", "descricao", "opitions", "autor"]
    }


    def validar_parametros(cls, self):
        try:
            validate(self.parametros, cls.parametros_schema)
            return True
        except ValidationError as e:
            erro_msg("Erro na validação dos parâmetros", e)
            return False


    def to_json(self):
        # Converte um objeto de usuário em um dicionário JSON
        return {
            self.turma: {
                self.colecao:{
                    self.nome:self.parametros
                }
            }
        }

    @classmethod
    def save(self):
        try:
            # Verificar se a trilha já existe no banco de dados
            trilha_existente = mongoDB.Trilhas.find_one(
                {
                    self.turma: {
                        self.colecao: {
                            self.nome: {
                                "$exists": True
                            }
                        }
                    }
                }
            )

            if trilha_existente:
                # Se a trilha já existe, atualize-a
                mongoDB.Trilhas.update_one(
                    {
                        self.turma: {
                            self.colecao: {
                                self.nome: {
                                    "$exists": True
                                }
                            }
                        }
                    },
                    {
                        "$set": {
                            f"{self.turma}.{self.colecao}.{self.nome}": self.parametros
                        }
                    }
                )
            else:
                # Se a trilha não existe, insira-a
                mongoDB.Trilhas.insert_one(
                    {
                        self.turma: {
                            self.colecao: {
                                self.nome: self.parametros
                            }
                        }
                    }
                )

        except Exception as e:
         erro_msg("Erro ao cadastrar trilha", e)

    @classmethod
    def syncpermissoes(cls, self, usuario, habilitado=True):
        try:
            # Consulta o documento de permissões do usuário
            permissao_usuario = mongoDB.Permissoes.find_one({"usuario": usuario})

            if not permissao_usuario:
                # Se o documento de permissões não existir, crie-o com uma estrutura vazia para permissões
                permissao_usuario = {
                    "usuario": usuario,
                    "turma":self.turma,
                    "permissoes": {}
                }

            # Crie uma estrutura de permissões para a turma se não existir
            if self.turma not in permissao_usuario["permissoes"]:
                permissao_usuario["permissoes"][self.turma] = {}

            # Crie uma estrutura de permissões para a coleção se não existir
            if self.colecao not in permissao_usuario["permissoes"][self.turma]:
                permissao_usuario["permissoes"][self.turma][self.colecao] = {}

            # Atualize as permissões do usuário com as trilhas sincronizadas
            permissao_usuario["permissoes"][self.turma][self.colecao][self.nome] = habilitado

            # Atualize ou insira o documento de permissões no banco de dados
            mongoDB.Permissoes.update_one(
                {"usuario": usuario},
                {"$set": {"permissoes": permissao_usuario["permissoes"]}},
                upsert=True  # Insere um novo documento se não existir
            )

        except Exception as e:
            erro_msg("Erro ao sincronizar trilhas para o usuário", e)

def load_trilha_nome(turma, colecao, nome):
    try:
        # Busca a trilha no banco de dados
        trilha_data = mongoDB.Trilhas.find_one(
            {
                turma: {
                    colecao: {
                        nome: {
                            "$exists": True
                        }
                    }
                }
            }
        )
        if trilha_data:
            # Se a trilha existe no banco de dados, crie uma instância da classe Trilha
            trilha = Trilha(
                turma=turma,
                colecao=colecao,
                nome=nome,
                ordem=trilha_data[turma][colecao][nome]['ordem'],
                img_path=trilha_data[turma][colecao][nome]['img_path'],
                descricao=trilha_data[turma][colecao][nome]['descricao'],
                quiz=trilha_data[turma][colecao][nome]['opitions']['quiz'],
                teoria=trilha_data[turma][colecao][nome]['opitions']['teoria'],
                ar=trilha_data[turma][colecao][nome]['opitions']['ar'],
                validacao_pratica=trilha_data[turma][colecao][nome]['opitions']['validacao_pratica'],
                progressivo=trilha_data[turma][colecao][nome]['opitions']['progressivo'],
                autor=trilha_data[turma][colecao][nome]['autor']
            )
            return trilha
        else:
            return None
    except Exception as e:
        erro_msg("Erro ao carregar trilha", e)
        return None
        

def buscar_trilhas_por_colecao(turma, colecao):
    try:
        # Consulta o banco de dados para obter os nomes de trilhas da turma e coleção específicas
        trilhas = mongoDB.Trilhas.find(
            {
                turma: {
                    colecao: {
                        "$exists": True
                    }
                }
            }
        )
        # Extrai os nomes das trilhas encontradas
        nomes_de_trilhas = []
        for trilha in trilhas:
            nomes_de_trilhas.extend(trilha[turma][colecao].keys())
        return nomes_de_trilhas
    except Exception as e:
        erro_msg("Erro ao buscar nomes de trilhas", e)
    return []

def listar_nomes_colecoes_por_turma(turma):
    try:
        # Consulta o banco de dados para obter as trilhas da turma específica
        trilhas_por_turma = mongoDB.Trilhas.find(
            {
                turma: {
                    "$exists": True
                }
            }
        )
        # Lista para armazenar os nomes das coleções
        nomes_colecoes = []
        for trilhas_turma in trilhas_por_turma:
            for colecao in trilhas_turma[turma].keys():
                nomes_colecoes.append(colecao)
        return nomes_colecoes
    except Exception as e:
        erro_msg("Erro ao listar nomes das coleções por turma", e)
        return []