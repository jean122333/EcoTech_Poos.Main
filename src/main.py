# main.py
import logging

from persistencia.conexion import probar_conexion
from persistencia.crear_bd import crear_tablas
from menus.entradas import ejecutar_menu
from menus.menu_empleado import menu_empleado
from menus.menu_departamento import menu_departamento
from menus.menu_proyecto import menu_proyecto
from menus.menu_registro_tiempo import menu_registro_tiempo
from menus.demo_relaciones import demo_relaciones

# el detalle técnico del error se guarda en un archivo; el usuario solo ve un mensaje seguro
logging.basicConfig(
    filename="ecotech.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main():
    # main.py solo coordina: no contiene SQL ni credenciales
    if not probar_conexion():
        raise SystemExit("Revisa el archivo .env y que MariaDB/MySQL esté iniciado.")

    try:
        crear_tablas()
    except Exception:
        logging.exception("Error al preparar la base de datos")
        raise SystemExit("No fue posible preparar la base de datos.")

    try:
        ejecutar_menu("ECOTECH", {
            1: ("Empleados", menu_empleado),
            2: ("Departamentos", menu_departamento),
            3: ("Proyectos", menu_proyecto),
            4: ("Registro de tiempo", menu_registro_tiempo),
            5: ("Demo de relaciones (sin base de datos)", demo_relaciones),
        })
    except (KeyboardInterrupt, EOFError):
        print()  # Ctrl+C o Ctrl+D: salida limpia, sin traceback

    print("Hasta luego.")


# ejecuta main() solo cuando este archivo se inicia directamente
if __name__ == "__main__":
    main()