# coding: utf8
import sys
import socket
import random

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print(f"Servidor UDP (con OK) escuchando en puerto {puerto}...")

while True:
    datagrama, origen = s.recvfrom(1024)
    
    # Simulación de pérdida con un 50% de probabilidad
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido...")
    else:
        print(f"Recibido de {origen}: {datagrama.decode('utf8')}")
        # Enviamos la confirmación "OK" al cliente
        s.sendto(b"OK", origen)