# Envía un correo hablando SMTP directamente por un socket
import socket
import sys


def RecvReply(s, codigo):
    respuesta = s.recv(1024)
    print(respuesta.decode("utf-8", errors="replace"), end="")
    if respuesta[:3] != codigo:
        print("ERROR: se esperaba", codigo.decode(), "y se recibió", respuesta[:3].decode())
        sys.exit(1)


server = "relay.uniovi.es"
port = 25
fromaddr = "uo290171@uniovi.es"
toaddr = "uo290171@uniovi.es"
subject = "Prueba SMTP en crudo"
data = "Hola, este correo se ha enviado desde un socket en python."

message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
RecvReply(s, b"220")

s.send(b"HELO " + socket.gethostname().encode("ascii") + b"\r\n")
RecvReply(s, b"250")

s.send(("MAIL FROM:<%s>\r\n" % fromaddr).encode("ascii"))
RecvReply(s, b"250")

s.send(("RCPT TO:<%s>\r\n" % toaddr).encode("ascii"))
RecvReply(s, b"250")

s.send(b"DATA\r\n")
RecvReply(s, b"354")

s.send(message.encode("utf-8"))
RecvReply(s, b"250")

s.send(b"QUIT\r\n")
RecvReply(s, b"221")
s.close()
