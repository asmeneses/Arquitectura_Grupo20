import requests
import redis
import time
from monitor_utils import reiniciar_contenedor

# servicios_registro[0] es el servicio principal
# servicios_registro[1] es el servicio backup
servicios_registro = ['http://registro1:5002/usuario-comandos-ins-1', 'http://registro2:5002/usuario-comandos-ins-2']
servicios_nombre = ['registro1', 'registro2']
servicio_principal = 0


def check_health(servicio):
    try:
        response = requests.get(f'{servicio}/health')
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
    global servicio_principal
    r = redis.Redis(host='redis', port=6379, db=0)
    while True:
        # Reviso el estado de los servicios de registro
        for i in range(len(servicios_registro)):
            response = check_health(servicios_registro[i])

            if response:
                r.publish('events', 'El servicio de registro está funcionando correctamente')
            else:
                reiniciar_contenedor(servicios_nombre[i])   
                print("El servicio de registro está caído, intentando reiniciar")
                r.publish('events', 'El servicio de registro está caído, intentando reiniciar')

            # Si el servicio principal está activo uso ese endpoint, sino uso el backup
            servicio = servicios_registro[0] if servicio_principal == i and response else servicios_registro[1]
            r.publish('server', f'{servicio}')


        # if check_health():
        #     r.publish('events', 'El servicio de registro está funcionando correctamente')
        # else:
        #     reiniciar_contenedor('registro')
        #     print("El servicio de registro está caído, intentando reiniciar")
        #     r.publish('events', 'El servicio de registro está caído, intentando reiniciar')

        time.sleep(1)

if __name__ == '__main__':
    main()
