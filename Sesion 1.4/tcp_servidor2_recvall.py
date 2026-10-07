# coding: utf8
import sys
import socket

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

def recvall(sd, n):
    """Función eficiente para leer exactamente n bytes del socket"""
    buf = b""
    while len(buf) < n:
        packet = sd.recv(n - len(buf))
        if not packet:
            break
        buf += packet
    return buf.decode("ascii")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor TCP (con recvall) escuchando en el puerto {puerto}...")

while True:
    print("Esperando un cliente...")
    sd, origen = s.accept()
    print(f"Nuevo cliente conectado desde {origen[0]}:{origen[1]}")
    
    continuar = True
    while continuar:
        # Usamos recvall para leer exactamente bloques de 5 bytes
        datos = recvall(sd, 5)
        
        if datos == "":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print(f"Recibido mensaje: {datos}")
            