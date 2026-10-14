# menus/menu_proyecto.py
from dominio.proyecto import Proyecto
from persistencia.conexion import ERRORES_INTEGRIDAD
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from menus.entradas import (
    manejar_errores, ejecutar_menu, solicitar_entero, solicitar_fecha, solicitar_texto,
)

_MSG_DUPLICADO = "Ya existe un proyecto con ese nombre."


@manejar_errores("registrar proyecto", _MSG_DUPLICADO)
def registrar_proyecto():
    nombre = solicitar_texto("Nombre del proyecto")
    fecha = solicitar_fecha("Fecha de inicio")
    descripcion = solicitar_texto("Descripción", obligatorio=False)

    proyecto = Proyecto(nombre, fecha, descripcion)  # nace con id=None
    ProyectoDAO.insertar(proyecto)
    print("Proyecto registrado correctamente:", proyecto.mostrar_datos())


@manejar_errores("listar proyectos")
def listar_proyectos():
    proyectos = ProyectoDAO.listar()
    if not proyectos:
        print("No hay proyectos registrados.")
        return

    print("Listado:")
    for proyecto in proyectos:
        print(" ", proyecto.mostrar_datos())


@manejar_errores("buscar proyecto")
def buscar_proyecto():
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    criterio = input("Seleccione el criterio: ").strip()

    if criterio == "1":
        proyecto = ProyectoDAO.buscar_por_id(solicitar_entero("ID del proyecto"))
    elif criterio == "2":
        proyecto = ProyectoDAO.buscar_por_nombre(solicitar_texto("Nombre"))
    else:
        print("Opción no válida.")
        return

    if proyecto is None:
        print("Proyecto no encontrado.")
    else:
        print("Encontrado:", proyecto.mostrar_datos())


@manejar_errores("actualizar proyecto", _MSG_DUPLICADO)
def actualizar_proyecto():
    proyecto = ProyectoDAO.buscar_por_id(solicitar_entero("ID del proyecto"))
    if proyecto is None:
        print("Proyecto no encontrado.")
        return

    print("Datos actuales:", proyecto.mostrar_datos())
    print("Deje vacío un campo para conservar su valor.")
    nombre = solicitar_texto("Nuevo nombre", obligatorio=False)
    fecha = solicitar_fecha("Nueva fecha de inicio", opcional=True)
    descripcion = solicitar_texto("Nueva descripción", obligatorio=False)

    if nombre:
        proyecto.nombre = nombre
    if fecha:
        proyecto.fecha_inicio = fecha
    if descripcion:
        proyecto.descripcion = descripcion

    if ProyectoDAO.actualizar(proyecto):
        print("Proyecto actualizado correctamente.")
    else:
        print("Proyecto no encontrado.")


@manejar_errores("eliminar proyecto")
def eliminar_proyecto():
    if ProyectoDAO.eliminar(solicitar_entero("ID del proyecto")):
        print("Proyecto eliminado correctamente.")
    else:
        print("Proyecto no encontrado.")


@manejar_errores("asignar empleado a proyecto")
def asignar_empleado():
    id_proyecto = solicitar_entero("ID del proyecto")
    id_empleado = solicitar_entero("ID del empleado")

    if ProyectoDAO.buscar_por_id(id_proyecto) is None:
        print("Proyecto no encontrado.")
        return
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        print("Empleado no encontrado.")
        return

    try:
        ProyectoDAO.asignar_empleado(id_proyecto, id_empleado)
        print("Empleado asignado al proyecto.")
    except ERRORES_INTEGRIDAD:
        # la clave primaria compuesta (empleado, proyecto) impide duplicar la asignación
        print("Ese empleado ya estaba asignado al proyecto.")


@manejar_errores("quitar empleado de proyecto")
def quitar_empleado():
    id_proyecto = solicitar_entero("ID del proyecto")
    id_empleado = solicitar_entero("ID del empleado")

    if ProyectoDAO.quitar_empleado(id_proyecto, id_empleado):
        print("Empleado quitado del proyecto.")
    else:
        print("Ese empleado no estaba asignado al proyecto.")


@manejar_errores("listar empleados del proyecto")
def ver_empleados_proyecto():
    proyecto = ProyectoDAO.buscar_por_id(solicitar_entero("ID del proyecto"))
    if proyecto is None:
        print("Proyecto no encontrado.")
        return

    empleados = EmpleadoDAO.listar_por_proyecto(proyecto.id_proyecto)
    print("Proyecto:", proyecto.mostrar_datos())
    if not empleados:
        print("No tiene empleados asignados.")
    for empleado in empleados:
        print(" ", empleado.mostrar_datos())


def menu_proyecto():
    ejecutar_menu("PROYECTOS", {
        1: ("Registrar proyecto", registrar_proyecto),
        2: ("Listar proyectos", listar_proyectos),
        3: ("Buscar proyecto", buscar_proyecto),
        4: ("Actualizar proyecto", actualizar_proyecto),
        5: ("Eliminar proyecto", eliminar_proyecto),
        6: ("Asignar empleado al proyecto", asignar_empleado),
        7: ("Quitar empleado del proyecto", quitar_empleado),
        8: ("Ver empleados del proyecto", ver_empleados_proyecto),
    })