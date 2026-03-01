class Libro:
    """Entidad que representa un libro en el catálogo."""

    def __init__(self, id_libro: str, titulo: str, autor: str, anio: int, genero: str) -> None:
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.genero = genero
        self.prestado = False

    def __str__(self) -> str:
        # Usamos if/else para determinar el estado
        if self.prestado == True:
            estado = "Prestado"
        else:
            estado = "Disponible"

        # Ajusté los separadores para que coincidan exactamente con tu formato:
        # "{id_libro}: {titulo} - {autor} ({anio}) [{genero}] · {estado}"
        return f"{self.id_libro}: {self.titulo} - {self.autor} ({self.anio}) [{self.genero}] · {estado}"