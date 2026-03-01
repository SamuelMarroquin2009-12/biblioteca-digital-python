from datetime import datetime

class Prestamo:
    def __init__(self, id_prestamo: str, id_libro: str, id_usuario: str, fecha_salida: datetime | None = None) -> None:
        self.id_prestamo = id_prestamo
        self.id_libro = id_libro
        self.id_usuario = id_usuario
        self.fecha_salida = fecha_salida if fecha_salida is not None else datetime.now()
        self.fecha_devolucion = None

    def marcar_devuelto(self) -> None:
        self.fecha_devolucion = datetime.now()