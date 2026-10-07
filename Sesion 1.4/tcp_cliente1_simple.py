# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente TCP conectado a {host}:{puerto}")

# Enviar 5 veces "ABCDE" (exactamente 5 bytes cada uno)
for i in range(5):
    s.send(b"ABCDE")

# Enviar el mensaje de finalización
s.send(b"FINAL")

s.close()
print("Cliente finalizado y socket cerrado.")
