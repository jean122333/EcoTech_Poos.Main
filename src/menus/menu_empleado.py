# menus/menu_empleado.py
from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from menus.entradas import (
    manejar_errores, ejecutar_menu, solicitar_entero, solicitar_decimal, solicitar_texto,
)

_MSG_CORREO = "Ya existe un empleado con ese correo, o el departamento indicado no existe."


def _pedir_departamento_id(opcional=True):
    """Pide un id de departamento y comprueba que exista (resultado normal: None)."""
    id_departamento = solicitar_entero("ID del departamento (vacío = ninguno)", opcional=opcional)
    if id_departamento is not None and DepartamentoDAO.buscar_por_id(id_departamento) is None:
        raise ValueError(f"No existe un departamento con ID {id_departamento}")
    return id_departamento


@manejar_errores("registrar empleado", _MSG_CORREO)
def registrar_empleado():
    nombre = solicitar_texto("Nombre")
    correo = solicitar_texto("Correo")
    salario = solicitar_decimal("Salario")

    empleado = Empleado(nombre, correo, salario)  # nace con id=None
    empleado.departamento_id = _pedir_departamento_id()
    EmpleadoDAO.insertar(empleado)
    print("Empleado registrado correctamente:", empleado.mostrar_datos())


@manejar_errores("listar empleados")
def listar_empleados():
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("No hay empleados registrados.")
        return

    print("Listado:")
    for empleado in empleados:
        depto = f" | depto: {empleado.departamento_id}" if empleado.departamento_id else ""
        print(" ", empleado.mostrar_datos() + depto)


@manejar_errores("buscar empleado")
def buscar_empleado():
    print("1. Buscar por ID")
    print("2. Buscar por correo")
    criterio = input("Seleccione el criterio: ").strip()

    if criterio == "1":
        empleado = EmpleadoDAO.buscar_por_id(solicitar_entero("ID del empleado"))
    elif criterio == "2":
        empleado = EmpleadoDAO.buscar_por_correo(solicitar_texto("Correo").lower())
    else:
        print("Opción no válida.")
        return

    # None es un resultado normal, no una excepción
    if empleado is None:
        print("Empleado no encontrado.")
    else:
        print("Encontrado:", empleado.mostrar_datos())


@manejar_errores("actualizar empleado", _MSG_CORREO)
def actualizar_empleado():
    empleado = EmpleadoDAO.buscar_por_id(solicitar_entero("ID del empleado"))
    if empleado is None:
        print("Empleado no encontrado.")
        return

    print("Datos actuales:", empleado.mostrar_datos(), "| depto:", empleado.departamento_id)
    print("Deje vacío un campo para conservar su valor.")

    nombre = solicitar_texto("Nuevo nombre", obligatorio=False)
    correo = solicitar_texto("Nuevo correo", obligatorio=False)
    salario = solicitar_decimal("Nuevo salario", opcional=True)
    departamento_id = _pedir_departamento_id()

    # el objeto cambia en memoria; el DAO sincroniza el cambio con la BD
    if nombre:
        empleado.nombre = nombre
    if correo:
        empleado.correo = correo
    if salario is not None:
        empleado.salario = salario
    if departamento_id is not None:
        empleado.departamento_id = departamento_id

    if EmpleadoDAO.actualizar(empleado):
        print("Empleado actualizado correctamente.")
    else:
        print("Empleado no encontrado.")


@manejar_errores("eliminar empleado")
def eliminar_empleado():
    # tres caminos: eliminado (True), no encontrado (False) o fallo real (excepción)
    if EmpleadoDAO.eliminar(solicitar_entero("ID del empleado")):
        print("Empleado eliminado correctamente.")
    else:
        print("Empleado no encontrado.")


@manejar_errores("consultar la ficha del empleado")
def ver_ficha_empleado():
    id_empleado = solicitar_entero("ID del empleado")
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado is None:
        print("Empleado no encontrado.")
        return

    print("Empleado:", empleado.mostrar_datos())
    if empleado.departamento_id:
        departamento = DepartamentoDAO.buscar_por_id(empleado.departamento_id)
        print("Departamento:", departamento.mostrar_datos() if departamento else "(sin datos)")
    else:
        print("Departamento: (ninguno)")

    proyectos = ProyectoDAO.listar_por_empleado(id_empleado)
    print("Proyectos:", ", ".join(p.nombre for p in proyectos) if proyectos else "(ninguno)")
    print("Horas registradas:", RegistroTiempoDAO.total_horas_empleado(id_empleado))


def menu_empleado():
    ejecutar_menu("EMPLEADOS", {
        1: ("Registrar empleado", registrar_empleado),
        2: ("Listar empleados", listar_empleados),
        3: ("Buscar empleado", buscar_empleado),
        4: ("Actualizar empleado", actualizar_empleado),
        5: ("Eliminar empleado", eliminar_empleado),
        6: ("Ver ficha (departamento, proyectos y horas)", ver_ficha_empleado),
    })