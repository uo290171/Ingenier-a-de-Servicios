# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente Oche mejorado conectado a {host}:{puerto}")

# Enviar varios mensajes seguidos sin intercalar lecturas
mensajes = ["UNO\r\n", "DOS\r\n", "TRES\r\n"]

for msg in mensajes:
    s.sendall(bytes(msg, "utf8"))

# Leer las respuestas correspondientes
for i in range(len(mensajes)):
    respuesta_bytes = b""
    while not respuesta_bytes.endswith(b"\r\n"):
        byte = s.recv(1)
        if not byte:
            break
        respuesta_bytes += byte
        
    print(f"Recibida respuesta {i+1}: {repr(str(respuesta_bytes, 'utf8'))}")

s.close()
print("Cliente finalizado y socket cerrado.")
