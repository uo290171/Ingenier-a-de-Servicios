# Muestra un resumen de cada correo de gmail usando poplib y la biblioteca email
import email
import email.header
import getpass
import poplib


def imprime_resumen_mensaje(msg_bytes):
    # Parsear los bytes recibidos y construir con ellos un
    # objeto EmailMessage
    msg = email.message_from_bytes(msg_bytes)
    # Extraemos las cabeceras "From" y "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")

    # Si estas cabeceras contienen unicode hay que decodificarlas
    # lo que es un poco enrevesado
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))

    # Extraemos el cuerpo (este ya vendrá correctamente decodificado)
    cuerpo = msg.get_payload()

    # Pero si es multi-part, lo anterior nos retorna una lista
    # En ese caso nos quedamos con el primer elemento, que será a su
    # vez un mensaje con su propio payload
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + str(parte_1)

    # Finalmente imprimimos un resumen, que son las cabeceras
    # extraidas y los primeros 500 caracteres del mensaje
    print("From:", remite)
    print("Subject:", asunto)
    print(cuerpo[:500])
    if len(cuerpo) > 500:
        print("...[omitido]")
    print("-" * 80)


server = "pop.gmail.com"

username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

pop3_mail = poplib.POP3_SSL(server)
pop3_mail.user(username)
pop3_mail.pass_(password)

num_msgs, tam = pop3_mail.stat()
print("Hay", num_msgs, "mensajes")

for n in range(1, num_msgs + 1):
    respuesta, lineas, octetos = pop3_mail.retr(n)
    # poplib devuelve una lista de líneas sin \r\n: las unimos
    imprime_resumen_mensaje(b"\r\n".join(lineas))

pop3_mail.quit()
