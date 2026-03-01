from datetime import datetime
from collections import Counter  # Para contar autores más frecuentes
from src.biblioteca.libro import Libro
from src.biblioteca.usuario import Usuario
from src.biblioteca.prestamo import Prestamo


class Biblioteca:
    def __init__(self) -> None:
        # Estructuras principales: diccionarios para acceso rápido por ID
        self.catalogo: dict[str, Libro] = {}
        self.usuarios: dict[str, Usuario] = {}
        self.prestamos_activos: list[Prestamo] = []
        # Índices de búsqueda (Avanzado) para no recorrer todo el catálogo
        self.indice_por_autor: dict[str, list[str]] = {}
        self.indice_por_genero: dict[str, list[str]] = {}
        # Diccionario para guardar qué libros ha pedido cada usuario
        self.historial_prestamos: dict[str, list[str]] = {}

    def registrar_libro(self, libro: Libro) -> None:
        # Validamos que no exista el ID (evita duplicados)
        if libro.id_libro in self.catalogo: raise ValueError("El id_libro ya existe.")
        # Guardamos en catálogo e índices de búsqueda rápida
        self.catalogo[libro.id_libro] = libro
        self.indice_por_autor.setdefault(libro.autor, []).append(libro.id_libro)
        self.indice_por_genero.setdefault(libro.genero, []).append(libro.id_libro)

    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.id_usuario in self.usuarios: raise ValueError("El id_usuario ya existe.")
        self.usuarios[usuario.id_usuario] = usuario

    def prestar(self, id_usuario: str, id_libro: str) -> str:
        # Validaciones de existencia de objetos
        if id_usuario not in self.usuarios: raise ValueError("Usuario no existe.")
        if id_libro not in self.catalogo: raise ValueError("Libro no existe.")

        u, l = self.usuarios[id_usuario], self.catalogo[id_libro]
        # Reglas de negocio: disponibilidad y cupo del usuario
        if l.prestado: return "El libro ya está prestado."
        if not u.puede_prestar: return "El usuario no tiene cupo disponible."

        l.prestado = True  # Cambiamos estado del libro
        id_p = f"P{len(self.prestamos_activos) + 1:03d}"  # Generamos ID tipo P001
        p = Prestamo(id_p, id_libro, id_usuario)

        # Guardamos el préstamo en el sistema y en el usuario
        u.prestamos.append(p)
        self.prestamos_activos.append(p)
        self._registrar_evento(id_usuario, f"Prestado: {l.titulo}")
        return f"Préstamo concedido (id={id_p})."

    def devolver(self, id_prestamo: str) -> str:
        # Buscamos el préstamo en la lista de activos
        p = next((p for p in self.prestamos_activos if p.id_prestamo == id_prestamo), None)
        if not p: return "No se encontró el préstamo activo."

        p.marcar_devuelto()  # Actualizamos fecha en el objeto Prestamo
        self.catalogo[p.id_libro].prestado = False  # El libro queda disponible
        self.prestamos_activos.remove(p)  # Sale de la lista de pendientes
        self._registrar_evento(p.id_usuario, f"Devuelto: {self.catalogo[p.id_libro].titulo}")
        return "Devolución registrada."

    # --- SOLUCIÓN BÚSQUEDAS (Elimina errores de imagen 1, 2 y 4) ---
    def buscar_por_autor(self, autor: str) -> list[Libro]:
        # Convertimos la lista de IDs del índice en objetos Libro reales
        return [self.catalogo[idx] for idx in self.indice_por_autor.get(autor, [])]

    def buscar_por_genero(self, genero: str) -> list[Libro]:
        return [self.catalogo[idx] for idx in self.indice_por_genero.get(genero, [])]

    def buscar_por_titulo(self, texto: str) -> list[Libro]:
        # Búsqueda parcial (case-insensitive) en todos los títulos
        t = texto.lower()
        return [l for l in self.catalogo.values() if t in l.titulo.lower()]

    # --- SOLUCIÓN REPORTES (Elimina errores de imagen 3, 5 y 6) ---
    def disponibles_por_genero(self) -> dict[str, int]:
        # Crea un mapa de cuántos libros NO están prestados por cada género
        return {gen: sum(1 for idx in ids if not self.catalogo[idx].prestado)
                for gen, ids in self.indice_por_genero.items()}

    def prestamos_activos_por_usuario(self) -> dict[str, int]:
        # Cuenta cuántos préstamos tiene cada usuario en la lista de activos
        res = {u_id: 0 for u_id in self.usuarios}
        for p in self.prestamos_activos: res[p.id_usuario] += 1
        return res

    def top_autores_mas_prestados(self, k: int = 3) -> list[tuple]:
        # Analizamos el historial de eventos para contar autores
        autores = []
        for evs in self.historial_prestamos.values():
            for e in evs:
                if "Prestado:" in e:
                    titulo = e.split("Prestado: ")[1]
                    # Buscamos el autor asociado a ese título en el catálogo
                    for l in self.catalogo.values():
                        if l.titulo == titulo: autores.append(l.autor)
        return Counter(autores).most_common(k)

    def _registrar_evento(self, id_u: str, ev: str) -> None:
        # Método auxiliar para guardar la actividad con fecha
        self.historial_prestamos.setdefault(id_u, []).append(f"{datetime.now().date()} - {ev}")