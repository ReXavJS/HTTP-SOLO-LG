# TCP-SOLO-LG

docker-compose.yml à mettre à la racine du projet

version: "3.8"

services:
  flask-server:
    build:
      context: ./TCP-SOLO-LG/http_server
    ports:
      - "5000:5000"
    restart: unless-stopped
    command: python run.py


  moteur-administration:
    build:
      context: ./TCP-SOLO-LG/admin
    ports:
      - "6000:6000"
    restart: unless-stopped
    command: python moteur_administration.py

  serveur-tcp:
    build:
      context: /TCP-SOLO-LG/interface-TCP
    ports:
      - "65432:65432"  
    restart: unless-stopped
    command: python server_tcp.py
