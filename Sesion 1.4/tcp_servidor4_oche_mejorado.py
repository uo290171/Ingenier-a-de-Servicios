# coding: utf8
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


def recibe_mensaje(sd):
    """Lee del socket byte a byte hasta encontrar el terminador \\r\\n.

    Retorna la línea completa (bytes) incluyendo el \\r\\n final, o b"" si el
    otro extremo cerró la conexión sin enviar nada más.
    Los bytes se acumulan en una lista y se unen al final con b"".join(),
    que es mucho más eficiente que ir concatenando con +.
    """
    buffer = []
    while True:
        byte = sd.recv(1)          # recv(1) devuelve un objeto bytes, p.ej. b"\r"
        if not byte:               # Conexión cerrada
            break
        buffer.append(byte)
        # Comparamos bytes con bytes: los dos últimos deben ser b"\r\n"
        if b"".join(buffer[-2:]) == b"\r\n":
            break
    return b"".join(buffer)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor Oche mejorado (recibe_mensaje) escuchando en el puerto {puerto}...")

while True:
    print("Esperando un cliente...")
    sd, origen = s.accept()
    if retardo:
        print("(--sleep) Esperando 1 segundo antes de leer...")
        time.sleep(1)
    print(f"Nuevo cliente conectado desde {origen[0]}:{origen[1]}")

    continuar = True
    while continuar:
        mensaje_bytes = recibe_mensaje(sd)

        if mensaje_bytes == b"":
            print("Conexión cerrada por el cliente")
            sd.close()
            continuar = False
            break

        mensaje_str = str(mensaje_bytes, "utf8")

        # Quitar el fin de línea final (\r\n)
        linea = mensaje_str[:-2]
        linea_invertida = linea[::-1]

        # Enviar de vuelta con \r\n
        respuesta = linea_invertida + "\r\n"
        sd.sendall(bytes(respuesta, "utf8"))
        print(f"Enviado eco invertido: {linea_invertida}")
