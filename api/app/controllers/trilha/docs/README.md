# Documentação da API de Upload de Arquivos

Esta documentação descreve como utilizar a API de upload de arquivos em uma página da web. A API é construída com o framework Flask em Python e pode ser usada para fazer o upload de arquivos, como imagens, para um servidor web. Ela também inclui verificações de autenticação e validações para garantir a segurança e a integridade dos arquivos enviados.

## Requisitos

Antes de usar esta API, é importante garantir que você atenda aos seguintes requisitos:

1. Ter o Python instalado (versão 3.6 ou superior).
2. Instalar as dependências necessárias listadas no arquivo de requisitos do projeto, normalmente chamado `requirements.txt`.

## Endpoint da API

A API possui um único endpoint para fazer o upload de arquivos:

- **Método HTTP**: POST
- **URL**: `/upload_file/<acao>`
- **Parâmetros da URL**:
  - `<acao>`: Uma string que especifica a ação a ser executada durante o upload (por exemplo, 'icon' ou 'teoria').

## Autenticação

A API exige autenticação para garantir que apenas usuários autorizados possam fazer uploads. Atualmente, apenas os usuários com a função 'professor' estão autorizados. A autenticação é implementada através da função `authenticate('professor')`.

## Requisitos do Formulário

Para fazer um upload bem-sucedido, é necessário enviar um formulário com os seguintes campos:

1. **file**: O campo para selecionar o arquivo a ser enviado.
2. **metadata**: Um campo JSON que contém informações sobre o arquivo a ser enviado. Deve conter as chaves 'colecao' e 'trilha'.

## Estrutura do JSON de Metadata

O JSON enviado no campo 'metadata' deve ter a seguinte estrutura:

```json
{
    "colecao": "nome_da_colecao",
    "trilha": "nome_da_trilha"
}

## Coleção e Trilha

- **Coleção:** O nome da coleção à qual o arquivo pertence.
- **Trilha:** O nome da trilha à qual o arquivo pertence.

## Construção do Nome do Arquivo

O nome do arquivo é construído com base nas informações fornecidas no JSON de metadata e na ação especificada na URL.

- Se a ação for 'icon', o nome do arquivo será construído como: `current_user.turma/colecao/trilha/icon.extensao`.
- Se a ação for 'teoria', o nome do arquivo será construído como: `current_user.turma/colecao/trilha/teoria/<número_do_arquivo>.extensao`. O número do arquivo é incrementado automaticamente.

## Exemplo de Uso

Aqui está um exemplo de como usar a API de upload de arquivos em uma página da web:

```html
<form action="/upload_file/icon" method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="hidden" name="metadata" value='{"colecao": "minha_colecao", "trilha": "minha_trilha"}'>
    <input type="submit" value="Enviar Arquivo">
</form>

Lembre-se de que você deve substituir os valores de 'colecao' e 'trilha' com os nomes apropriados para o seu caso de uso.

## Respostas da API

A API retornará respostas JSON que indicam o resultado do upload:

### Upload Bem-Sucedido

Se o upload for bem-sucedido, você receberá uma resposta com um status HTTP 200 e uma mensagem de sucesso, juntamente com o novo nome do arquivo.

```json
{
    "upload": true,
    "message": "Arquivo 'nome_do_arquivo' renomeado para 'novo_nome_do_arquivo' e salvo com sucesso!",
    "new_filename": "novo_nome_do_arquivo"
}

# Erro no Processo de Upload

Se houver algum erro no processo de upload, você receberá uma resposta com um status HTTP 400 e uma mensagem de erro.

```json
{
    "upload": false,
    "Retorno": "Erro",
    "erro": "Descrição do erro"
}


##Considerações Finais
Certifique-se de entender completamente os requisitos da API e fornecer as informações necessárias no formulário para que o upload funcione corretamente. Além disso, lembre-se de implementar a lógica de autenticação apropriada para proteger seus uploads contra acesso não autorizado.

