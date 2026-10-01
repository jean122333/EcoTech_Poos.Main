# persistencia/empleado_dao.py
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql

# Columnas de la tabla, en el mismo orden que usa _fila_a_empleado()
_COLUMNAS = "id_empleado, nombre, salario"


class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
            INSERT INTO empleado (
            nombre,
            salario
            )
            VALUES ({marcador}, {marcador})
        """

        cursor.execute(sql, (empleado.nombre, empleado.salario))
        empleado.id_empleado = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id_empleado=fila[0],
            nombre=fila[1],
            salario=float(fila[2])  # MySQL entrega DECIMAL, se pasa a float
        )

    @staticmethod
    def _buscar_uno(columna, valor):
        # 'columna' es una constante interna (nunca viene del usuario);
        # el valor siempre va parametrizado para evitar inyección SQL.
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        sql = f"SELECT {_COLUMNAS} FROM empleado WHERE {columna} = {marcador_sql()}"
        cursor.execute(sql, (valor,))

        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None
        return EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def buscar_por_id(id_empleado):
        return EmpleadoDAO._buscar_uno("id_empleado", id_empleado)

    @staticmethod
    def buscar_por_nombre(nombre):
        return EmpleadoDAO._buscar_uno("nombre", nombre)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        cursor.execute(f"SELECT {_COLUMNAS} FROM empleado")
        filas = cursor.fetchall()
        conexion.close()

        return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]