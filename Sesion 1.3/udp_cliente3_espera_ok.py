# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Cliente UDP (esperando OK) para enviar a {host}:{puerto}")
print("Escribe tus mensajes (escribe FIN para terminar):")

contador = 1
while True:
    texto = input("> ")
    if texto == "FIN":
        break
    
    mensaje = f"{contador}: {texto}"
    s.sendto(mensaje.encode("utf8"), (host, puerto))
    
    # Configuramos un timeout de 0.1 segundos para recibir el OK
    s.settimeout(0.1)
    try:
        respuesta, origen = s.recvfrom(1024)
        if respuesta.decode("utf8") == "OK":
            print("Recibida confirmación OK del servidor")
        else:
            print("Recibido datagrama no esperado")
    except socket.timeout:
        print("ERROR: El datagrama de confirmación no llega (paquete perdido o timeout)")
    
    contador += 1

s.close()
