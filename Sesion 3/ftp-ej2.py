# Como ftp-ej1.py pero con MLSD, mostrando solo los nombres
# y omitiendo las pseudo-carpetas . y ..
import ftplib, getpass

lista = []

def acumular(linea):
    lista.append(linea)

clave = getpass.getpass("Clave? ")

f = ftplib.FTP("localhost")
f.login("uo290171", clave)
f.cwd("carpeta")

resp = f.retrlines("MLSD", acumular)
print("Respuesta del protocolo: ", resp)
print("Ficheros de la carpeta remota:")
for l in lista:
    # Formato: "hecho1=v1;hecho2=v2; nombre"
    if "type=cdir" in l or "type=pdir" in l:
        continue
    hechos, nombre = l.split(" ", 1)
    print(nombre)
f.quit()
