# Ejemplo de la documentación de telnetlib, modificado para listar /home
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

tn.write(b"ls /home\n")
tn.write(b"exit\n")

# UTF-8 en lugar de ascii, por si hay nombres con acentos o eñes
print(tn.read_all().decode('utf-8'))
