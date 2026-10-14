# persistencia/registro_tiempo_dao.py
from dominio.registroTiempo import RegistroTiempo
from persistencia.base_dao import ejecutar_escritura, consultar
from persistencia.conexion import marcador_sql

_COLUMNAS = "id_registro, fecha, horas_trabajadas, descripcion, empleado_id, proyecto_id"


class RegistroTiempoDAO:
    # CREATE
    @staticmethod
    def insertar(registro):
        """Persiste el registro. Requiere registro.empleado_id (la clave foránea)."""
        m = marcador_sql()
        sql = (
            "INSERT INTO registro_tiempo "
            "(fecha, horas_trabajadas, descripcion, empleado_id, proyecto_id) "
            f"VALUES ({m}, {m}, {m}, {m}, {m})"
        )
        _, nuevo_id = ejecutar_escritura(
            sql,
            (registro.fecha, registro.horas_trabajadas, registro.descripcion,
             registro.empleado_id, registro.proyecto_id),
        )
        registro.id_registro = nuevo_id
        return registro

    # mapeo fila -> objeto
    @staticmethod
    def _fila_a_registro(fila):
        return RegistroTiempo(
            id_registro=fila[0],
            fecha=str(fila[1]),  # MariaDB entrega un objeto date
            horas_trabajadas=float(fila[2]),  # y un DECIMAL
            descripcion=fila[3],
            empleado_id=fila[4],
            proyecto_id=fila[5],
        )

    # READ
    @staticmethod
    def buscar_por_id(id_registro):
        sql = f"SELECT {_COLUMNAS} FROM registro_tiempo WHERE id_registro = {marcador_sql()}"
        fila = consultar(sql, (id_registro,), uno=True)
        return None if fila is None else RegistroTiempoDAO._fila_a_registro(fila)

    @staticmethod
    def listar():
        filas = consultar(f"SELECT {_COLUMNAS} FROM registro_tiempo ORDER BY fecha, id_registro")
        return [RegistroTiempoDAO._fila_a_registro(fila) for fila in filas]

    @staticmethod
    def _listar_por(columna, valor):
        # columna es una constante interna; el valor va siempre parametrizado
        sql = (f"SELECT {_COLUMNAS} FROM registro_tiempo WHERE {columna} = {marcador_sql()} "
               "ORDER BY fecha, id_registro")
        return [RegistroTiempoDAO._fila_a_registro(f) for f in consultar(sql, (valor,))]

    @staticmethod
    def listar_por_empleado(id_empleado):
        return RegistroTiempoDAO._listar_por("empleado_id", id_empleado)

    @staticmethod
    def listar_por_proyecto(id_proyecto):
        return RegistroTiempoDAO._listar_por("proyecto_id", id_proyecto)

    @staticmethod
    def total_horas_empleado(id_empleado):
        """Suma de horas de un empleado calculada por la base de datos."""
        sql = ("SELECT COALESCE(SUM(horas_trabajadas), 0) FROM registro_tiempo "
               f"WHERE empleado_id = {marcador_sql()}")
        return float(consultar(sql, (id_empleado,), uno=True)[0])

    # UPDATE
    @staticmethod
    def actualizar(registro):
        m = marcador_sql()
        sql = (
            "UPDATE registro_tiempo "
            f"SET fecha = {m}, horas_trabajadas = {m}, descripcion = {m}, proyecto_id = {m} "
            f"WHERE id_registro = {m}"
        )
        filas, _ = ejecutar_escritura(
            sql,
            (registro.fecha, registro.horas_trabajadas, registro.descripcion,
             registro.proyecto_id, registro.id_registro),
        )
        return filas > 0

    # DELETE
    @staticmethod
    def eliminar(id_registro):
        filas, _ = ejecutar_escritura(
            f"DELETE FROM registro_tiempo WHERE id_registro = {marcador_sql()}", (id_registro,)
        )
        return filas > 0