# src/dominio/proyecto.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # solo para los tipos: evita el import circular con Empleado
    from dominio.empleado import Empleado


class Proyecto:
    def __init__(self, nombre: str, fecha_inicio: str, descripcion: str):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.descripcion = descripcion
        self._empleados: list[Empleado] = []

    # ---- encapsulamiento: atributos privados + validación ----
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def fecha_inicio(self) -> str:
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha de inicio no puede estar vacía")
        self._fecha_inicio = valor.strip()

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        if not isinstance(valor, str):
            raise ValueError("La descripción debe ser texto")
        self._descripcion = valor.strip()

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    # ---- comportamiento del UML ----
    def asignar_empleado(self, empleado: Empleado) -> bool:
        """Asigna el empleado al proyecto y sincroniza el otro lado de la relación."""
        if empleado in self._empleados:
            return False

        self._empleados.append(empleado)
        empleado.agregar_proyecto(self)  # Empleado hace lo mismo con este proyecto
        return True

    def mostrar_datos(self) -> str:
        return f"{self.nombre} (inicio: {self.fecha_inicio}) - {self.descripcion}"