# main.py
import logging

from persistencia.conexion import probar_conexion, ERRORES_INTEGRIDAD
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto

# el detalle técnico del error se guarda en un archivo; el usuario solo ve un mensaje seguro
logging.basicConfig(filename="ecotech.log", level=logging.ERROR)

MENSAJE_SEGURO = "No fue posible completar la operación."


def mostrar(empleado):
    return f"[{empleado.id_empleado}] {empleado.nombre} <{empleado.correo}> - ${empleado.salario:,.0f}"


# validación de entradas
def solicitar_opcion():
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion < 0 or opcion > 6:
                print("Opción fuera de rango.")
                continue

            return opcion

        except ValueError:
            print("Debe ingresar un número.")


def solicitar_id():
    while True:
        try:
            id_empleado = int(input("ID del empleado: "))

            if id_empleado <= 0:
                print("El ID debe ser un número positivo.")
                continue

            return id_empleado

        except ValueError:
            print("Debe ingresar un número entero.")


def solicitar_salario():
    while True:
        try:
            salario = float(input("Salario: "))

            if salario < 0:
                print("El salario no puede ser negativo.")
                continue

            return salario

        except ValueError:
            print("Debe ingresar un número.")


# operaciones del menú (CRUD)
def registrar_empleado():
    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()
    salario = solicitar_salario()

    try:
        empleado = Empleado(nombre, correo, salario)  # nace con id=None
        EmpleadoDAO.insertar(empleado)
        print("Empleado registrado correctamente:", mostrar(empleado))
    except ValueError as error:
        # error esperable: datos inválidos del usuario
        print("Datos inválidos:", error)
    except ERRORES_INTEGRIDAD:
        print("Ya existe un empleado con ese correo.")
    except Exception:
        logging.exception("Error al registrar empleado")
        print(MENSAJE_SEGURO)


def listar_empleados():
    try:
        empleados = EmpleadoDAO.listar()
        if not empleados:
            print("No hay empleados registrados.")
            return

        print("Listado:")
        for empleado in empleados:
            print(" ", mostrar(empleado))
    except Exception:
        logging.exception("Error al listar empleados")
        print(MENSAJE_SEGURO)


def buscar_empleado():
    print("1. Buscar por ID")
    print("2. Buscar por correo")
    criterio = input("Seleccione el criterio: ").strip()

    try:
        if criterio == "1":
            empleado = EmpleadoDAO.buscar_por_id(solicitar_id())
        elif criterio == "2":
            empleado = EmpleadoDAO.buscar_por_correo(input("Correo: ").strip().lower())
        else:
            print("Opción no válida.")
            return

        # None es un resultado normal, no una excepción
        if empleado is None:
            print("Empleado no encontrado.")
        else:
            print("Encontrado:", mostrar(empleado))
    except Exception:
        logging.exception("Error al buscar empleado")
        print(MENSAJE_SEGURO)


def actualizar_empleado():
    id_empleado = solicitar_id()

    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("Empleado no encontrado.")
            return

        print("Datos actuales:", mostrar(empleado))
        print("Deje vacío un campo para conservar su valor.")

        nombre = input("Nuevo nombre: ").strip()
        correo = input("Nuevo correo: ").strip()
        salario = input("Nuevo salario: ").strip()

        # el objeto cambia en memoria; el DAO sincroniza el cambio con la BD
        if nombre:
            empleado.nombre = nombre
        if correo:
            empleado.correo = correo
        if salario:
            empleado.salario = float(salario)

        if EmpleadoDAO.actualizar(empleado):
            print("Empleado actualizado correctamente.")
        else:
            print("Empleado no encontrado.")
    except ValueError as error:
        print("Datos inválidos:", error)
    except ERRORES_INTEGRIDAD:
        print("Ya existe un empleado con ese correo.")
    except Exception:
        logging.exception("Error al actualizar empleado")
        print(MENSAJE_SEGURO)


def eliminar_empleado():
    id_empleado = solicitar_id()

    # tres caminos: eliminado (True), no encontrado (False) o fallo real (excepción)
    try:
        if EmpleadoDAO.eliminar(id_empleado):
            print("Empleado eliminado correctamente.")
        else:
            print("Empleado no encontrado.")
    except Exception:
        logging.exception("Error al eliminar empleado")
        print(MENSAJE_SEGURO)


def demo_relaciones():
    print("\n--- Demo de relaciones ---")
    ana = Empleado("Ana Torres", "ana.torres@ecotech.cl", 850000)
    luis = Empleado("Luis Pérez", "luis.perez@ecotech.cl", 920000)

    # Departamento 1 ── 0..* Empleado (se sincroniza en ambos sentidos)
    ti = Departamento(nombre="Tecnología", gerente="Marta Soto", id_departamento=1)
    ti.agregar_empleado(ana)
    ti.agregar_empleado(luis)
    print("Empleados en", ti.nombre, ":", ti.cantidad_empleados())
    print("Departamento de Ana:", ana.departamento.nombre)

    # Empleado 0..* ── 0..* Proyecto (también en ambos sentidos)
    web = Proyecto("Sitio web", "2026-09-24", "Rediseño del sitio corporativo")
    web.asignar_empleado(ana)
    web.asignar_empleado(luis)
    print("Empleados en", web.nombre, ":", [e.nombre for e in web.empleados])
    print("Proyectos de Ana:", [p.nombre for p in ana.proyectos])
    print("¿Asignar de nuevo a Ana?", web.asignar_empleado(ana))  # False: no se duplica

    # Empleado 1 ── 0..* RegistroTiempo
    print("Registrar 8 h:", ana.registrar_horas("2026-09-24", 8))
    print("Registrar 6.5 h:", ana.registrar_horas("2026-09-25", 6.5))
    print("Registrar 30 h (inválido):", ana.registrar_horas("2026-09-26", 30))
    total = sum(r.calcular_horas() for r in ana.registros)
    print("Horas totales de Ana:", total)


# menú y punto de entrada
def mostrar_menu():
    print("\n===== ECOTECH =====")
    print("1. Registrar empleado")
    print("2. Listar empleados")
    print("3. Buscar empleado")
    print("4. Actualizar empleado")
    print("5. Eliminar empleado")
    print("6. Demo de relaciones")
    print("0. Salir")


def main():
    if not probar_conexion():
        raise SystemExit("Revisa el archivo .env y que MySQL esté iniciado.")

    try:
        crear_tablas()
    except Exception:
        logging.exception("Error al preparar la base de datos")
        raise SystemExit("No fue posible preparar la base de datos.")

    acciones = {
        1: registrar_empleado,
        2: listar_empleados,
        3: buscar_empleado,
        4: actualizar_empleado,
        5: eliminar_empleado,
        6: demo_relaciones,
    }

    while True:
        mostrar_menu()
        opcion = solicitar_opcion()

        if opcion == 0:
            print("Hasta luego.")
            break

        acciones[opcion]()


# ejecuta main() solo cuando este archivo se inicia directamente
if __name__ == "__main__":
    main()