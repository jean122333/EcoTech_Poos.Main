# persistencia/proyecto_dao.py
from dominio.proyecto import Proyecto
from persistencia.base_dao import ejecutar_escritura, consultar
from persistencia.conexion import marcador_sql

_COLUMNAS = "id_proyecto, nombre, fecha_inicio, descripcion"


class ProyectoDAO:
    # CREATE
    @staticmethod
    def insertar(proyecto):
        m = marcador_sql()
        sql = f"INSERT INTO proyecto (nombre, fecha_inicio, descripcion) VALUES ({m}, {m}, {m})"
        _, nuevo_id = ejecutar_escritura(
            sql, (proyecto.nombre, proyecto.fecha_inicio, proyecto.descripcion)
        )
        proyecto.id_proyecto = nuevo_id
        return proyecto

    # mapeo fila -> objeto
    @staticmethod
    def _fila_a_proyecto(fila):
        return Proyecto(
            id_proyecto=fila[0],
            nombre=fila[1],
            fecha_inicio=str(fila[2]),  # MariaDB entrega un objeto date
            descripcion=fila[3],
        )

    # READ
    @staticmethod
    def _buscar_uno(columna, valor):
        # columna es una constante interna; el valor va siempre parametrizado
        sql = f"SELECT {_COLUMNAS} FROM proyecto WHERE {columna} = {marcador_sql()}"
        fila = consultar(sql, (valor,), uno=True)
        return None if fila is None else ProyectoDAO._fila_a_proyecto(fila)

    @staticmethod
    def buscar_por_id(id_proyecto):
        return ProyectoDAO._buscar_uno("id_proyecto", id_proyecto)

    @staticmethod
    def buscar_por_nombre(nombre):
        return ProyectoDAO._buscar_uno("nombre", nombre)

    @staticmethod
    def listar():
        filas = consultar(f"SELECT {_COLUMNAS} FROM proyecto ORDER BY id_proyecto")
        return [ProyectoDAO._fila_a_proyecto(fila) for fila in filas]

    @staticmethod
    def listar_por_empleado(id_empleado):
        """Proyectos en los que participa un empleado (JOIN con la tabla intermedia)."""
        columnas = ", ".join(f"p.{c.strip()}" for c in _COLUMNAS.split(","))
        sql = (
            f"SELECT {columnas} FROM proyecto p "
            "JOIN empleado_proyecto ep ON ep.proyecto_id = p.id_proyecto "
            f"WHERE ep.empleado_id = {marcador_sql()} ORDER BY p.id_proyecto"
        )
        filas = consultar(sql, (id_empleado,))
        return [ProyectoDAO._fila_a_proyecto(fila) for fila in filas]

    # UPDATE
    @staticmethod
    def actualizar(proyecto):
        m = marcador_sql()
        sql = (f"UPDATE proyecto SET nombre = {m}, fecha_inicio = {m}, descripcion = {m} "
               f"WHERE id_proyecto = {m}")
        filas, _ = ejecutar_escritura(
            sql,
            (proyecto.nombre, proyecto.fecha_inicio, proyecto.descripcion,
             proyecto.id_proyecto),
        )
        return filas > 0

    # DELETE (borra también sus asignaciones; los registros de tiempo quedan sin proyecto)
    @staticmethod
    def eliminar(id_proyecto):
        filas, _ = ejecutar_escritura(
            f"DELETE FROM proyecto WHERE id_proyecto = {marcador_sql()}", (id_proyecto,)
        )
        return filas > 0

    # relación Empleado 0..* ── 0..* Proyecto (tabla empleado_proyecto)
    @staticmethod
    def asignar_empleado(id_proyecto, id_empleado):
        """Asigna un empleado al proyecto. Lanza IntegrityError si ya estaba asignado
        o si alguno de los dos ids no existe."""
        m = marcador_sql()
        sql = f"INSERT INTO empleado_proyecto (empleado_id, proyecto_id) VALUES ({m}, {m})"
        filas, _ = ejecutar_escritura(sql, (id_empleado, id_proyecto))
        return filas > 0

    @staticmethod
    def quitar_empleado(id_proyecto, id_empleado):
        """True si se quitó la asignación, False si no existía."""
        m = marcador_sql()
        sql = f"DELETE FROM empleado_proyecto WHERE empleado_id = {m} AND proyecto_id = {m}"
        filas, _ = ejecutar_escritura(sql, (id_empleado, id_proyecto))
        return filas > 0