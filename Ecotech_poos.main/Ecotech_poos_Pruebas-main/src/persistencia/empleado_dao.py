# persistencia/empleado_dao.py
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql


class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
            INSERT INTO empleado (
            nombre,
            correo
            )
            VALUES ({marcador}, {marcador})
        """

        cursor.execute(sql, (empleado.nombre, empleado.correo))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado
    

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id=fila[0],
            nombre=fila[1],
            correo=fila[2]
        )

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        marcador = marcador_sql()
        sql = f"""
            SELECT id, nombre, correo 
            FROM empleado WHERE id = {marcador}
        """

        cursor.execute(sql, (id_empleado,))
        
        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None

        #return Empleado(id=fila[0], nombre=fila[1], correo=fila[2])
        return EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id, nombre, correo FROM empleado"
        )
        filas = cursor.fetchall()
        conexion.close()

        empleados = []

        for fila in filas:
            empleados.append(EmpleadoDAO._fila_a_empleado(fila))

        return empleados

