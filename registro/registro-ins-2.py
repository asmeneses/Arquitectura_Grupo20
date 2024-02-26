from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import sqlalchemy
from datetime import datetime
from registrar_usuario_background import registrar_usuario_background

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/registro.db'
#db = sqlalchemy(app)

usuarios_registrados = []
servicio_disponible = True  # Simula la disponibilidad del servicio

q = Queue(connection=Redis(host='redis', port=6379, db=0))


@app.route('/usuario-comandos-ins-2/registro', methods=['POST'])
def registrar_usuario():
    global servicio_disponible
    if not servicio_disponible:
        return jsonify({"error": "El servicio de registro no está disponible"}), 503
    usuario = request.json
    q.enqueue(registrar_usuario_background, usuario, datetime.utcnow())
    return jsonify({"mensaje": "Usuario registrado exitosamente", "usuario": usuario}), 201

@app.route('/usuario-comandos-ins-2/health', methods=['GET'])
def health_check():
    global servicio_disponible
    if servicio_disponible:
        return jsonify({"status": "UP"}), 200
    else:
        return jsonify({"status": "DOWN"}), 400

@app.route('/usuario-comandos-ins-2/activar-registro')
def activar_registro():
    global servicio_disponible
    servicio_disponible = True
    return jsonify({
        "status": servicio_disponible
    })

@app.route('/usuario-comandos-ins-2/desactivar-registro')
def desactivar_registro():
    global servicio_disponible
    servicio_disponible = False
    return jsonify({
        "status": servicio_disponible
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
