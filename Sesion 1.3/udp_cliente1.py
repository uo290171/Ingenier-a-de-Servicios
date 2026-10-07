# coding: utf8
import sys
import socket

# Leer IP y puerto del servidor por argumentos o usar valores por defecto
host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Cliente UDP conectado para enviar a {host}:{puerto}")
print("Escribe tus mensajes (escribe FIN para terminar):")

while True:
    mensaje = input("> ")
    if mensaje == "FIN":
        break
    # Enviar el mensaje codificado en bytes a la tupla (host, puerto)
    s.sendto(mensaje.encode("utf8"), (host, puerto))

s.close()