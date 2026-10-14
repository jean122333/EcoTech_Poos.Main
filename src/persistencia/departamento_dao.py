# persistencia/departamento_dao.py
from dominio.departamento import Departamento
from persistencia.base_dao import ejecutar_escritura, consultar
from persistencia.conexion import marcador_sql

_COLUMNAS = "id_departamento, nombre, gerente"


class DepartamentoDAO:
    # CREATE
    @staticmethod
    def insertar(departamento):
        m = marcador_sql()
        sql = f"INSERT INTO departamento (nombre, gerente) VALUES ({m}, {m})"
        _, nuevo_id = ejecutar_escritura(sql, (departamento.nombre, departamento.gerente))
        departamento.id_departamento = nuevo_id
        return departamento

    # mapeo fila -> objeto
    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(id_departamento=fila[0], nombre=fila[1], gerente=fila[2])

    # READ
    @staticmethod
    def _buscar_uno(columna, valor):
        # columna es una constante interna; el valor va siempre parametrizado
        sql = f"SELECT {_COLUMNAS} FROM departamento WHERE {columna} = {marcador_sql()}"
        fila = consultar(sql, (valor,), uno=True)
        return None if fila is None else DepartamentoDAO._fila_a_departamento(fila)

    @staticmethod
    def buscar_por_id(id_departamento):
        return DepartamentoDAO._buscar_uno("id_departamento", id_departamento)

    @staticmethod
    def buscar_por_nombre(nombre):
        return DepartamentoDAO._buscar_uno("nombre", nombre)

    @staticmethod
    def listar():
        filas = consultar(f"SELECT {_COLUMNAS} FROM departamento ORDER BY id_departamento")
        return [DepartamentoDAO._fila_a_departamento(fila) for fila in filas]

    # UPDATE
    @staticmethod
    def actualizar(departamento):
        m = marcador_sql()
        sql = (f"UPDATE departamento SET nombre = {m}, gerente = {m} "
               f"WHERE id_departamento = {m}")
        filas, _ = ejecutar_escritura(
            sql, (departamento.nombre, departamento.gerente, departamento.id_departamento)
        )
        return filas > 0

    # DELETE (los empleados del departamento quedan sin departamento: ON DELETE SET NULL)
    @staticmethod
    def eliminar(id_departamento):
        filas, _ = ejecutar_escritura(
            f"DELETE FROM departamento WHERE id_departamento = {marcador_sql()}",
            (id_departamento,),
        )
        return filas > 0