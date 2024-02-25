import docker

client = docker.from_env()

def reiniciar_contenedor(nombre_contenedor):
    '''Reinicia una instancia de docker
        parameters:
            - nombre_contenedor: El nombre real o ID del contenedor
    '''
    try:
        contenedor = client.containers.get(nombre_contenedor)
        contenedor.restart()
        print(f"Contenedor {nombre_contenedor} reiniciado exitosamente.")
    except docker.errors.NotFound:
        print(f"El contenedor {nombre_contenedor} no se encontró.")
    except Exception as e:
        print(f"Error al reiniciar el contenedor {nombre_contenedor}: {e}")
