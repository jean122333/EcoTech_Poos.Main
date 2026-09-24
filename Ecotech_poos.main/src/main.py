# main.py
from persistencia.conexion import probar_conexion
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto


def mostrar(empleado):
    return f"[{empleado.id_empleado}] {empleado.nombre} - ${empleado.salario:,.0f}"


# ---------- Parte 1: conexión y base de datos ----------
if not probar_conexion():
    raise SystemExit("Revisa el archivo .env y que MySQL esté iniciado.")

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

# ---------- Parte 2: demo de relaciones ----------
print("\n--- Demo de relaciones ---")
ana, luis = nuevos

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

# Empleado 1 ── 0..*