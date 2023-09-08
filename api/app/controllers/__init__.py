from flask import Response
from flask_login import login_manager, current_user

def authenticate(privilegio):
    response = {}
    usuario = current_user.is_authenticated
    print(usuario)
    if usuario: 
        usuario = current_user
        if (usuario.privilegio == privilegio):
            return False
        elif(privilegio == "log"):
            return False
        elif(usuario.privilegio == "administrador"):
            return False
        else:
            response['login'] = False
            response['Retorno'] = 'Acesso negado'
            response['Necessario'] = privilegio
    else:
            response['login'] = False
            response['Retorno'] = 'Acesso negado'
            response['Necessario'] = privilegio
    return response

#Usar:
#    auth = authenticate("adm")
#    if auth:
#        return Response(json.dumps(auth), status=200, mimetype="application/json")