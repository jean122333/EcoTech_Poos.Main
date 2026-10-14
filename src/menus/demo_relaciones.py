# menus/demo_relaciones.py
"""Demostración en memoria de las relaciones del UML (no usa la base de datos)."""
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto


def demo_relaciones():
    print("\n--- Demo de relaciones (en memoria) ---")
    ana = Empleado("Ana Torres", "ana.torres@ecotech.cl", 850000)
    luis = Empleado("Luis Pérez", "luis.perez@ecotech.cl", 920000)

    # Departamento 1 ── 0..* Empleado (se sincroniza en ambos sentidos)
    ti = Departamento(nombre="Tecnología", gerente="Marta Soto")
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
    print("Registrar 8 h:", ana.registrar_horas("2026-09-24", 8, "Maquetación", web))
    print("Registrar 6.5 h:", ana.registrar_horas("2026-09-25", 6.5))
    print("Registrar 30 h (inválido):", ana.registrar_horas("2026-09-26", 30))
    total = sum(r.calcular_horas() for r in ana.registros)
    print("Horas totales de Ana:", total)