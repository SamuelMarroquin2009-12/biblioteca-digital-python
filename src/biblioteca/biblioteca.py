from datetime import datetime
from collections import Counter
from src.biblioteca.libro import Libro
from src.biblioteca.usuario import Usuario
from src.biblioteca.prestamo import Prestamo


class Biblioteca:
    def __init__(self) -> None:
        self.catalogo: dict[str, Libro] = {}
        self.usuarios: dict[str, Usuario] = {}
        self.prestamos_activos: list[Prestamo] = []
        self.indice_por_autor: dict[str, list[str]] = {}
        self.indice_por_genero: dict[str, list[str]] = {}
        self.historial_prestamos: dict[str, list[str]] = {}

    # --- REGISTRO ---
    def registrar_libro(self, libro: Libro) -> None:
        if libro.id_libro in self.catalogo:
            raise ValueError("El id_libro ya existe.")
        self.catalogo[libro.id_libro] = libro
        # Lógica para índices (Avanzado) - NECESARIO PARA TEST_BUSQUEDAS
        self.indice_por_autor.setdefault(libro.autor, []).append(libro.id_libro)
        self.indice_por_genero.setdefault(libro.genero, []).append(libro.id_libro)

    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.id_usuario in self.usuarios:
            raise ValueError("El id_usuario ya existe.")
        self.usuarios[usuario.id_usuario] = usuario

    # --- NEGOCIO ---
    def prestar(self, id_usuario: str, id_libro: str) -> str:
        if id_usuario not in self.usuarios: raise ValueError("Usuario no existe.")
        if id_libro not in self.catalogo: raise ValueError("Libro no existe.")

        u, l = self.usuarios[id_usuario], self.catalogo[id_libro]
        if l.prestado: return "El libro ya está prestado."
        if not u.puede_prestar: return "El usuario no tiene cupo disponible."

        l.prestado = True
        id_p = f"P{len(self.prestamos_activos) + 1:03d}"
        p = Prestamo(id_p, id_libro, id_usuario)
        u.prestamos.append(p)
        self.prestamos_activos.append(p)

        # Guardar en historial para reportes
        self._registrar_evento(id_usuario, f"Prestado: {l.titulo}")
        return f"Préstamo concedido (id={id_p})."

    def devolver(self, id_prestamo: str) -> str:
        p = next((p for p in self.prestamos_activos if p.id_prestamo == id_prestamo), None)
        if not p: return "No se encontró el préstamo activo."

        p.marcar_devuelto()
        self.catalogo[p.id_libro].prestado = False
        self.prestamos_activos.remove(p)
        self._registrar_evento(p.id_usuario, f"Devuelto: {self.catalogo[p.id_libro].titulo}")
        return "Devolución registrada."

    # --- BÚSQUEDAS (Soluciona AttributeError: buscar_por_...) ---
    def buscar_por_autor(self, autor: str) -> list[Libro]:
        ids = self.indice_por_autor.get(autor, [])
        return [self.catalogo[idx] for idx in ids]

    def buscar_por_genero(self, genero: str) -> list[Libro]:
        ids = self.indice_por_genero.get(genero, [])
        return [self.catalogo[idx] for idx in ids]

    def buscar_por_titulo(self, texto: str) -> list[Libro]:
        t = texto.lower()
        return [l for l in self.catalogo.values() if t in l.titulo.lower()]

    # --- REPORTES (Soluciona AttributeError: disponibles_por_genero, etc.) ---
    def disponibles_por_genero(self) -> dict[str, int]:
        res = {}
        for gen, ids in self.indice_por_genero.items():
            res[gen] = sum(1 for idx in ids if not self.catalogo[idx].prestado)
        return res

    def prestamos_activos_por_usuario(self) -> dict[str, int]:
        res = {u_id: 0 for u_id in self.usuarios}
        for p in self.prestamos_activos:
            res[p.id_usuario] += 1
        return res

    def top_autores_mas_prestados(self, k: int = 3) -> list[tuple]:
        autores = []
        for eventos in self.historial_prestamos.values():
            for ev in eventos:
                if "Prestado:" in ev:
                    tit = ev.split("Prestado: ")[1]
                    for l in self.catalogo.values():
                        if l.titulo == tit: autores.append(l.autor)
        return Counter(autores).most_common(k)

    def _registrar_evento(self, id_usuario: str, evento: str) -> None:
        self.historial_prestamos.setdefault(id_usuario, []).append(f"{datetime.now().date()} - {evento}")