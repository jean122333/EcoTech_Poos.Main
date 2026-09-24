# src/dominio/empleado.py​
from dominio.registroTiempo import RegistroTiempo

class Empleado:
    def __init__(self, nombre, correo, id_empleado=None, salario=0.0, departamento=None):
        self._id_empleado = id_empleado
        self._nombre = nombre
        self._correo = correo
        self._salario = salario
        self._departamento = departamento
        self._registros = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def id_empleado(self):
        return self._id_empleado

    @property
    def salario(self):
        return self._salario

    @property
    def departamento(self):
        return self._departamento

    def get_salario(self):
        return self._salario

    def registrar_horas(self, fecha, horas) -> bool:
        if horas <= 0 or horas > 24:
            return False
        registro = RegistroTiempo(fecha, horas)
        self._registros.append(registro)
        return True

    def __str__(self):
        return f"Empleado(id={self.id_empleado}, nombre={self.nombre}, correo={self.correo})"

    def mostrar_datos(self) -> str:
        return f"id:{self.id_empleado} {self.nombre} - {self.correo}"
