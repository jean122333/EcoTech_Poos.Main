# persistencia/conexion.py
import os
import sqlite3
import mysql.connector  # conector oficial de MySQL
from dotenv import load_dotenv

load_dotenv()

def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()

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
        )

    raise ValueError(f"Motor no soportado: {motor}")


def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"


def probar_conexion() -> bool:
    """Prueba de conexión: abre la conexión, ejecuta SELECT 1 y la cierra."""
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conexion.close()
        print(f"Conexión exitosa ({obtener_motor()}).")
        return True
    except (sqlite3.Error, mysql.connector.Error, ValueError) as error:
        print(f"No se pudo conectar: {error}")
        return False