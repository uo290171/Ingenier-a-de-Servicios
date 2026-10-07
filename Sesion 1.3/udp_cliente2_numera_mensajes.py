# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Cliente UDP (numerando mensajes) para enviar a {host}:{puerto}")
print("Escribe tus mensajes (escribe FIN para terminar):")

contador = 1
while True:
    texto = input("> ")
    if texto == "FIN":
        break
    
    mensaje = f"{contador}: {texto}"
    s.sendto(mensaje.encode("utf8"), (host, puerto))
    contador += 1

s.close()