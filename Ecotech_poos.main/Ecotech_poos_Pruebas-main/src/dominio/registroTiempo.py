class RegistroTiempo:
    def __init__(self, fecha: str, hora: str):
        self.fecha = fecha
        self.hora = hora
        
    def mostrar_registro(self) -> str:
        return f"fecha: {self.fecha} hrs: {self.hora}"