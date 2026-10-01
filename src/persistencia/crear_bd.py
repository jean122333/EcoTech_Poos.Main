# persistencia/crear_bd.py
from persistencia.conexion import (abrir_conexion,obtener_motor )

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    if obtener_motor() == "sqlite":
        sql = '''
            CREATE TABLE IF NOT EXISTS empleado (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            salario REAL NOT NULL
            )
        '''
    else:
        sql = '''
            CREATE TABLE IF NOT EXISTS empleado (
            id_empleado INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            salario DECIMAL(10,2) NOT NULL
            )
        '''
    cursor.execute(sql)
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")