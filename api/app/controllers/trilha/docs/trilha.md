# Documentação da Aplicação Flask

Esta documentação descreve a implementação e o funcionamento de uma aplicação web baseada em Flask. A aplicação permite a criação, listagem e manipulação de trilhas educacionais, bem como a interação com questionários associados a essas trilhas. A aplicação é projetada para ser utilizada por professores e alunos em um ambiente educacional.

## Endpoints da Aplicação

### 1. Cadastro de Trilha

- **Rota**: `/cadastrartrilha`
- **Método**: `POST`
- **Descrição**: Permite aos professores cadastrar uma nova trilha educacional.

**Parâmetros de Requisição:**
- `colecao` (string): Nome da coleção à qual a trilha pertencerá.
- `trilha` (string): Nome da trilha.
- `ordem` (int): A ordem da trilha.
- `img_path` (string): O caminho da imagem associada à trilha.
- `descricao` (string): A descrição da trilha.
- `teoria` (string): Conteúdo teórico da trilha.
- `quiz` (lista de objetos): Lista de questionários associados à trilha.
- `validacao_pratica` (string): Informação sobre a validação prática da trilha.
- `ar` (string): Informação sobre a avaliação da trilha.
- `progressivo` (boolean): Define se a trilha é progressiva ou não.

**Respostas:**
- `Status 200`: Trilha cadastrada com sucesso. Retorna um JSON com os detalhes da trilha.
- `Status 400`: Parâmetros inválidos ou ausentes na requisição.
- `Status 401`: Falha na autenticação do professor.
- `Status 500`: Erro interno do servidor ao cadastrar a trilha.

### 2. Listar Coleções

- **Rota**: `/listar_colecoes`
- **Método**: `GET`
- **Descrição**: Lista todas as coleções disponíveis para o usuário logado.

**Respostas:**
- `Status 200`: Retorna um JSON com a lista de coleções.
- `Status 401`: Falha na autenticação do usuário.
- `Status 500`: Erro interno do servidor ao listar coleções.

### 3. Buscar Trilha

- **Rota**: `/buscartrilha`
- **Método**: `POST`
- **Descrição**: Busca uma trilha específica pelo nome e pela coleção.

**Parâmetros de Requisição:**
- `colecao` (string): Nome da coleção à qual a trilha pertence.
- `trilha` (string): Nome da trilha a ser buscada.

**Respostas:**
- `Status 200`: Retorna um JSON com os detalhes da trilha encontrada.
- `Status 400`: Parâmetros inválidos ou ausentes na requisição.
- `Status 401`: Falha na autenticação do usuário.
- `Status 500`: Erro interno do servidor ao buscar a trilha.

### 4. Listar Trilhas por Coleção

- **Rota**: `/listartrilha_por_colecao/<colecao>`
- **Método**: `GET`
- **Descrição**: Lista todas as trilhas disponíveis em uma coleção específica.

**Respostas:**
- `Status 200`: Retorna um JSON com a lista de trilhas encontradas.
- `Status 401`: Falha na autenticação do usuário.
- `Status 500`: Erro interno do servidor ao listar trilhas.

### 5. Listar Trilhas por Coleção Permitida

- **Rota**: `/listartrilha_por_colecao_permitida/<colecao>`
- **Método**: `GET`
- **Descrição**: Lista todas as trilhas com permissão de acesso em uma coleção específica.

**Respostas:**
- `Status 200`: Retorna um JSON com a lista de trilhas com permissão de acesso.
- `Status 401`: Falha na autenticação do usuário.
- `Status 500`: Erro interno do servidor ao listar trilhas com permissão.

### 6. Carregar Quiz

- **Rota**: `/carregarquiz`
- **Método**: `POST`
- **Descrição**: Carrega um questionário associado a uma trilha específica.

**Parâmetros de Requisição:**
- `colecao` (string): Nome da coleção à qual a trilha pertence.
- `trilha` (string): Nome da trilha.
 
**Respostas:**
- `Status 200`: Retorna um JSON com o questionário da trilha.
- `Status 400`: Parâmetros inválidos ou ausentes na requisição.
- `Status 401`: Falha na autenticação do usuário.
- `Status 500`: Erro interno do servidor ao carregar o questionário.

### 7. Verificar Quiz

- **Rota**: `/verifiacarquiz`
- **Método**: `POST`
- **Descrição**: Verifica as respostas dadas pelo usuário em um questionário.

**Parâmetros de Requisição:**
- `colecao` (string): Nome da coleção à qual a trilha pertence.
- `trilha` (string): Nome da trilha.
- `numero` (int): Número da pergunta no questionário.
- `resposta` (string): Resposta dada pelo usuário.

**Respostas:**
- `Status 200`: Retorna um JSON com a resposta correta e se a resposta do usuário estava correta.
- `Status 400`: Parâmetros inválidos ou ausentes na requisição.
- `Status 401`: Falha na autenticação do usuário.
- `Status 500`: Erro interno do servidor ao verificar o questionário.

### 8. Cadastrar Progresso

- **Rota**: `/cadastrarprogresso`
- **Método**: `POST`
- **Descrição**: Registra o progresso do usuário em uma trilha.

**Parâmetros de Requisição:**
- `colecao` (string): Nome da coleção à qual a trilha pertence.
- `trilha` (string): Nome da trilha.
- `elemento` (string): Elemento da trilha em que o progresso será registrado.

**Respostas:**
- `Status 200`: Progresso registrado com sucesso.
- `Status 400`: Parâmetros inválidos ou ausentes na requisição.
- `Status 401`: Falha na autenticação do usuário.
- `Status 500`: Erro interno do servidor ao registrar o progresso.

## Autenticação

A autenticação é necessária para acessar as rotas que requerem permissões específicas. Os professores têm acesso a funcionalidades adicionais em comparação com os alunos.

## Considerações Finais

Esta documentação fornece uma visão geral das funcionalidades da aplicação Flask e dos endpoints disponíveis. Certifique-se de que a autenticação seja implementada adequadamente para proteger as rotas relevantes. É importante seguir as convenções de nomenclatura e estrutura de dados para garantir o funcionamento correto da aplicação.
