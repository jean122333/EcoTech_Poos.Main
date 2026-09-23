# src/dominio/empleado.py​
from dominio.registroTiempo import RegistroTiempo

class Empleado:
    def __init__(self, nombre, correo, id=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        
    def __str__(self):
        return f"Empleado(id={self.id}, nombre={self.nombre}, correo={self.correo})"

    def mostrar_datos(self) -> str:
        return f"id:{self.id} {self.nombre} - {self.correo}"
