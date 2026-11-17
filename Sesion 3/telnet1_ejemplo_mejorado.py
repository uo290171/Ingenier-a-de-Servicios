# Igual que telnet1_ejemplo.py pero descartando el mensaje de bienvenida:
# se lee hasta el primer prompt ($) y solo se muestra el comando y su salida
import getpass
import telnetlib

HOST = "localhost"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

# Leer y descartar todo hasta el prompt (termina en "$ ")
tn.read_until(b"$ ")

tn.write(b"ls /home\n")
# Leer hasta el siguiente prompt: eco del comando + su salida
salida = tn.read_until(b"$ ")
tn.write(b"exit\n")
tn.read_all()

# Quitar el prompt final (última línea)
texto = salida.decode('utf-8')
print(texto.rsplit("\n", 1)[0])
