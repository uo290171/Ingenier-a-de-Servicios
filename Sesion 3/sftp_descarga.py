# Descarga por sftp todos los ficheros regulares de una carpeta remota
# Uso: python sftp_descarga.py carpeta_remota [carpeta_local]
import base64
import getpass
import os
import sys
from stat import S_ISDIR
import paramiko

HOST = "localhost"
USUARIO = "uo290171"

if len(sys.argv) < 2:
    print("Uso: python sftp_descarga.py carpeta_remota [carpeta_local]")
    sys.exit(1)
remota = sys.argv[1]
local = sys.argv[2] if len(sys.argv) > 2 else "descargas"
os.makedirs(local, exist_ok=True)

c = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(
    b'AAAAC3NzaC1lZDI1NTE5AAAAIFr/dgSG3f7mi540h4N/YnbGY2cGHqwsg81F/FUsTEq6'))
c.get_host_keys().add(HOST, 'ssh-ed25519', key)
clave = getpass.getpass(f"Clave de {USUARIO}: ")
c.connect(HOST, username=USUARIO, password=clave)

sftp = c.open_sftp()
sftp.chdir(remota)
for nombre in sftp.listdir():
    if S_ISDIR(sftp.stat(nombre).st_mode):
        print(f"Saltando carpeta {nombre}")
        continue
    sftp.get(nombre, os.path.join(local, nombre))
    print(f"Descargado {nombre}")

sftp.close()
c.close()
