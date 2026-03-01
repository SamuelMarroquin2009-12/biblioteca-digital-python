class Libro:
    """Entidad que representa un libro en el catálogo."""

    def __init__(self, id_libro: str, titulo: str, autor: str, anio: int, genero: str) -> None:
        # Asignamos cada parámetro a un atributo de instancia (self)
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.genero = genero
        # Inicializamos el estado como False (Disponible) por defecto
        self.prestado = False

    def __str__(self) -> str:
        # Usamos una variable auxiliar para el texto del estado según el booleano
        estado = "Prestado" if self.prestado else "Disponible"
        # Retornamos el f-string con el formato exacto de la rúbrica
        return f"{self.id_libro}: {self.titulo} - {self.autor} ({self.anio}) [{self.genero}] · {estado}"