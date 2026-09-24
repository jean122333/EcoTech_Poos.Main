# main.py
from persistencia.conexion import probar_conexion
from persistencia.crear_bd import crear_tablas
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO


def mostrar(empleado):
    return f"[{empleado.id_empleado}] {empleado.nombre} - ${empleado.salario:,.0f}"


if not probar_conexion():
    raise SystemExit("Revisa el archivo .env y que MySQL esté iniciado (XAMPP).")

crear_tablas()

# Los 2 empleados que se guardan en la base de datos local (phpMyAdmin)
nuevos = [
    Empleado(nombre="Ana Torres", salario=850000),
    Empleado(nombre="Luis Pérez", salario=920000),
]

for empleado in nuevos:
    # Si ya existe, no se vuelve a insertar (así no se duplica al ejecutar de nuevo)
    existente = EmpleadoDAO.buscar_por_nombre(empleado.nombre)
    if existente is None:
        EmpleadoDAO.insertar(empleado)
        print("Insertado:", mostrar(empleado))
    else:
        print("Ya existía:", mostrar(existente))

primero = EmpleadoDAO.buscar_por_nombre("Ana Torres")
print("Encontrado por id:", mostrar(EmpleadoDAO.buscar_por_id(primero.id_empleado)))

print("Listado:")
for item in EmpleadoDAO.listar():
    print(" ", mostrar(item))

