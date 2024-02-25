import requests
import redis
import time
from monitor_utils import reiniciar_contenedor

def check_health():
    try:
        response = requests.get('http://registro:5002/usuario-comandos/health')
        if response.status_code == 200:
            print("El servicio de registro está UP")
            return True
        else:
            print("El servicio de registro está DOWN")
            return False
    except requests.exceptions.RequestException as e:
        print("No se pudo conectar al servicio de registro")
        return False

def main():
    r = redis.Redis(host='redis', port=6379, db=0)
    while True:
        if check_health():
            r.publish('events', 'El servicio de registro está funcionando correctamente')                    
        else:
            # TODO: Implementar el reinicio del servicio
            print("El servicio de registro está caído, intentando reiniciar")
            reiniciar_contenedor('registro')
            r.publish('events', 'El servicio de registro está caído, intentando reiniciar')            
        time.sleep(1)

if __name__ == '__main__':
    main()
