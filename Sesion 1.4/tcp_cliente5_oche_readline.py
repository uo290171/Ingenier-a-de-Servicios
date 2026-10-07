# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente Oche readline conectado a {host}:{puerto}")

# Usamos también makefile en el cliente para leer cómodamente con readline
f = s.makefile(encoding="utf8", newline="\r\n")

mensajes = ["HOLA\r\n", "REDES\r\n", "SERVICIOS\r\n"]

for msg in mensajes:
    s.sendall(bytes(msg, "utf8"))

for i in range(len(mensajes)):
    respuesta = f.readline()
    print(f"Recibido eco: {repr(respuesta.strip())}")

f.close()
s.close()
print("Cliente finalizado y socket cerrado.")
