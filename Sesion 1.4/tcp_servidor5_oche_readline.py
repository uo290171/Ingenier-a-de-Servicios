# coding: utf8
import sys
import socket

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor Oche con readline() escuchando en el puerto {puerto}...")

while True:
    print("Esperando un cliente...")
    sd, origen = s.accept()
    print(f"Nuevo cliente conectado desde {origen[0]}:{origen[1]}")
    
    # Convertimos el socket en un objeto de tipo fichero para usar readline()
    f = sd.makefile(encoding="utf8", newline="\r\n")
    
    continuar = True
    while continuar:
        # readline lee automáticamente hasta encontrar \r\n y decodifica a str
        mensaje_str = f.readline()
        
        if mensaje_str == "":
            print("Conexión cerrada por el cliente")
            f.close()
            sd.close()
            continuar = False
            break
            
        # Quitar el fin de línea y dar la vuelta
        linea = mensaje_str[:-2]
        linea_invertida = linea[::-1]
        
        respuesta = linea_invertida + "\r\n"
        sd.sendall(bytes(respuesta, "utf8"))
        print(f"Enviado eco invertido: {linea_invertida}")
        