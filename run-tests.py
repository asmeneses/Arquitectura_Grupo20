from requests import get, post
import random
import time
numero_peticiones = 100

peticion_botar_servicio = random.randint(1, numero_peticiones/4)

for i in range(numero_peticiones):
    if i == peticion_botar_servicio:
        peticion = get('http://localhost:5002/usuario-comandos-ins-1/desactivar-registro').json()
        servicio = get('http://localhost:5002/api/servicio').json()
    else:
        peticion = post('http://localhost:5002/api/registro', json={"nombre": "usuario" + str(i)}).json()
        servicio = get('http://localhost:5002/api/servicio').json()

    time.sleep(1)
    print(peticion)
    print(servicio)
    print('\n\n')


