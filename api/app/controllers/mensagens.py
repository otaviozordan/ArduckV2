from colorama import Fore, Style
from flask import Response
import json

def escrever_mensagem(mensagem):
    arquivo = open('arquivo_log.txt', 'a')

    from datetime import datetime
    data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mensagem_formatada = f'[{data_hora_atual}] {mensagem}\n'
    arquivo.write(mensagem_formatada)

    arquivo.close()

# Função para formatar mensagens de erro
def erro_msg(msg, error):
    escrever_mensagem(f"[ERRO] {msg} -> {error}")
    print(f"{Fore.RED}[ERRO] {msg} -> {error} {Style.RESET_ALL}")
    response = {
        'erro':'fatal erro',
        'msg': msg + " -> " + str(error),
    }
    return Response(json.dumps(response), status=500, mimetype="application/json")

# Função para formatar mensagens de erro
def normal_msg(msg, error):
    escrever_mensagem(f"[INFO] {msg} -> {error}")
    print(f"{Fore.GREEN}[INFO] {msg} -> {error} {Style.RESET_ALL}")
    response = {
        'erro':'fatal erro',
        'msg': msg + " -> " + str(error),
    }
    return Response(json.dumps(response), status=500, mimetype="application/json")