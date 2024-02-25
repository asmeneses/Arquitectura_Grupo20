from flask import Flask, request, jsonify
app = Flask(__name__)

usuarios_registrados = []
servicio_disponible = True  # Simula la disponibilidad del servicio

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    global servicio_disponible
    if not servicio_disponible:
        return jsonify({"error": "El servicio de registro no está disponible"}), 503
    usuario = request.json
    usuarios_registrados.append(usuario)
    return jsonify({"mensaje": "Usuario registrado exitosamente", "usuario": usuario}), 201

@app.route('/health', methods=['GET'])
def health_check():
    global servicio_disponible
    if servicio_disponible:
        return jsonify({"status": "UP"}), 200
    else:
        return jsonify({"status": "DOWN"}), 400

@app.route('/activar-registro')
def activar_registro():
    global servicio_disponible
    servicio_disponible = True
    return jsonify({
        "status": servicio_disponible
    })

@app.route('/desactivar-registro')
def desactivar_registro():
    global servicio_disponible
    servicio_disponible = False
    return jsonify({
        "status": servicio_disponible
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)
