# coding: utf8
import sys
import socket

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor Oche simplista escuchando en el puerto {puerto}...")

while True:
    print("Esperando un cliente...")
    sd, origen = s.accept()
    print(f"Nuevo cliente conectado desde {origen[0]}:{origen[1]}")
    
    continuar = True
    while continuar:
        # Primera aproximación: recibimos hasta 80 bytes asumiendo que llega la línea completa
        mensaje = sd.recv(80)
        
        if mensaje == b"":
            print("Conexión cerrada por el cliente")
            sd.close()
            continuar = False
            break
            
        mensaje_str = str(mensaje, "utf8")
        
        # Quitar el fin de línea (los últimos 2 caracteres: \r\n)
        linea = mensaje_str[:-2]
        
        # Darle la vuelta al string
        linea_invertida = linea[::-1]
        
        # Enviar de vuelta con \r\n añadido
        respuesta = linea_invertida + "\r\n"
        sd.sendall(bytes(respuesta, "utf8"))
        print(f"Enviado eco invertido: {linea_invertida}")
        