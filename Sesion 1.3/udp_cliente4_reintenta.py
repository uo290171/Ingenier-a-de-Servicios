# coding: utf8
import sys
import socket

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Cliente UDP (con reintentos) para enviar a {host}:{puerto}")
print("Escribe tus mensajes (escribe FIN para terminar):")

contador = 1
while True:
    texto = input("> ")
    if texto == "FIN":
        break
    
    mensaje = f"{contador}: {texto}"
    enviado = False
    timeout_actual = 0.1  # Timeout inicial de 1 décima de segundo
    
    # Bucle de reintentos mientras el timeout no supere los 2 segundos
    while timeout_actual <= 2.0:
        s.sendto(mensaje.encode("utf8"), (host, puerto))
        s.settimeout(timeout_actual)
        
        try:
            respuesta, origen = s.recvfrom(1024)
            if respuesta.decode("utf8") == "OK":
                print(f"Confirmación OK recibida para el mensaje {contador}")
                enviado = True
                break
        except socket.timeout:
            print(f"Timeout agotar ({timeout_actual}s). Reenviando mensaje...")
            timeout_actual *= 2  # Duplicamos el timeout para el siguiente intento
            
    if not enviado:
        print("ERROR: Puede que el servidor esté caído. Inténtelo más tarde")
        break
    
    contador += 1

s.close()