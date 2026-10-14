# menus/menu_registro_tiempo.py
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from menus.entradas import (
    manejar_errores, ejecutar_menu, solicitar_entero, solicitar_decimal,
    solicitar_fecha, solicitar_texto,
)


def _mostrar(registros):
    if not registros:
        print("No hay registros.")
    for registro in registros:
        print(" ", registro.mostrar_registro(), "|", registro.descripcion or "(sin descripción)")


def _pedir_proyecto_id():
    """Proyecto opcional: si se indica, debe existir."""
    id_proyecto = solicitar_entero("ID del proyecto (vacío = ninguno)", opcional=True)
    if id_proyecto is not None and ProyectoDAO.buscar_por_id(id_proyecto) is None:
        raise ValueError(f"No existe un proyecto con ID {id_proyecto}")
    return id_proyecto


@manejar_errores("registrar horas")
def registrar_horas():
    id_empleado = solicitar_entero("ID del empleado")
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        print("Empleado no encontrado.")
        return

    fecha = solicitar_fecha("Fecha")
    horas = solicitar_decimal("Horas trabajadas (0-24)", minimo=0.01, maximo=24)
    descripcion = solicitar_texto("Descripción del trabajo", obligatorio=False)

    registro = RegistroTiempo(fecha, horas, descripcion, empleado_id=id_empleado,
                              proyecto_id=_pedir_proyecto_id())
    RegistroTiempoDAO.insertar(registro)
    print("Horas registradas correctamente:", registro.mostrar_registro())


@manejar_errores("listar registros de tiempo")
def listar_registros():
    _mostrar(RegistroTiempoDAO.listar())


@manejar_errores("listar registros de un empleado")
def listar_por_empleado():
    id_empleado = solicitar_entero("ID del empleado")
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        print("Empleado no encontrado.")
        return

    _mostrar(RegistroTiempoDAO.listar_por_empleado(id_empleado))
    print("Total de horas:", RegistroTiempoDAO.total_horas_empleado(id_empleado))


@manejar_errores("listar registros de un proyecto")
def listar_por_proyecto():
    id_proyecto = solicitar_entero("ID del proyecto")
    if ProyectoDAO.buscar_por_id(id_proyecto) is None:
        print("Proyecto no encontrado.")
        return

    _mostrar(RegistroTiempoDAO.listar_por_proyecto(id_proyecto))


@manejar_errores("actualizar registro de tiempo")
def actualizar_registro():
    registro = RegistroTiempoDAO.buscar_por_id(solicitar_entero("ID del registro"))
    if registro is None:
        print("Registro no encontrado.")
        return

    print("Datos actuales:", registro.mostrar_registro(), "|", registro.descripcion)
    print("Deje vacío un campo para conservar su valor.")
    fecha = solicitar_fecha("Nueva fecha", opcional=True)
    horas = solicitar_decimal("Nuevas horas (0-24)", minimo=0.01, maximo=24, opcional=True)
    descripcion = solicitar_texto("Nueva descripción", obligatorio=False)

    if fecha:
        registro.fecha = fecha
    if horas is not None:
        registro.horas_trabajadas = horas
    if descripcion:
        registro.descripcion = descripcion

    if RegistroTiempoDAO.actualizar(registro):
        print("Registro actualizado correctamente.")
    else:
        print("Registro no encontrado.")


@manejar_errores("eliminar registro de tiempo")
def eliminar_registro():
    if RegistroTiempoDAO.eliminar(solicitar_entero("ID del registro")):
        print("Registro eliminado correctamente.")
    else:
        print("Registro no encontrado.")


def menu_registro_tiempo():
    ejecutar_menu("REGISTRO DE TIEMPO", {
        1: ("Registrar horas", registrar_horas),
        2: ("Listar todos los registros", listar_registros),
        3: ("Listar registros de un empleado (con total)", listar_por_empleado),
        4: ("Listar registros de un proyecto", listar_por_proyecto),
        5: ("Actualizar registro", actualizar_registro),
        6: ("Eliminar registro", eliminar_registro),
    })