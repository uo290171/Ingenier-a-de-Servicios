# Sesión 1.4 – Programación de red con Python (TCP)

Todos los servidores reciben el puerto como primer argumento (por defecto `9999`).
Todos los clientes reciben `host puerto` (por defecto `localhost 9999`).

| Ejercicio | Servidor | Cliente | Técnica de *framing* |
|---|---|---|---|
| 1 | `tcp_servidor1_simple.py` | `tcp_cliente1_simple.py` | Bloques de 5 bytes con `recv(5)` / `send()` |
| 2 | `tcp_servidor2_recvall.py` | `tcp_cliente2_sendall.py` | Bloques de 5 bytes con `recvall()` / `sendall()` |
| 3 | `tcp_servidor3_oche_simplista.py` | `tcp_cliente3_oche.py` | Líneas `\r\n`, suponiendo un `recv()` = una línea |
| 3 (exp.) | `tcp_servidor3_oche_simplista.py` | `tcp_cliente3_oche_envia_seguido.py` | Envía 3 líneas seguidas y luego lee 3 respuestas |
| 4 | `tcp_servidor4_oche_mejorado.py` | `tcp_cliente4_oche_mejorado.py` | `recibe_mensaje()` leyendo byte a byte hasta `\r\n` |
| 5 | `tcp_servidor5_oche_readline.py` | `tcp_cliente5_oche_readline.py` | `makefile()` + `readline()` |
| 6 | `tcp_servidor6_oche_len.py` | `tcp_cliente6_oche_len.py` | Longitud en ASCII terminada en `\n` + `recvall()` |
| 7 (opcional) | `tcp_servidor7_opcional.py` | `tcp_cliente7_opcional.py` | Longitud binaria de 2 bytes big endian (`struct.pack(">H")`) |

> En el guion el cliente del ejercicio 6 aparece como `tcp_cliente.6_oche_len.py`;
> se ha llamado `tcp_cliente6_oche_len.py` por coherencia con el resto.

Ejemplo de prueba en local:

```bash
python3 tcp_servidor6_oche_len.py 9999 &
python3 tcp_cliente6_oche_len.py localhost 9999
```

## Despliegue con Docker

**Puerto del anfitrión: 9091** (el guion propone 9090, pero en nuestra máquina
el 9090 lo usa Prometheus, instalado en la sesión 2.3, y `docker run -p 9090:...`
falla con `address already in use`).

Los comandos se lanzan desde esta carpeta. Como su nombre (`Sesion 1.4`) contiene
un espacio, `$(pwd)` debe ir entre comillas en la opción `-v`.

```bash
# Crear la red (solo la primera vez)
docker network create pruebas

# 1) Servidor en la red "pruebas", sin exponer puertos
docker run -d --rm --network pruebas --name servidor_oche -v "$(pwd)":/app \
  python:3.7 python /app/tcp_servidor5_oche_readline.py

# Cliente en otro contenedor de la misma red, usando el nombre del servidor
docker run --rm --network pruebas -v "$(pwd)":/app \
  python:3.7 python /app/tcp_cliente5_oche_readline.py servidor_oche 9999

# Parar el servidor (con --rm se borra solo) y comprobar que ya no aparece
docker stop servidor_oche
docker ps -a

# 2) Servidor accesible desde fuera: puerto 9091 del anfitrión -> 9999 del contenedor
docker run -d --rm -p 9091:9999 --network pruebas \
  --name servidor_oche -v "$(pwd)":/app \
  python:3.7 python /app/tcp_servidor5_oche_readline.py

docker ps        # PORTS: 0.0.0.0:9091->9999/tcp

# Cliente desde el anfitrión
python3 tcp_cliente5_oche_readline.py localhost 9091

# Cliente desde otro PC (p. ej. un compañero): IP de la máquina Ubuntu y puerto 9091
python3 tcp_cliente5_oche_readline.py <IP_UBUNTU> 9091

docker stop servidor_oche
```
