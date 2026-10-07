# persistencia/empleado_dao.py
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql

# columnas de la tabla, en el mismo orden que usa _fila_a_empleado()
_COLUMNAS = "id_empleado, nombre, correo, salario"


class EmpleadoDAO:
    # CREATE
    @staticmethod
    def insertar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marcador = marcador_sql()

            # el id no se envía: lo genera la base de datos
            sql = f"""
                INSERT INTO empleado (nombre, correo, salario)
                VALUES ({marcador}, {marcador}, {marcador})
            """

            cursor.execute(sql, (empleado.nombre, empleado.correo, empleado.salario))
            conexion.commit()
            empleado.id_empleado = cursor.lastrowid
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    # mapeo fila -> objeto
    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id_empleado=fila[0],
            nombre=fila[1],
            correo=fila[2],
            salario=float(fila[3])  # MySQL entrega DECIMAL, se pasa a float
        )

    # READ
    @staticmethod
    def _buscar_uno(columna, valor):
        # columna es una constante interna (nunca viene del usuario);
        # el valor siempre va parametrizado para evitar inyección SQL
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            sql = f"SELECT {_COLUMNAS} FROM empleado WHERE {columna} = {marcador_sql()}"
            cursor.execute(sql, (valor,))
            fila = cursor.fetchone()
        finally:
            if conexion:
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
    def buscar_por_correo(correo):
        return EmpleadoDAO._buscar_uno("correo", correo)

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            cursor.execute(f"SELECT {_COLUMNAS} FROM empleado")
            filas = cursor.fetchall()
        finally:
            if conexion:
                conexion.close()

        return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]

    # UPDATE
    @staticmethod
    def actualizar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = (
                "UPDATE empleado "
                f"SET nombre = {marca}, correo = {marca}, salario = {marca} "
                f"WHERE id_empleado = {marca}"
            )

            cursor.execute(
                sql,
                (empleado.nombre, empleado.correo, empleado.salario, empleado.id_empleado)
            )
            conexion.commit()
            # True si se modificó una fila, False si el id no existe
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    # DELETE
    @staticmethod
    def eliminar(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            sql = f"DELETE FROM empleado WHERE id_empleado = {marcador_sql()}"
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            # True si se eliminó una fila, False si el id no existe
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()