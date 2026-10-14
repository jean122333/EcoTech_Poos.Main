# persistencia/base_dao.py
"""Funciones compartidas por todos los DAO.

Aquí vive UNA sola vez el patrón de la Clase 6 (conexión, commit, rollback y cierre),
para no repetirlo en cada método de cada DAO. No contiene SQL propio de ninguna entidad.
"""
from persistencia.conexion import abrir_conexion


def ejecutar_escritura(sql, parametros=()):
    """INSERT / UPDATE / DELETE. Devuelve (filas_afectadas, ultimo_id).

    commit si todo sale bien; rollback si falla; la conexión siempre se cierra.
    La excepción se propaga: el DAO detecta el fallo y la aplicación decide el mensaje.
    """
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.rowcount, cursor.lastrowid
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()


def consultar(sql, parametros=(), uno=False):
    """SELECT. Devuelve una fila (o None) si uno=True; si no, una lista de filas."""
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchone() if uno else cursor.fetchall()
    finally:
        if conexion:
            conexion.close()