# main.py
from dominio.departamento import Departamento
from persistencia.crear_bd import crear_tablas
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

crear_tablas()


empleado = Empleado(
    nombre="Ana Torres",
    correo="ana.torres@ecotech.cl"
)

EmpleadoDAO.insertar(empleado)
print("Insertado:", empleado.mostrar_datos())

encontrado = EmpleadoDAO.buscar_por_id(empleado.id_empleado)
print("Encontrado:", encontrado)

print("Listado:")
for item in EmpleadoDAO.listar():
    print(item)

departamento = Departamento("Ventas", 1)
departamento.agregar_empleado(empleado)
print("Departamento:", empleado.departamento.nombre)
print("Empleados en el departamento:", departamento.cantidad_empleados())
 

empleado.registrar_horas("2026-09-24", 8)
empleado.registrar_horas("2026-09-25", 6)
print("Horas registradas:")
for registro in empleado.registros:
    print(registro.mostrar_registro())
    
  
    
