from flask import Flask, request, jsonify
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from redis import Redis
from rq import Queue
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sender import registrar_usuario_cola

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportapp.db'


servicio_disponible = True  # Simula la disponibilidad del servicio

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
usuarioSchema = UsuarioSchema()

with app.app_context():
    db.create_all()


@app.route('/usuario-comandos-ins-1/registro', methods=['POST'])
def registrar_usuario():
    global servicio_disponible
    if not servicio_disponible:
        return jsonify({"error": "El servicio de registro no está disponible"}), 503
    usuario = request.json
    usuario = Usuario(username=usuario['username'], password=usuario['password'])
    db.session.add(usuario)
    db.session.commit()
    q.enqueue(registrar_usuario_cola, usuarioSchema.dump(usuario))
    return jsonify({"mensaje": "Usuario registrado exitosamente", "usuario": usuarioSchema.dump(usuario)}), 201

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
