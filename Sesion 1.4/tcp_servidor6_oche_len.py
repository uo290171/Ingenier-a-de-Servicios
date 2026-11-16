# coding: utf8
# Servicio "oche" con framing por longitud en ASCII:
# cada mensaje (en ambos sentidos) va precedido de su longitud en bytes,
# escrita en ASCII y terminada en "\n". Ejemplo: b"4\nHOLA"
import sys
import socket
import time

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
        return None  # Conexión cerrada a mitad de mensaje
    return datos.decode("utf8")


def envia_mensaje(sd, mensaje):
    datos = bytes(mensaje, "utf8")
    longitud = "%d\n" % len(datos)  # Longitud en bytes, no en caracteres
    sd.sendall(bytes(longitud, "ascii") + datos)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor Oche (longitud en ASCII) escuchando en el puerto {puerto}...")

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
