# src/dominio/departamento.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # solo para los tipos: evita el import circular con Empleado
    from dominio.empleado import Empleado


class Departamento:
    def __init__(self, nombre: str, gerente: str, id_departamento: int):
        self.nombre = nombre
        self.gerente = gerente
        self.id_departamento = id_departamento
        self._empleados: list[Empleado] = []

    # ---- encapsulamiento: atributos privados + validación ----
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del departamento no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def gerente(self) -> str:
        return self._gerente

    @gerente.setter
    def gerente(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El gerente no puede estar vacío")
        self._gerente = valor.strip()

    @property
    def id_departamento(self) -> int:
        return self._id_departamento

    @id_departamento.setter
    def id_departamento(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El id del departamento debe ser un entero positivo")
        self._id_departamento = valor

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    # ---- comportamiento del UML ----
    def agregar_empleado(self, empleado: Empleado) -> None:
        """Agrega el empleado y sincroniza el otro lado de la relación."""
        if empleado in self._empleados:
            return
        self._empleados.append(empleado)
        empleado.asignar_departamento(self)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)