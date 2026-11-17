import base64
import getpass
import paramiko
import time

# Datos del servidor del compañero (rellenar):
HOST = "IP_DEL_COMPANERO"
USUARIO = "alumno"
# Parte base64 de /etc/ssh/ssh_host_ed25519_key.pub del compañero
CLAVE_PUBLICA = b'PEGAR_AQUI_AAAA...'

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_PUBLICA))
client.get_host_keys().add(HOST, 'ssh-ed25519', key)
clave = getpass.getpass(f"Clave de {USUARIO}@{HOST}: ")
client.connect(HOST, username=USUARIO, password=clave)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
