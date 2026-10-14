# src/dominio/registroTiempo.py
from datetime import date


class RegistroTiempo:
    """Horas que un empleado dedica a un proyecto en una fecha.

    Es la clase de la relación Empleado 1 ── 0..* RegistroTiempo 0..* ── 1 Proyecto.
    Guarda los ids de los extremos (empleado_id y proyecto_id) para poder persistirse.
    """

    # El constructor cumple el registroDeTiempo(fecha, horas) del UML;
    # el resto de los parámetros son opcionales para no romper ese contrato.
    def __init__(self, fecha: str, horas_trabajadas: float, descripcion: str = "",
                 id_registro: int | None = None, empleado_id: int | None = None,
                 proyecto_id: int | None = None):
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion = descripcion
        self._id_registro = id_registro
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id

    # encapsulamiento: atributos privados + validación
    @property
    def id_registro(self) -> int | None:
        return self._id_registro

    @id_registro.setter
    def id_registro(self, valor: int | None):
        # lo usa el DAO para guardar el id que genera la base de datos
        self._id_registro = valor

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha no puede estar vacía")
        try:
            date.fromisoformat(valor.strip())
        except ValueError:
            raise ValueError("La fecha debe tener formato AAAA-MM-DD") from None
        self._fecha = valor.strip()

    @property
    def horas_trabajadas(self) -> float:
        return self._horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, valor: float):
        es_numero = isinstance(valor, (int, float)) and not isinstance(valor, bool)
        if not es_numero or not 0 < valor <= 24:
            raise ValueError("Las horas trabajadas deben ser un número entre 0 y 24")
        self._horas_trabajadas = float(valor)

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        if not isinstance(valor, str):
            raise ValueError("La descripción debe ser texto")
        self._descripcion = valor.strip()

    # comportamiento del UML
    def calcular_horas(self) -> float:
        return self._horas_trabajadas

    def mostrar_registro(self) -> str:
        return (f"[{self.id_registro}] fecha: {self.fecha} hrs: {self.horas_trabajadas} "
                f"(empleado {self.empleado_id}, proyecto {self.proyecto_id})")

    def __str__(self):
        return (f"RegistroTiempo(id={self.id_registro}, fecha={self.fecha}, "
                f"horas={self.horas_trabajadas})")