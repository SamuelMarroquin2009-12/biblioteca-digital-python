class Usuario:
    """Representa a una persona que puede solicitar préstamos en la biblioteca."""

    def __init__(self, id_usuario: str, nombre: str, limite_prestamos: int = 3) -> None:
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.limite_prestamos = limite_prestamos
        self.prestamos = []

    @property
    def puede_prestar(self) -> bool:
        # Filtra préstamos donde la fecha de devolución aún es None
        activos = [p for p in self.prestamos if p.fecha_devolucion is None]
        return len(activos) < self.limite_prestamos

    def __str__(self) -> str:
        cantidad = len([p for p in self.prestamos if p.fecha_devolucion is None])
        return f"{self.id_usuario} - {self.nombre} · préstamos activos: {cantidad}"