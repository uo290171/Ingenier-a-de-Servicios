# Descarga carpeta/prueba.txt como prueba-copia.txt
import ftplib, getpass

clave = getpass.getpass("Clave? ")

f = ftplib.FTP("localhost")
f.login("uo290171", clave)
f.cwd("carpeta")

f_local = open("prueba-copia.txt", "wb")      # Creamos el fichero local
                                              # importante abrirlo en modo binario "b"
result = f.retrbinary("RETR prueba.txt",      # Enviar petición de fichero
                      f_local.write)          # Función a ejecutar por cada bloque recibido
f_local.close()
print(result)
f.quit()
