# persistencia/conexion.py
import os
import re
import sqlite3
import mysql.connector  # conector oficial de MySQL
from mysql.connector.constants import ClientFlag
from dotenv import load_dotenv

load_dotenv()

# errores de integridad (correo duplicado, restricciones) de cada motor
ERRORES_INTEGRIDAD = (sqlite3.IntegrityError, mysql.connector.IntegrityError)


def obtener_motor():
    motor = os.getenv("DB_ENGINE", "sqlite").strip().lower()
    # MariaDB es compatible con el conector de MySQL
    if motor in ("mysql", "mariadb"):
        return "mysql"
    return motor


def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        return sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))

    if motor == "mysql":
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            # rowcount cuenta filas encontradas, aunque el UPDATE no cambie valores
            client_flags=[ClientFlag.FOUND_ROWS],
        )

    raise ValueError(f"Motor no soportado: {motor}")


def crear_base_datos():
    """En MySQL/MariaDB crea la base si no existe; en SQLite no hace nada."""
    if obtener_motor() != "mysql":
        return

    nombre = os.getenv("DB_NAME", "")
    # el nombre de una base no se puede parametrizar, por eso se valida
    if not re.fullmatch(r"[A-Za-z0-9_]+", nombre):
        raise ValueError("DB_NAME solo puede tener letras, números y guion bajo")

    conexion = None
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD", ""),
        )
        cursor = conexion.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{nombre}` CHARACTER SET utf8mb4")
        conexion.commit()
    finally:
        if conexion:
            conexion.close()


def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"


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
        return False
    finally:
        if conexion:
            conexion.close()