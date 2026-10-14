# diagnostico.py
"""Diagnóstico paso a paso de la conexión a la base de datos.

Uso (desde la raíz del proyecto):   python src/diagnostico.py

Revisa, en orden, lo que suele fallar al conectarse desde otra PC o lugar:
configuración (.env) -> nombre del servidor -> puerto/firewall -> usuario y clave ->
permisos -> base de datos -> tablas. Se detiene en el primer problema y dice qué hacer.
No muestra nunca la contraseña.
"""
import os
import socket
import sqlite3
import sys
import time

import mysql.connector

from persistencia.conexion import (
    _parametros_servidor, abrir_conexion, explicar_error, obtener_motor,
)

OK, FALLO, AVISO = "[ OK ]", "[FALLO]", "[AVISO]"


def paso(estado, texto):
    print(f"{estado} {texto}")


def pista(texto):
    print(f"        -> {texto}")


def diagnosticar_sqlite():
    nombre = os.getenv("DB_NAME", "ecotech.db")
    ruta = os.path.abspath(nombre)
    paso(OK, f"Motor: sqlite. Archivo: {ruta}")

    carpeta = os.path.dirname(ruta)
    if not os.access(carpeta, os.W_OK):
        paso(FALLO, f"No hay permiso de escritura en la carpeta {carpeta}")
        pista("Cambia DB_NAME a una ruta donde puedas escribir.")
        return False
    paso(OK, "Hay permiso de escritura en la carpeta")

    try:
        conexion = abrir_conexion()
        conexion.execute("SELECT 1")
        tablas = [f[0] for f in conexion.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        conexion.close()
    except sqlite3.Error as error:
        paso(FALLO, f"SQLite no pudo abrir el archivo: {error}")
        return False
    paso(OK, "SQLite abre el archivo correctamente")
    paso(OK if tablas else AVISO, f"Tablas: {', '.join(tablas) if tablas else 'ninguna todavía (se crean al ejecutar main.py)'}")
    return True


def diagnosticar_mysql():
    parametros = _parametros_servidor()
    host, puerto = parametros["host"], parametros["port"]
    usuario, base = parametros["user"], os.getenv("DB_NAME", "")
    paso(OK, f"Motor: mariadb/mysql. Servidor: {host}:{puerto}. Usuario: {usuario}. Base: {base}")

    # 1. configuración mínima
    faltan = [v for v in ("DB_USER", "DB_NAME") if not os.getenv(v)]
    if faltan:
        paso(FALLO, f"Faltan variables en .env: {', '.join(faltan)}")
        pista("Copia .env.example como .env y complétalo.")
        return False
    if not os.getenv("DB_PASSWORD"):
        paso(AVISO, "DB_PASSWORD está vacío (normal en XAMPP local, no en un servidor remoto)")

    # 2. nombre del servidor
    try:
        ip = socket.getaddrinfo(host, puerto, proto=socket.IPPROTO_TCP)[0][4][0]
        paso(OK, f"El nombre '{host}' se resuelve a {ip}")
    except socket.gaierror:
        paso(FALLO, f"No se puede resolver el nombre '{host}'")
        pista("Revisa DB_HOST (sin http:// ni espacios) y tu conexión a internet/VPN.")
        return False

    # 3. red: ¿llega algo al puerto?
    inicio = time.time()
    try:
        socket.create_connection((host, puerto), timeout=parametros["connection_timeout"]).close()
        paso(OK, f"El puerto {puerto} responde ({(time.time() - inicio) * 1000:.0f} ms)")
    except socket.timeout:
        paso(FALLO, f"Tiempo agotado: nadie responde en {host}:{puerto}")
        pista("Suele ser un firewall o router bloqueando el puerto, o una IP equivocada.")
        pista("En el servidor: abre el puerto 3306 en el firewall (ver docs/ACCESO_REMOTO.md).")
        pista("Si estás en una red de universidad/empresa, puede bloquear el 3306: usa VPN (Tailscale).")
        return False
    except OSError as error:
        paso(FALLO, f"Conexión rechazada o sin ruta: {error}")
        pista("El servidor está apagado (inicia MySQL en XAMPP / docker compose up -d),")
        pista("o solo escucha en localhost (bind-address). Ver docs/ACCESO_REMOTO.md.")
        return False

    # 4. usuario y clave (sin elegir base todavía)
    try:
        conexion = mysql.connector.connect(**parametros)
    except mysql.connector.Error as error:
        paso(FALLO, f"El servidor rechazó el login: {error}")
        pista(explicar_error(error) or "Revisa usuario, clave y permisos.")
        return False
    cursor = conexion.cursor()
    cursor.execute("SELECT VERSION(), CURRENT_USER()")
    version, usuario_efectivo = cursor.fetchone()
    paso(OK, f"Login correcto. Servidor {version}. Entraste como {usuario_efectivo}")

    # 5. permisos y base de datos
    cursor.execute("SHOW DATABASES")
    bases = [fila[0] for fila in cursor.fetchall()]
    if base not in bases:
        paso(AVISO, f"La base '{base}' no existe o este usuario no la ve")
        pista("main.py la crea sola si el usuario tiene permiso CREATE.")
        pista("Si no lo tiene, créala en phpMyAdmin o ejecuta sql/crear_usuario_remoto.sql como root.")
        conexion.close()
        return True
    paso(OK, f"La base '{base}' existe y es visible")

    # 6. tablas
    try:
        conexion.database = base
        cursor = conexion.cursor()
        cursor.execute("SHOW TABLES")
        tablas = [fila[0] for fila in cursor.fetchall()]
    except mysql.connector.Error as error:
        paso(FALLO, f"No se pudo usar la base '{base}': {error}")
        pista(explicar_error(error) or "Falta un GRANT sobre esa base.")
        conexion.close()
        return False
    paso(OK if tablas else AVISO, f"Tablas: {', '.join(tablas) if tablas else 'ninguna todavía (se crean al ejecutar main.py)'}")
    conexion.close()
    return True


def main():
    print("=== Diagnóstico de conexión EcoTech ===")
    motor = obtener_motor()
    if motor == "sqlite":
        correcto = diagnosticar_sqlite()
    elif motor == "mysql":
        correcto = diagnosticar_mysql()
    else:
        paso(FALLO, f"DB_ENGINE='{motor}' no es válido. Usa sqlite o mariadb.")
        correcto = False

    print()
    print("Todo en orden: ya puedes ejecutar python src/main.py" if correcto
          else "Corrige el punto marcado como [FALLO] y vuelve a ejecutar este diagnóstico.")
    sys.exit(0 if correcto else 1)


if __name__ == "__main__":
    main()