# Crea los servicios

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'API Gateway Home'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
