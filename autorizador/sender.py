from autorizador import app, db, Usuario
import bcrypt
import pyotp

def registrar_usuario_cola(usuario_data):
    contrasenia = usuario_data['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(contrasenia, bcrypt.gensalt())
    usuario = Usuario(
        username=usuario_data['username'], 
        password=hashed_password, 
        key2fa=usuario_data['key2fa'])
    with app.app_context():        
        db.session.add(usuario)
        db.session.commit()

        regUsuario = Usuario.query.filter(Usuario.username == usuario.username,
                                Usuario.password == usuario.password).first()

        print(f'Usuario registrado: {regUsuario}')