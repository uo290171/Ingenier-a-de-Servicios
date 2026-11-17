# Descarga por FTP todos los ficheros (no subcarpetas) de una carpeta remota
# Uso: python ftp-ej4.py [carpeta_remota]
import ftplib, getpass, sys

carpeta = sys.argv[1] if len(sys.argv) > 1 else "carpeta"
clave = getpass.getpass("Clave? ")

f = ftplib.FTP("localhost")
f.login("uo290171", clave)
f.cwd(carpeta)

lista = []
f.retrlines("MLSD", lista.append)

for l in lista:
    hechos, nombre = l.split(" ", 1)
    if "type=file" not in hechos.lower():
        continue   # saltar ., .. y subcarpetas
    with open(nombre, "wb") as f_local:
        f.retrbinary("RETR " + nombre, f_local.write)
    print("Descargado", nombre)
f.quit()
