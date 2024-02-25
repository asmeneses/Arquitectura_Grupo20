
def registrar_usuario_background(usuario, fecha):
    with open('log_register.txt','a') as file:
        file.write('{} - Se trato de registrar un usuario:{}\n'.format(usuario, fecha))