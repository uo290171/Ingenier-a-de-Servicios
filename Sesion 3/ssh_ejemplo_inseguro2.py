import getpass
import paramiko
import time
client = paramiko.SSHClient()
# Acepta cualquier clave, pero avisa con un warning (sigue siendo inseguro)
client.set_missing_host_key_policy(paramiko.WarningPolicy())
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
