from flask import Flask, request, jsonify
import bcrypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from redis import Redis
from rq import Queue
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sender import registrar_usuario_cola

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/sportapp.db'


servicio_disponible = True  # Simula la disponibilidad del servicio

q = Queue(connection=Redis(host='redis', port=6379, db=0))
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.LargeBinary)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True        
usuarioSchema = UsuarioSchema()

with app.app_context():
    db.create_all()


@app.route('/usuario-comandos-ins-1/registro', methods=['POST'])
def registrar_usuario():
    global servicio_disponible
    if not servicio_disponible:
        return jsonify({"error": "El servicio de registro no está disponible"}), 503
    
    usuario = request.json
    contrasenia = usuario['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(contrasenia, bcrypt.gensalt())
    user = Usuario(username=usuario['username'], password=hashed_password)
    buscar_usuario = Usuario.query.filter(Usuario.username == user.username).first()

    if buscar_usuario is not None:
        return jsonify({"error": "El usuario ya existe"}), 400
    
    db.session.add(user)
    db.session.commit()

    q.enqueue(registrar_usuario_cola, {'username': request.json['username'], 'password': request.json['password']})
    return jsonify({"mensaje": "Usuario registrado exitosamente, prosiga con el login", "usuario": user.username}), 201

@app.route('/usuario-comandos-ins-1/health', methods=['GET'])
def health_check():
    global servicio_disponible
    if servicio_disponible:
        return jsonify({"status": "UP"}), 200
    else:
        return jsonify({"status": "DOWN"}), 400

@app.route('/usuario-comandos-ins-1/activar-registro')
def activar_registro():
    global servicio_disponible
    servicio_disponible = True
    return jsonify({
        "status": servicio_disponible
    })

@app.route('/usuario-comandos-ins-1/desactivar-registro')
def desactivar_registro():
    global servicio_disponible
    servicio_disponible = False
    return jsonify({
        "status": servicio_disponible
    })

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5002)
