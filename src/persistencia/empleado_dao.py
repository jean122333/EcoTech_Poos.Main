# persistencia/empleado_dao.py
from dominio.empleado import Empleado
from persistencia.base_dao import ejecutar_escritura, consultar
from persistencia.conexion import marcador_sql

# columnas de la tabla, en el mismo orden que usa _fila_a_empleado()
_COLUMNAS = "id_empleado, nombre, correo, salario, departamento_id"


class EmpleadoDAO:
    # CREATE
    @staticmethod
    def insertar(empleado):
        m = marcador_sql()
        # el id no se envía: lo genera la base de datos
        sql = (
            "INSERT INTO empleado (nombre, correo, salario, departamento_id) "
            f"VALUES ({m}, {m}, {m}, {m})"
        )
        _, nuevo_id = ejecutar_escritura(
            sql,
            (empleado.nombre, empleado.correo, empleado.salario, empleado.departamento_id),
        )
        empleado.id_empleado = nuevo_id
        return empleado

    # mapeo fila -> objeto
    @staticmethod
    def _fila_a_empleado(fila):
        empleado = Empleado(
            id_empleado=fila[0],
            nombre=fila[1],
            correo=fila[2],
            salario=float(fila[3]),  # MariaDB entrega DECIMAL, se pasa a float
        )
        empleado.departamento_id = fila[4]
        return empleado

    # READ
    @staticmethod
    def _buscar_uno(columna, valor):
        # columna es una constante interna (nunca viene del usuario);
        # el valor siempre va parametrizado para evitar inyección SQL
        sql = f"SELECT {_COLUMNAS} FROM empleado WHERE {columna} = {marcador_sql()}"
        fila = consultar(sql, (valor,), uno=True)
        return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)

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
        filas = consultar(f"SELECT {_COLUMNAS} FROM empleado ORDER BY id_empleado")
        return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]

    @staticmethod
    def listar_por_departamento(id_departamento):
        sql = (f"SELECT {_COLUMNAS} FROM empleado WHERE departamento_id = {marcador_sql()} "
               "ORDER BY id_empleado")
        filas = consultar(sql, (id_departamento,))
        return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]

    @staticmethod
    def listar_por_proyecto(id_proyecto):
        """Empleados asignados a un proyecto (JOIN con la tabla intermedia)."""
        columnas = ", ".join(f"e.{c.strip()}" for c in _COLUMNAS.split(","))
        sql = (
            f"SELECT {columnas} FROM empleado e "
            "JOIN empleado_proyecto ep ON ep.empleado_id = e.id_empleado "
            f"WHERE ep.proyecto_id = {marcador_sql()} ORDER BY e.id_empleado"
        )
        filas = consultar(sql, (id_proyecto,))
        return [EmpleadoDAO._fila_a_empleado(fila) for fila in filas]

    # UPDATE
    @staticmethod
    def actualizar(empleado):
        m = marcador_sql()
        sql = (
            "UPDATE empleado "
            f"SET nombre = {m}, correo = {m}, salario = {m}, departamento_id = {m} "
            f"WHERE id_empleado = {m}"
        )
        filas, _ = ejecutar_escritura(
            sql,
            (empleado.nombre, empleado.correo, empleado.salario,
             empleado.departamento_id, empleado.id_empleado),
        )
        # True si se modificó una fila, False si el id no existe
        return filas > 0

    # DELETE
    @staticmethod
    def eliminar(id_empleado):
        filas, _ = ejecutar_escritura(
            f"DELETE FROM empleado WHERE id_empleado = {marcador_sql()}", (id_empleado,)
        )
        # True si se eliminó una fila, False si el id no existe
        return filas > 0