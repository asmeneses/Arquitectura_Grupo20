from autorizador import db,Usuario

def registrar_usuario_cola(usuario_data):
    usuario = Usuario(username=usuario_data['username'], password=usuario_data['password'])
    db.session.add(usuario)
    db.session.commit()