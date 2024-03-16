from autorizador import app, db, Usuario

def registrar_usuario_cola(usuario_data):
    usuario = Usuario(username=usuario_data['username'], password=usuario_data['password'])

    with app.app_context():
        db.session.add(usuario)
        db.session.commit()

        regUsuario = Usuario.query.filter(Usuario.username == usuario.username,
                                Usuario.password == usuario.password).first()

        print(f'Usuario registrado: {regUsuario}')