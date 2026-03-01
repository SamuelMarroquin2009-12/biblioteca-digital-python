"""
Módulo que define la clase Libro.

TODO (Principiantes - Paso 1):
- Definir la clase Libro con los atributos indicados.
- Implementar el método __str__ para mostrar la información del libro.
"""


class Libro:
    """Entidad que representa un libro en el catálogo."""

    def __init__(self, id_libro: str, titulo: str, autor: str, anio: int, genero: str) -> None:
        """
        Inicializa un nuevo libro.
        TODO: Asignar los parámetros a atributos de instancia.
        Además, crear un atributo 'prestado' que inicie en False.

        Args:
            id_libro: Identificador único del libro (ej: "L001")
            titulo: Título del libro
            autor: Nombre del autor
            anio: Año de publicación
            genero: Género literario (ej: "Ciencia Ficción")
        """
        self.id_libro=id_libro
        self.titulo=titulo
        self.autor=autor
        self.anio=anio
        self.genero=genero
        self.prestado=False
    def __str__(self) -> str:
        """
        Devuelve una representación en texto del libro.

        TODO: Retornar un string con el formato:
        "{id_libro}: {titulo} - {autor} ({anio}) [{genero}] · {estado}"

        Donde estado es "Prestado" si prestado=True, o "Disponible" si prestado=False.

        Ejemplo de salida:
        "L001: Cien años de soledad - García Márquez (1967) [Realismo Mágico] · Disponible"
        """
        if self.prestado == True :
            estado="Prestado"
        if self.prestado == False :
            estado="Disponible"
        return f"{self.id_libro}:{self.titulo}-{self.autor} ({self.anio}) [{self.genero}]·{estado}"

