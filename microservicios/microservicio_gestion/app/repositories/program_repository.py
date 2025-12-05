"""Auxiliares de repositorio que encapsulan la persistencia de Programa."""

from collections.abc import Mapping, Sequence

from app.extensions import db
from app.models import Programa


class ProgramaRepository:
    """Colección de operaciones CRUD sobre la entidad Programa."""

    @staticmethod
    def crear(programa: Programa) -> Programa:
        """Persistir un programa y devolver la entidad con su ID asignado."""
        db.session.add(programa)
        db.session.commit()
        return programa

    @staticmethod
    def actualizar(programa: Programa, cambios: Mapping) -> Programa:
        """Actualizar campos simples de la instancia existente y guardar cambios."""
        for key, value in cambios.items():
            setattr(programa, key, value)
        db.session.commit()
        return programa

    @staticmethod
    def listar(vigente: bool | None = None) -> Sequence[Programa]:
        """Obtener todos los programas ordenados alfabéticamente, opcionalmente filtrados."""
        query = Programa.query.order_by(Programa.nombre)
        if vigente is not None:
            query = query.filter(Programa.vigente == vigente)
        return query.all()

    @staticmethod
    def obtener_por_id(programa_id: int) -> Programa | None:
        """Retornar un programa por su ID o `None` si no existe."""
        return Programa.query.get(programa_id)

    @staticmethod
    def eliminar(programa: Programa) -> None:
        """Eliminar definitivamente un programa de la base."""
        db.session.delete(programa)
        db.session.commit()
