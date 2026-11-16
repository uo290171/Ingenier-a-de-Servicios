# coding: utf8
# Experimento del ejercicio 3: el cliente envía primero tres mensajes seguidos
# y después intenta leer las tres respuestas, cada una con un recv().
# Si las respuestas del servidor llegan "pegadas", el primer recv() las recibe
# todas juntas y el cliente se queda colgado en el siguiente recv().
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente Oche (envía seguido) conectado a {host}:{puerto}")

mensajes = ["UNO\r\n", "DOS\r\n", "TRES\r\n"]

# Primero los tres envíos, sin leer nada entre medias
for msg in mensajes:
    s.sendall(bytes(msg, "utf8"))

# Después las tres lecturas
for i in range(len(mensajes)):
    respuesta = s.recv(80)
    respuesta = str(respuesta, "utf8")
    print(repr(respuesta))

s.close()
print("Cliente finalizado y socket cerrado.")
