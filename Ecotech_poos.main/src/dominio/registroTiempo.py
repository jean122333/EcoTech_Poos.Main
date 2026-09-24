# src/dominio/registroTiempo.py
class RegistroTiempo:
    # El constructor cumple el registroDeTiempo(fecha, horas) del UML
    def __init__(self, fecha: str, horas_trabajadas: float):
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas

    #encapsulamiento: atributos privados + validación
    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha no puede estar vacía")
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

    # comportamiento del UML
    def calcular_horas(self) -> float:
        return self._horas_trabajadas

    def mostrar_registro(self) -> str:
        return f"fecha: {self.fecha} hrs: {self.horas_trabajadas}"