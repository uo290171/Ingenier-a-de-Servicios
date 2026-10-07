# coding: utf8
import sys
import socket

# Si se pasa un puerto por argumento se usa, si no el 9999 por defecto
puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# Crear socket UDP (AF_INET para IPv4, SOCK_DGRAM para UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print(f"Servidor UDP escuchando en el puerto {puerto}...")

while True:
    # Recibir datagrama (máximo 1024 bytes)
    datagrama, origen = s.recvfrom(1024)
    print(f"Recibido de {origen}: {datagrama.decode('utf8')}")