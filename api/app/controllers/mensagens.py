from colorama import Fore, Style

# Função para formatar mensagens de erro
def erro_msg(msg, error):
    return f"{Fore.RED}[ERRO] {msg} -> {error} {Style.RESET_ALL}"