# src/dominio/empleado.py
from __future__ import annotations
from typing import TYPE_CHECKING
from dominio.registroTiempo import RegistroTiempo

if TYPE_CHECKING:  # solo para los tipos: evita el import circular
    from dominio.departamento import Departamento
    from dominio.proyecto import Proyecto


class Empleado:
    def __init__(self, nombre, salario=0.0, id_empleado=None, departamento=None):
        self._id_empleado = id_empleado
        self._nombre = nombre
        self._salario = salario
        self._departamento = departamento
        self._proyectos: list[Proyecto] = []
        self._registros: list[RegistroTiempo] = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def id_empleado(self):
        return self._id_empleado

    @id_empleado.setter
    def id_empleado(self, valor):
        # lo usa el DAO para guardar el id que genera la base de datos
        self._id_empleado = valor

    @property
    def salario(self):
        return self._salario

    @property
    def departamento(self):
        return self._departamento

    @property
    def proyectos(self) -> tuple:
        return tuple(self._proyectos)

    @property
    def registros(self) -> tuple:
        return tuple(self._registros)

    def get_salario(self):
        return self._salario

    def registrar_horas(self, fecha, horas) -> bool:
        if horas <= 0 or horas > 24:
            return False
        registro = RegistroTiempo(fecha, horas)
        self._registros.append(registro)
        return True

    def asignar_departamento(self, departamento: Departamento) -> bool:
        """Asigna el departamento y sincroniza el otro lado de la relación."""
        if self._departamento is departamento:
            return False
        self._departamento = departamento
        departamento.agregar_empleado(self)
        return True

    def agregar_proyecto(self, proyecto: Proyecto) -> bool:
        """Agrega el proyecto y sincroniza el otro lado de la relación."""
        if proyecto in self._proyectos:
            return False
        self._proyectos.append(proyecto)
        proyecto.asignar_empleado(self)
        return True

    def __str__(self):
        return f"Empleado(id={self.id_empleado}, nombre={self.nombre}, salario={self.salario})"

    def mostrar_datos(self) -> str:
        return f"id:{self.id_empleado} {self.nombre} - ${self.salario:,.0f}"