# SportApp Microservicios Disponibilidad

## Instalación
### MacOS

Para realizar la instalación ejecute el comando:

```
./install_mac_os.sh
```
Se empezará a descargar la imagen de Docker Desktop, espere que termine la descarga y sig alas instrucciones.

### Linux

Para realizar la instalación ejecute el comando:

```
./install.sh
```

Durante este proceso el sistema se actualizará e instalará todas las dependencias necesarias.


## Empezar el experimento
### MacOS

Una vez haya finalizado con el proceso de instalación verifique que docker y docker compose están instalados en su OS, para esto use los comandos:

```
docker --version
```

```
docker-compose --version
```
-------------------
- Ejecute el siguiente comando para crear las instancias de docker:

```
docker-compose build --no-cache
```

- Ejecute el siguiente comando para levantar las instancias de docker:
```
docker-compose up -d
```

1. Verifique en que puertos están corriendo las instancias de docker, para esto use el comando:

```
ifconfig | grep 192
```

La terminal mostrará un output similar a este:
```
inet 192.168.1.1 netmask 0xffffff00 broadcast 192.168.1.255
```

Use la dirección IP que aparece después de inet.

### Linux

Una vez finalice la instalación se crearán los contenedores de docker y empezarán a correr con los diferentes servicios.

# Descripción del experimento 2:
* [Video demostración]()

# Descripción del experimento 1:


Podrá ver diferentes instancias de docker:
- nginx-1: API Gateway
- Monitor: Revisa la salud de los servicios de registro
- Registro: Registra los usuarios en la plataforma. (Replica pasiva)
- Orquestador: Actúa como una API de alto nivel que enmascara el error de la instancia principal de registros y redirige los registros para la instancia secundaria.

Endpoints para replicar el experimento:

- http://localhost:5002/api/start: Empieza el orquestador

Ejecuta el comando para empezar con la simulación de registros, durante este proceso la instancia 1 fallará y la instancia 2 del servicio de registros tomará su lugar. Una vez la instancia 1 se reestablezca, tomará control del servicio de registros nuevamente:
```
python3 run-tests.py
```
