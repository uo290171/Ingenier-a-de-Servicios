# coding: utf8
import socket

PUERTO = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Activamos el modo broadcast en el socket usando setsockopt
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(("", PUERTO))

print(f"Servidor Broadcast escuchando en el puerto {PUERTO}...")

while True:
    datagrama, origen = s.recvfrom(1024)
    mensaje = datagrama.decode("utf8")
    print(f"Recibido de {origen}: {mensaje}")
    
    if mensaje == "BUSCANDO HOLA":
        # Notificamos al cliente que implementamos el servicio
        respuesta = "IMPLEMENTO HOLA"
        s.sendto(respuesta.encode("utf8"), origen)
    elif mensaje == "HOLA":
        # Respondemos con la IP del cliente
        respuesta = f"HOLA: {origen[0]}"
        s.sendto(respuesta.encode("utf8"), origen)
        