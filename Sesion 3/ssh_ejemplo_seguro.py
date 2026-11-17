import base64
import getpass
import paramiko
import time
client = paramiko.SSHClient()
# Política por defecto (RejectPolicy): solo se aceptan claves conocidas.
# Registramos la clave pública ed25519 del servidor
# (sacada de /etc/ssh/ssh_host_ed25519_key.pub)
key = paramiko.Ed25519Key(data=base64.b64decode(
    b'AAAAC3NzaC1lZDI1NTE5AAAAIFr/dgSG3f7mi540h4N/YnbGY2cGHqwsg81F/FUsTEq6'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)
clave = getpass.getpass("Clave de uo290171: ")
client.connect('localhost', username='uo290171', password=clave)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
