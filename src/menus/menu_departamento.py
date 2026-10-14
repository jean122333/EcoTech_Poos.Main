# menus/menu_departamento.py
from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from menus.entradas import manejar_errores, ejecutar_menu, solicitar_entero, solicitar_texto

_MSG_DUPLICADO = "Ya existe un departamento con ese nombre."


@manejar_errores("registrar departamento", _MSG_DUPLICADO)
def registrar_departamento():
    nombre = solicitar_texto("Nombre del departamento")
    gerente = solicitar_texto("Gerente")

    departamento = Departamento(nombre, gerente)  # nace con id=None
    DepartamentoDAO.insertar(departamento)
    print("Departamento registrado correctamente:", departamento.mostrar_datos())


@manejar_errores("listar departamentos")
def listar_departamentos():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("No hay departamentos registrados.")
        return

    print("Listado:")
    for departamento in departamentos:
        print(" ", departamento.mostrar_datos())


@manejar_errores("buscar departamento")
def buscar_departamento():
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    criterio = input("Seleccione el criterio: ").strip()

    if criterio == "1":
        departamento = DepartamentoDAO.buscar_por_id(solicitar_entero("ID del departamento"))
    elif criterio == "2":
        departamento = DepartamentoDAO.buscar_por_nombre(solicitar_texto("Nombre"))
    else:
        print("Opción no válida.")
        return

    if departamento is None:
        print("Departamento no encontrado.")
    else:
        print("Encontrado:", departamento.mostrar_datos())


@manejar_errores("actualizar departamento", _MSG_DUPLICADO)
def actualizar_departamento():
    departamento = DepartamentoDAO.buscar_por_id(solicitar_entero("ID del departamento"))
    if departamento is None:
        print("Departamento no encontrado.")
        return

    print("Datos actuales:", departamento.mostrar_datos())
    print("Deje vacío un campo para conservar su valor.")
    nombre = solicitar_texto("Nuevo nombre", obligatorio=False)
    gerente = solicitar_texto("Nuevo gerente", obligatorio=False)

    if nombre:
        departamento.nombre = nombre
    if gerente:
        departamento.gerente = gerente

    if DepartamentoDAO.actualizar(departamento):
        print("Departamento actualizado correctamente.")
    else:
        print("Departamento no encontrado.")


@manejar_errores("eliminar departamento")
def eliminar_departamento():
    # los empleados del departamento se conservan, quedan sin departamento
    if DepartamentoDAO.eliminar(solicitar_entero("ID del departamento")):
        print("Departamento eliminado correctamente.")
    else:
        print("Departamento no encontrado.")


@manejar_errores("listar empleados del departamento")
def ver_empleados_departamento():
    departamento = DepartamentoDAO.buscar_por_id(solicitar_entero("ID del departamento"))
    if departamento is None:
        print("Departamento no encontrado.")
        return

    empleados = EmpleadoDAO.listar_por_departamento(departamento.id_departamento)
    print("Departamento:", departamento.mostrar_datos())
    if not empleados:
        print("No tiene empleados.")
    for empleado in empleados:
        print(" ", empleado.mostrar_datos())


def menu_departamento():
    ejecutar_menu("DEPARTAMENTOS", {
        1: ("Registrar departamento", registrar_departamento),
        2: ("Listar departamentos", listar_departamentos),
        3: ("Buscar departamento", buscar_departamento),
        4: ("Actualizar departamento", actualizar_departamento),
        5: ("Eliminar departamento", eliminar_departamento),
        6: ("Ver empleados del departamento", ver_empleados_departamento),
    })