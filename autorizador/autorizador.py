from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from redis import Redis
from rq import Queue
import requests
import bcrypt
import pyotp
from flask_qrcode import QRcode

user_secret = -1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/auth.db'
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
QRcode(app)

jwt = JWTManager(app)
q = Queue(connection=Redis(host='redis', port=6379, db=0))
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.LargeBinary)
    key2fa = db.Column(db.String(100), nullable=True, default=None)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        #exclude = ('password',)
usuarioSchema = UsuarioSchema()

with app.app_context():
    db.create_all()

@app.route('/autorizador-comandos/login', methods=['POST'])
def login():
    user = Usuario.query.filter_by(username=request.json['username']).first()
    contrasenia = request.json['password'].encode('utf-8')        
    key2fa = request.json['key2fa']

    if user is None:
        return jsonify({"msg": "El usuario no existe"}), 401

    if bcrypt.checkpw(contrasenia, user.password) is False:
        return jsonify({"msg": "Credenciales incorrectas", 'user': usuarioSchema.dump(user)}), 401
    
    if verify_2fa(user, key2fa) is False:
        return jsonify({"msg": "Autenticacion 2FA fallida"}), 401

    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

    

@app.route('/autorizador-comandos/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token)


@app.route('/autorizador-comandos/2fa-login/<username>', methods=['GET'])
def setup_2fa(username):
    user = Usuario.query.filter_by(username=username).first()
    #user_secret = pyotp.random_base32()
    url = pyotp.totp.TOTP(user.key2fa).provisioning_uri(name=username, issuer_name="SportApp")
    return render_template("setup_2fa.html", qr_url=url)

#@app.route('/autorizador-comandos/2fa-login', methods=['POST'])
def verify_2fa(user: Usuario, key2fa: str):
    print(f'El usuario tiene el secreto: {user_secret}')
    totp = pyotp.TOTP(user.key2fa)
    puede_acceder = totp.verify(key2fa)
    return puede_acceder
    print(f'El usuario puede acceder: {puede_acceder}')
    if puede_acceder:
        return jsonify({"msg": "Autenticación exitosa"}), 200
    else:
        return jsonify({"msg": "Autenticación fallida"}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
