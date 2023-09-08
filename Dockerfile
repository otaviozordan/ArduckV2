# Use uma imagem base do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Copie o restante do código do projeto para o contêiner
COPY server .

# Exponha a porta que sua aplicação Python irá ouvir
EXPOSE 80

# Comando para executar a sua aplicação quando o contêiner for iniciado
CMD ["python", "api/app.py"]
