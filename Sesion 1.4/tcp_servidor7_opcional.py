# coding: utf8
# Servicio "oche" con framing por longitud en binario:
# cada mensaje va precedido de su longitud en bytes, codificada como
# unsigned short (2 bytes) big endian con struct.pack(">H", ...).
import sys
import socket
import time
import struct

# Uso: python3 <servidor>.py [puerto] [--sleep]
# --sleep: espera 1 s tras el accept() para que los mensajes del cliente
#          se acumulen en el buffer del socket (experimento del guion)
args = sys.argv[1:]
retardo = "--sleep" in args
args = [a for a in args if a != "--sleep"]
puerto = int(args[0]) if args else 9999


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
    cabecera = recvall(sd, 2)  # Siempre 2 bytes: no hace falta buscar terminador
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
s.bind(("", puerto))
s.listen(5)

print(f"Servidor Oche (longitud binaria >H) escuchando en el puerto {puerto}...")

while True:
    print("Esperando un cliente...")
    sd, origen = s.accept()
    if retardo:
        print("(--sleep) Esperando 1 segundo antes de leer...")
        time.sleep(1)
    print(f"Nuevo cliente conectado desde {origen[0]}:{origen[1]}")

    while True:
        mensaje = recibe_mensaje(sd)
        if mensaje is None:
            print("Conexión cerrada por el cliente")
            sd.close()
            break
        invertido = mensaje[::-1]
        envia_mensaje(sd, invertido)
        print(f"Recibido ({len(bytes(mensaje, 'utf8'))} bytes): {mensaje!r} -> enviado: {invertido!r}")
