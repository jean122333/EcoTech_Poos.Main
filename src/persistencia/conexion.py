# persistencia/conexion.py
import os
import re
import sqlite3
import mysql.connector  # conector oficial de MySQL (también habla con MariaDB)
from mysql.connector.constants import ClientFlag
from dotenv import load_dotenv

load_dotenv()

# errores de integridad (correo duplicado, restricciones) de cada motor
ERRORES_INTEGRIDAD = (sqlite3.IntegrityError, mysql.connector.IntegrityError)

# errores de "no tienes permiso para crear la base": no son fatales si la base ya existe
_ERRNO_SIN_PERMISO = (1044, 1142, 1227)

# pistas para el usuario según el código de error de MariaDB/MySQL
_AYUDAS = {
    1045: "Usuario o contraseña incorrectos (revisa DB_USER y DB_PASSWORD en .env).",
    1130: "El servidor no permite conectarse desde este equipo. En el servidor hay que "
          "crear el usuario con '%' (o con la IP de este equipo). Ver docs/ACCESO_REMOTO.md.",
    1044: "El usuario no tiene permiso sobre esa base de datos (falta un GRANT).",
    1049: "La base de datos indicada en DB_NAME no existe en el servidor.",
    2003: "No se pudo llegar al servidor: está apagado, DB_HOST/DB_PORT están mal, "
          "o un firewall/router bloquea el puerto 3306.",
    2005: "El nombre del servidor (DB_HOST) no se pudo resolver. Revisa que esté bien escrito.",
    2006: "El servidor cerró la conexión (suele ser inactividad o reinicio del servidor).",
    2013: "Se perdió la conexión con el servidor durante la consulta.",
}


def obtener_motor():
    motor = os.getenv("DB_ENGINE", "sqlite").strip().lower()
    # MariaDB es compatible con el conector de MySQL
    if motor in ("mysql", "mariadb"):
        return "mysql"
    return motor


def _parametros_servidor():
    """Parámetros de red comunes (todos salen de .env, nunca del código)."""
    return {
        "host": os.getenv("DB_HOST", "localhost").strip(),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD", ""),
        # sin timeout, un servidor remoto caído deja el programa "colgado"
        "connection_timeout": int(os.getenv("DB_TIMEOUT", "10")),
    }


def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        conexion = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
        # SQLite no revisa las claves foráneas si no se le pide en cada conexión
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    if motor == "mysql":
        return mysql.connector.connect(
            **_parametros_servidor(),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            # rowcount cuenta filas encontradas, aunque el UPDATE no cambie valores
            client_flags=[ClientFlag.FOUND_ROWS],
        )

    raise ValueError(f"Motor no soportado: {motor}")


def crear_base_datos():
    """En MySQL/MariaDB crea la base si no existe; en SQLite no hace nada.

    Si el usuario no tiene permiso para crear bases (pasa en servidores remotos),
    se ignora el error: si la base ya existe, la conexión posterior funcionará igual.
    """
    if obtener_motor() != "mysql":
        return

    nombre = os.getenv("DB_NAME", "")
    # el nombre de una base no se puede parametrizar, por eso se valida
    if not re.fullmatch(r"[A-Za-z0-9_]+", nombre):
        raise ValueError("DB_NAME solo puede tener letras, números y guion bajo")

    conexion = None
    try:
        conexion = mysql.connector.connect(**_parametros_servidor())
        cursor = conexion.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{nombre}` CHARACTER SET utf8mb4")
        conexion.commit()
    except mysql.connector.Error as error:
        if error.errno not in _ERRNO_SIN_PERMISO:
            raise
    finally:
        if conexion:
            conexion.close()


def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"


def explicar_error(error) -> str:
    """Traduce un error de conexión a una pista entendible."""
    errno = getattr(error, "errno", None)
    return _AYUDAS.get(errno, "")


def probar_conexion() -> bool:
    """Prueba de conexión: abre la conexión, ejecuta SELECT 1 y la cierra."""
    conexion = None
    try:
        crear_base_datos()
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        print(f"Conexión exitosa ({obtener_motor()}).")
        return True
    except (sqlite3.Error, mysql.connector.Error, ValueError) as error:
        print(f"No se pudo conectar: {error}")
        ayuda = explicar_error(error)
        if ayuda:
            print("Pista:", ayuda)
        print("Para un diagnóstico paso a paso ejecuta: python src/diagnostico.py")
        return False
    finally:
        if conexion:
            conexion.close()