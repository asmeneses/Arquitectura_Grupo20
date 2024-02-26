import requests
import redis
import time
from monitor_utils import reiniciar_contenedor

# servicios_registro[0] es el servicio principal
# servicios_registro[1] es el servicio backup
servicios_registro = ['http://registro1:5002/usuario-comandos-ins-1', 'http://registro2:5002/usuario-comandos-ins-2']
servicios_nombre = ['registro1', 'registro2']
servicio_principal = 0

ultimo_servicio_usado = 'http://registro1:5002/usuario-comandos-ins-1'

def check_health(servicio):
    try:
        response = requests.get(f'{servicio}/health')
        if response.status_code == 200:
            # print("El servicio de registro está UP")
            return True
        else:
            # print("El servicio de registro está DOWN")
            return False
    except requests.exceptions.RequestException as e:
        # print("No se pudo conectar al servicio de registro")
        return False

def main():
    global servicio_principal
    global ultimo_servicio_usado

    r = redis.Redis(host='redis', port=6379, db=0)
    r.publish('server', f'{ultimo_servicio_usado}')

    while True:
        usarServicio1 = False

        # Reviso el estado de los servicios de registro
        for i in range(len(servicios_registro)):
            response = check_health(servicios_registro[i])
            if i == 0 and response == False:
                r.publish('service', f'{servicios_registro[1]}')

                # Reiniciando servicio principal
                reiniciar_contenedor(servicios_nombre[i])
                r.publish('events', f'El servicio de {servicios_nombre[i]} está caído, intentando reiniciar')
            elif i == 0 and response == True:
                r.publish('service', f'{servicios_registro[0]}')
                r.publish('events', f'El servicio de {servicios_nombre[i]} está funcionando correctamente')

        time.sleep(1)

if __name__ == '__main__':
    main()
