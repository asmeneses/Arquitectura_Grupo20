from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from redis import Redis
from rq import Queue


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/auth.db'
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)
q = Queue(connection=Redis(host='redis', port=6379, db=0))
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        exclude = ('password',)
usuarioSchema = UsuarioSchema()

with app.app_context():
    db.create_all()

@app.route('/autorizador-comandos/login', methods=['POST'])
def login():
    user = Usuario.query.filter_by(username=request.json['username']).first()

    if user is not None and user.password == (request.json['password']):
        # Crear tokens de acceso y actualización
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    return jsonify({"msg": "Credenciales incorrectas"}), 401

@app.route('/autorizador-comandos/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
