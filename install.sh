#!/bin/bash

echo actualizando sistema e instalando dependencias

# Update package index
sudo apt update

# Install dependencies to add Docker repository
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update package index again after adding Docker repository
sudo apt update

# Install Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to Docker Compose
sudo chmod +x /usr/local/bin/docker-compose

# Create symbolic link to make Docker Compose accessible from anywhere in the terminal
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Display installed versions
docker --version
docker-compose --version

# Creates container services
docker-compose build --no-cache

# Starts services
docker-compose up -d
