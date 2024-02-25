import subprocess

def reiniciar_contenedor(nombre_contenedor):
    '''Reinicia una instancia de docker
        parameters:
            - nombre_contenedor: El nombre real o ID del contenedor
    '''
    try:
        # Ejecutar el comando para reiniciar el contenedor
        subprocess.check_call(['docker', 'restart', nombre_contenedor])
        print(f"Contenedor {nombre_contenedor} reiniciado exitosamente.")
    except subprocess.CalledProcessError as e:
        # Manejar el caso en que el comando falla
        print(f"Error al reiniciar el contenedor {nombre_contenedor}: {e}")
