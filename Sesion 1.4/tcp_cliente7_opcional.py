# coding: utf8
# Cliente del servicio "oche" con la longitud en binario (2 bytes big endian).
import sys
import socket
import struct

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


def recibe_mensaje(sd):
    """Retorna el siguiente mensaje como str, o None si se cerró la conexión."""
    cabecera = recvall(sd, 2)
    if len(cabecera) < 2:
        return None
    (longitud,) = struct.unpack(">H", cabecera)
    datos = recvall(sd, longitud)
    if len(datos) < longitud:
        return None
    return datos.decode("utf8")


def envia_mensaje(sd, mensaje):
    datos = bytes(mensaje, "utf8")
    if len(datos) > 0xFFFF:
        raise ValueError("Mensaje demasiado largo para 2 bytes de longitud")
    sd.sendall(struct.pack(">H", len(datos)) + datos)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, puerto))

print(f"Cliente Oche (longitud binaria >H) conectado a {host}:{puerto}")

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
