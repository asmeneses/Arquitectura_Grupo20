#!/bin/bash

# Define la URL para descargar Docker Desktop para Mac
DOCKER_DESKTOP_URL="https://desktop.docker.com/mac/stable/Docker.dmg"

# Descarga Docker.dmg
echo "Descargando Docker Desktop para Mac..."
curl -L $DOCKER_DESKTOP_URL -o ~/Downloads/Docker.dmg

# Monta el archivo DMG
echo "Montando imagen DMG..."
hdiutil attach ~/Downloads/Docker.dmg

# Abre el instalador de Docker Desktop
# Nota: Este paso abrirá la ventana del instalador, pero la instalación debe completarse manualmente
echo "Abriendo el instalador de Docker Desktop..."
open /Volumes/Docker/Docker.app

echo "Por favor, sigue las instrucciones en la ventana del instalador de Docker Desktop para completar la instalación."
