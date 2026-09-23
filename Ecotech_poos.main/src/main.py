# main.py
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

encontrado = EmpleadoDAO.buscar_por_id(empleado.id)
print("Encontrado:", encontrado)

print("Listado:")
for item in EmpleadoDAO.listar():
    print(item)
    
    
    
