# coding: utf8
import sys
import socket

PUERTO = 12345
# Se puede pasar la IP de broadcast por argumento, o usar la genérica por defecto
BROADCAST_IP = sys.argv[1] if len(sys.argv) > 1 else "255.255.255.255"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Activamos el modo broadcast en el socket del cliente
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print(f"Enviando petición de búsqueda por broadcast a {BROADCAST_IP}:{PUERTO}...")
s.sendto(b"BUSCANDO HOLA", (BROADCAST_IP, PUERTO))

# Fijamos un timeout para recoger las respuestas de todos los servidores activos
s.settimeout(1.0)
primer_servidor_ip = None

try:
    while True:
        datagrama, origen = s.recvfrom(1024)
        respuesta = datagrama.decode("utf8")
        print(f"Servidor encontrado en {origen[0]} responde: {respuesta}")
        if not primer_servidor_ip:
            primer_servidor_ip = origen[0]
except socket.timeout:
    print("Fin del tiempo de espera para recepción de respuestas broadcast.")

if primer_servidor_ip:
    print(f"\nProbando servicio con el primer servidor detectado: {primer_servidor_ip}")
    s.sendto(b"HOLA", (primer_servidor_ip, PUERTO))
    
    s.settimeout(1.0)
    try:
        datagrama, origen = s.recvfrom(1024)
        print(f"Respuesta del servicio: {datagrama.decode('utf8')} (de {origen})")
    except socket.timeout:
        print("No se recibió respuesta del servicio HOLA.")
else:
    print("No se encontró ningún servidor activo.")

s.close()
