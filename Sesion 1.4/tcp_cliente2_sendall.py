# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente TCP (con sendall) conectado a {host}:{puerto}")

# Enviar 5 veces "ABCDE" usando sendall para asegurar el envío completo
for i in range(5):
    s.sendall(b"ABCDE")

# Enviar el mensaje de finalización
s.sendall(b"FINAL")

s.close()
print("Cliente finalizado y socket cerrado.")
