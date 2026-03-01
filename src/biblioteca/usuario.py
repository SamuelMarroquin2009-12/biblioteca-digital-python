class Usuario:
    """Representa a una persona que puede solicitar préstamos."""

    def __init__(self, id_usuario: str, nombre: str, limite_prestamos: int = 3) -> None:
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.limite_prestamos = limite_prestamos
        # Creamos la lista vacía donde guardaremos los objetos 'Prestamo'
        self.prestamos = []

    @property
    def puede_prestar(self) -> bool:
        # Filtramos: un préstamo es activo si NO tiene fecha de devolución (es None)
        activos = [p for p in self.prestamos if p.fecha_devolucion is None]
        # Retornamos True si aún no llega al límite de préstamos permitidos
        return len(activos) < self.limite_prestamos

    def __str__(self) -> str:
        # Contamos cuántos elementos de la lista siguen activos
        cantidad = len([p for p in self.prestamos if p.fecha_devolucion is None])
        return f"{self.id_usuario} - {self.nombre} · préstamos activos: {cantidad}"