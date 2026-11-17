# Arranca por telnet udp_servidor3_con_ok.py si no está ya en ejecución
import telnetlib
import time

HOST = "localhost"
USUARIO = "uo290171"
CLAVE = "123456"     # Clave en el código (mala práctica, lo pide el guion)
SERVIDOR = b"udp_servidor3_con_ok.py"

tn = telnetlib.Telnet(HOST)

# 1. Login con usuario y clave incrustados
tn.read_until(b"login: ")
tn.write(USUARIO.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(CLAVE.encode('utf-8') + b"\n")

# 2. Esperar al prompt
tn.read_until(b"$ ")

# 3. Pedir la lista de procesos (ps -ef como el guion; ww para no cortar las líneas a 80 columnas)
tn.write(b"ps -efww\n")

# 4. Esperar al siguiente prompt y guardar la respuesta
respuesta = tn.read_until(b"$ ")

# 5. ¿Está ya en ejecución?
if SERVIDOR in respuesta:
    print("El servidor ya está en ejecución")
else:
    # 6. Lanzarlo con nohup y en segundo plano
    tn.write(b"nohup python3 " + SERVIDOR + b" &\n")
    # 7. Dar tiempo a que arranque
    time.sleep(1)
    print("Servidor lanzado")

# 8. Cerrar la sesión
tn.write(b"exit\n")

# 9. Mostrar lo recibido (depuración)
print(tn.read_all().decode('utf-8'))
