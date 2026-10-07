# coding: utf8
import sys
import socket

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

def recibe_mensaje(sd):
    """Lee bytes del socket uno a uno de forma eficiente hasta encontrar \r\n"""
    buffer = []
    while True:
        byte = sd.recv(1)
        if not byte:
            break
        buffer.append(byte)
        # Comprobamos si los dos últimos bytes forman el terminador \r\n
        if len(buffer) >= 2 and buffer[-2] == b"\r"[0] and buffer[-1] == b"\n"[0]:
            break
    return b"".join(buffer)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor Oche mejorado (recibe_mensaje) escuchando en el puerto {puerto}...")

while True:
    print("Esperando un cliente...")
    sd, origen = s.accept()
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
        