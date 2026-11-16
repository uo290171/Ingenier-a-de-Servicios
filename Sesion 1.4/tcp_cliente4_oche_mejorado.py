# coding: utf8
# Basado en tcp_cliente3_oche_envia_seguido.py: envía tres mensajes seguidos y
# después lee las tres respuestas, pero usando recibe_mensaje() para separar
# correctamente cada línea aunque lleguen "pegadas".
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999


def recibe_mensaje(sd):
    """Lee del socket byte a byte hasta encontrar el terminador \\r\\n.

    Retorna la línea completa (bytes) incluyendo el \\r\\n final, o b"" si el
    otro extremo cerró la conexión sin enviar nada más.
    """
    buffer = []
    while True:
        byte = sd.recv(1)
        if not byte:
            break
        buffer.append(byte)
        if b"".join(buffer[-2:]) == b"\r\n":
            break
    return b"".join(buffer)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente Oche mejorado conectado a {host}:{puerto}")

mensajes = ["UNO\r\n", "DOS\r\n", "TRES\r\n"]

# Primero los tres envíos seguidos
for msg in mensajes:
    s.sendall(bytes(msg, "utf8"))

# Después leer las tres respuestas, una línea completa cada vez
for i in range(len(mensajes)):
    respuesta = recibe_mensaje(s)
    print(f"Recibida respuesta {i+1}: {repr(str(respuesta, 'utf8'))}")

s.close()
print("Cliente finalizado y socket cerrado.")
