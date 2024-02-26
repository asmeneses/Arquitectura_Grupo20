from flask import Flask, request, jsonify
from requests import post
import redis

app = Flask(__name__)

servicio_registro = 'http://registro1:5002/usuario-comandos-ins-1'

@app.route('/api/registro', methods=['POST'])
def registrar_usuario():
    global servicio_registro
    peticion = post(f'{servicio_registro}/registro', json=request.json).json()
    return jsonify(peticion)

@app.route('/api/servicio', methods=['GET'])
def health_check():
    global servicio_registro
    return jsonify(servicio_registro)

def startup():
    r = redis.Redis(host='redis', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe(['server'])

    print('Suscriptor esperando mensajes...')
    for message in pubsub.listen():
        if message['type'] == 'message':
            global servicio_registro
            servicio_registro = message['data'].decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
    startup()
