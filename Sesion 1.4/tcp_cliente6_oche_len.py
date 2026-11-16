# coding: utf8
# Cliente del servicio "oche" con framing por longitud en ASCII.
# Envía varios mensajes seguidos y después lee las respuestas.
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999


def recvall(sd, n):
    """Recibe exactamente n bytes (o menos si el otro extremo cierra)."""
    trozos = []
    recibidos = 0
    while recibidos < n:
        trozo = sd.recv(n - recibidos)
        if not trozo:
            break
        trozos.append(trozo)
        recibidos += len(trozo)
    return b"".join(trozos)


def recibe_longitud(sd):
    """Lee byte a byte hasta el "\\n" y retorna la longitud como int.
    Retorna None si el otro extremo cerró la conexión."""
    buffer = []
    while True:
        byte = sd.recv(1)
        if not byte:
            return None
        if byte == b"\n":
            break
        buffer.append(byte)
    return int(b"".join(buffer).decode("ascii"))


def recibe_mensaje(sd):
    """Retorna el siguiente mensaje como str, o None si se cerró la conexión."""
    longitud = recibe_longitud(sd)
    if longitud is None:
        return None
    datos = recvall(sd, longitud)
    if len(datos) < longitud:
        return None
    return datos.decode("utf8")


def envia_mensaje(sd, mensaje):
    datos = bytes(mensaje, "utf8")
    longitud = "%d\n" % len(datos)  # Longitud en bytes, no en caracteres
    sd.sendall(bytes(longitud, "ascii") + datos)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente Oche (longitud en ASCII) conectado a {host}:{puerto}")

# Ya no hace falta \r\n: los mensajes pueden contener saltos de línea,
# caracteres no ASCII (que ocupan más de un byte) o superar los 80 bytes.
mensajes = [
    "HOLA",
    "Línea con\r\nsalto en medio",
    "ÑANDÚ",
    "X" * 50 + "Y" * 50 + "Z" * 50,
]

for msg in mensajes:
    envia_mensaje(s, msg)

for i in range(len(mensajes)):
    respuesta = recibe_mensaje(s)
    print(f"Respuesta {i+1}: {respuesta!r}")

s.close()
print("Cliente finalizado y socket cerrado.")
