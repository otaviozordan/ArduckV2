from app import mongoDB
from app.controllers.mensagens import erro_msg
from flask_login import LoginManager, UserMixin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from jsonschema import validate, ValidationError

#Estrutura do MongoDB
#{
#   'turma': {
#        'nome da coleção':{
#            'nome trilha 1':{
#                'ordem':1,
#                'img_path':'/path',
#                'decricao':'Seja bem vindo ao ARduck, aqui você aprende de verdade. Essa trilha sumirá quando você criar outra.',
#                'options':{
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
    def __init__(self, turma, colecao, nome, ordem, img_path, img_colection, descricao, quiz, teoria, ar, validacao_pratica, progressivo, autor):
        self.turma = turma
        self.colecao = colecao
        self.nome = nome
        self.ordem = ordem
        self.img_path = img_path
        self.img_colection = img_colection
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
            'img_colection':img_colection,
            'descricao': descricao,
            'options':{
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
            "img_colection": {"type": "string"},
            "descricao": {"type": "string"},
            "options": {
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
        "required": ["ordem", "img_path", "descricao", "options", "autor"]
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

    def save(self):
        try:
            # Crie o filtro para verificar se a trilha já existe
            filtro = {
                self.turma + '.' + self.colecao + '.' + self.nome: {
                    "$exists": True
                }
            }

            # Crie o documento que você deseja inserir ou atualizar
            novo_documento = {
                self.turma + '.' + self.colecao + '.' + self.nome: self.parametros
            }

            # Use update_one com upsert=True para inserir ou atualizar o documento
            result = mongoDB.Trilhas.update_one(
                filtro,
                {
                    "$set": novo_documento
                },
                upsert=True
            )

            if result.upserted_id is None:
                # Se não houve inserção, o documento já existia e foi atualizado
                print(f"Trilha '{self.nome}' atualizada com sucesso.")
            else:
                # Se houve inserção, um novo documento foi criado
                print(f"Trilha '{self.nome}' criada com sucesso.")

        except Exception as e:
            erro_msg("Erro ao cadastrar/trilha", e)

    def syncpermissoes(self, usuario, habilitado=True):
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

    def syncprogresso(self, usuario):
        try:
            # Consulta o documento de progresso do usuário
            progresso_usuario = mongoDB.Progresso.find_one({"usuario": usuario})

            if not progresso_usuario:
                # Se o documento de progresso não existir, crie-o com uma estrutura vazia
                progresso_usuario = {
                    "usuario": usuario,
                    "turma": self.turma,
                    "progresso": {
                        'colecoes': [
                            {
                                'nome': self.colecao,
                                'trilhas': []
                            }
                        ]
                    }
                }
            else:
                # Verifique se a coleção existe, se não, crie-a
                colecoes = progresso_usuario.get("progresso", {}).get("colecoes", [])
                colecao_existente = False
                for colecao in colecoes:
                    if colecao["nome"] == self.colecao:
                        colecao_existente = True
                        break
                    
                if not colecao_existente:
                    progresso_usuario["progresso"]["colecoes"].append({
                        'nome': self.colecao,
                        'trilhas': []
                    })

            # Dados de exemplo em formato JSON para uma nova trilha
            nova_trilha = {
                "nome": self.nome,
                "quiz": [],
                "teoria": '',
                "atividade_pratica": ''
            }

            # Adicione a nova trilha à coleção existente (ou crie a coleção se não existir)
            for colecao in progresso_usuario["progresso"]["colecoes"]:
                if colecao["nome"] == self.colecao:
                    colecao["trilhas"].append(nova_trilha)
                    break
                
            # Atualize ou insira o documento de progresso no banco de dados
            mongoDB.Progresso.update_one(
                {"usuario": usuario},
                {"$set": {"progresso": progresso_usuario["progresso"]}},
                upsert=True  # Insere um novo documento se não existir
        )

        except Exception as e:
            erro_msg("Erro ao sincronizar progresso para o usuário", e)

    def setprogresso(self, usuario_email, elemento):
        try:
            # Variáveis fornecidas
            email = usuario_email
            nome_da_colecao = self.colecao
            nome_da_trilha = self.nome

            elemento_split = elemento.split('/')
            atualizacao = {}

            if len(elemento_split) == 3 and elemento_split[0] == 'quiz':
                numero_do_quiz = int(elemento_split[1])
                if elemento_split[2] == 'true':
                    novo_progresso_quiz = "Concluído"
                else:
                    novo_progresso_quiz = "Errado"
                atualizacao = {
                    '$set': {
                        f'progresso.colecoes.$[colecao].trilhas.$[trilha].quiz.{numero_do_quiz}': novo_progresso_quiz,
                    },
                }

            elif len(elemento_split) == 2 and elemento_split[0] == 'teoria':
                if elemento_split[1] == 'true':
                    novo_progresso_teoria = "Concluído"
                else:
                    novo_progresso_teoria = "Inconcluído"
                atualizacao = {
                    '$set': {
                        f'progresso.colecoes.$[colecao].trilhas.$[trilha].teoria': novo_progresso_teoria,
                    }
                }

            elif len(elemento_split) == 2 and elemento_split[0] == 'validacao_pratica':
                numero_do_quiz = elemento_split[1]
                if elemento_split[1] == 'true':
                    novo_progresso_pratica = "Concluído"
                else:
                    novo_progresso_pratica = "Inconcluído"
                atualizacao = {
                    '$set': {
                        f'progresso.colecoes.$[colecao].trilhas.$[trilha].atividade_pratica': novo_progresso_pratica,
                    }
                }

            query = {'usuario':email}

            # Opções para filtrar os documentos corretos e criar a coleção se não existir
            opcoes = [
                {'colecao.nome': nome_da_colecao},
                {'trilha.nome': nome_da_trilha}
            ]

            # Atualizar o documento no MongoDB
            x = mongoDB.Progresso.update_one(query, atualizacao, array_filters=opcoes, upsert=True)

        except Exception as e:
            erro_msg("Erro ao sincronizar progresso no db", e)
            return e

def load_trilha_por_colecao_nome(turma, colecao, nome):
    try:
        # Busca a trilha no banco de dados
        trilha_data = mongoDB.Trilhas.find_one(
            {
                turma+'.'+colecao+'.'+nome:{
                    "$exists": True
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
                img_colection=trilha_data[turma][colecao][nome]['img_colection'],
                descricao=trilha_data[turma][colecao][nome]['descricao'],
                quiz=trilha_data[turma][colecao][nome]['options']['quiz'],
                teoria=trilha_data[turma][colecao][nome]['options']['teoria'],
                ar=trilha_data[turma][colecao][nome]['options']['ar'],
                validacao_pratica=trilha_data[turma][colecao][nome]['options']['validacao_pratica'],
                progressivo=trilha_data[turma][colecao][nome]['options']['progressivo'],
                autor=trilha_data[turma][colecao][nome]['autor']
            )
            return trilha
        else:
            return False
    except Exception as e:
        erro_msg("Erro ao carregar trilha", e)
        return False
        
def load_trilhas_por_colecao(turma, colecao):
    try:
        # Consulta o banco de dados para obter os documentos que correspondem à turma e coleção específicas
        query = {turma + '.' + colecao: {"$exists": True}}
        trilhas_cursor = mongoDB.Trilhas.find(query)

        # Inicializa um dicionário para armazenar as trilhas no formato desejado
        trilha = {}

        # Itera pelos documentos retornados pela consulta
        for documento in trilhas_cursor:
            # Extrai o nome da trilha
            trilha_nome = list(documento[turma][colecao].keys())[0]
            
            # Acessa os dados da trilha dentro do documento
            trilha_data = documento[turma][colecao][trilha_nome]
            
            # Adiciona os dados da trilha ao dicionário no formato desejado
            trilha[trilha_nome] = trilha_data

        return trilha


    except Exception as e:
        # Lida com exceções
        print(f"Ocorreu um erro ao carregar trilhas por colecao: {str(e)}")
        return {}

def load_permissoes_por_colecao(turma, colecao):
    try:
        # Consulta o banco de dados para obter os documentos de permissões dos usuários
        # que têm a mesma turma e coleção especificadas
        query = {
            "permissoes."+ turma + '.' + colecao: {"$exists": True}
        }
        permissao_cursor = mongoDB.Permissoes.find(query)

        # Inicializa uma lista para armazenar os documentos de permissão
        permissoes = []

        # Itera pelos documentos retornados pela consulta
        for documento in permissao_cursor:
            # Adiciona o documento de permissão à lista
            permissoes.append(documento)

        return permissoes

    except Exception as e:
        # Lida com exceções
        print(f"Ocorreu um erro ao carregar trilhas por colecao: {str(e)}")
        return {}

def listar_trilhas_por_colecao(turma, colecao):
    try:
        # Consulta o banco de dados para obter os nomes de trilhas da turma e coleção específicas
        query = {turma+'.'+colecao: {"$exists": True}}
        trilhas_cursor = mongoDB.Trilhas.find(query)

        # Lista para armazenar as chaves das trilhas encontradas
        trilhas_encontradas = []

        # Itera pelos documentos retornados
        for documento in trilhas_cursor:
            trilhas_encontradas.extend(documento[turma][colecao].keys())

        return trilhas_encontradas
    except Exception as e:
        erro_msg("Erro ao buscar trilhas por coleção", e)
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
        # Conjunto para armazenar os nomes das coleções (evita duplicatas)
        nomes_colecoes = set()
        for trilhas_turma in trilhas_por_turma:
            for colecao in trilhas_turma[turma].keys():
                nomes_colecoes.add(colecao)  # Adiciona o nome da coleção ao conjunto

        return list(nomes_colecoes)  # Converte o conjunto de volta para uma lista
    except Exception as e:
        erro_msg("Erro ao listar nomes das coleções por turma", e)
        return []

def buscar_nomes_colecoes_por_turma_com_imagem(turma):
    try:
        # Consulta o banco de dados para obter as trilhas da turma específica
        trilhas_por_turma = mongoDB.Trilhas.find(
            {
                turma: {
                    "$exists": True
                }
            }
        )

        colecoes_return = {}
        
        for trilhas_turma in trilhas_por_turma:
            trilhas_da_turma = trilhas_turma[turma]
            for colecao in trilhas_da_turma:
                colecao_dic = trilhas_turma[turma][colecao]

                # Obtém a lista de chaves do dicionário 'colecao_dic'
                chaves = list(colecao_dic.keys())

                # Obtém a última chave do dicionário 'colecao_dic'
                ultima_chave = chaves[-1]

                # Obtém o valor correspondente à última chave
                ultimo_item_valor = colecao_dic[ultima_chave]

                # Verifica se 'ultimo_item_valor' é um dicionário e se contém a chave 'img_colection'
                if isinstance(ultimo_item_valor, dict) and 'img_colection' in ultimo_item_valor:
                    colecoes_return[colecao] = ultimo_item_valor['img_colection']

        return colecoes_return  # Converte o conjunto de volta para uma lista
    except Exception as e:
        erro_msg("Erro ao listar nomes das coleções por turma", e)
        return {}

def delete_trilha(turma, colecao, nome_trilha):
    try:
        # Construa o filtro para encontrar a trilha a ser excluída no DB Trilha
        filtro = {
            turma + '.' + colecao + '.' + nome_trilha: {
                "$exists": True
            }
        }

        # Use delete_one para remover a trilha
        resultado = mongoDB.Trilhas.delete_one(filtro)        

    except Exception as e:
        erro_msg("Erro ao excluir trilha", e)
