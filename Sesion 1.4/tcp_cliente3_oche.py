# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente Oche conectado a {host}:{puerto}")

# Enviar algunas líneas de prueba finalizadas con \r\n
mensajes = ["HOLA\r\n", "UNIVERSIDAD\r\n", "OVIEDO\r\n"]

for msg in mensajes:
    s.sendall(bytes(msg, "utf8"))
    # Leer la respuesta del servidor
    respuesta = s.recv(80)
    print(f"Enviado: {msg.strip()} --> Recibido eco: {str(respuesta, 'utf8').strip()}")

s.close()
print("Cliente finalizado y socket cerrado.")
