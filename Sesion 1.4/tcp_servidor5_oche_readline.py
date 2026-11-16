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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", puerto))
s.listen(5)

print(f"Servidor Oche con readline() escuchando en el puerto {puerto}...")

while True:
    print("Esperando un cliente...")
    sd, origen = s.accept()
    if retardo:
        print("(--sleep) Esperando 1 segundo antes de leer...")
        time.sleep(1)
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
        