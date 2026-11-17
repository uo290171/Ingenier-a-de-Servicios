# Lista por sftp la carpeta del usuario en el servidor remoto
import base64
import getpass
import paramiko

HOST = "localhost"
USUARIO = "uo290171"

c = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(
    b'AAAAC3NzaC1lZDI1NTE5AAAAIFr/dgSG3f7mi540h4N/YnbGY2cGHqwsg81F/FUsTEq6'))
c.get_host_keys().add(HOST, 'ssh-ed25519', key)
clave = getpass.getpass(f"Clave de {USUARIO}: ")
c.connect(HOST, username=USUARIO, password=clave)

sftp = c.open_sftp()
# Sin chdir(): por defecto estamos en la carpeta del usuario
for nombre in sorted(sftp.listdir()):
    print(nombre)

sftp.close()
c.close()
