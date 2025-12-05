from collections.abc import Sequence

from app.extensions import db
from app.models import Programa


class ProgramaRepository:
    @staticmethod
    def crear(programa: Programa) -> Programa:
        db.session.add(programa)
        db.session.commit()
        return programa

    @staticmethod
    def actualizar(programa: Programa, cambios: dict) -> Programa:
        for key, value in cambios.items():
            setattr(programa, key, value)
        db.session.commit()
        return programa

    @staticmethod
    def listar(vigente: bool | None = None) -> Sequence[Programa]:
        query = Programa.query.order_by(Programa.nombre)
        if vigente is not None:
            query = query.filter(Programa.vigente == vigente)
        return query.all()

    @staticmethod
    def obtener_por_id(programa_id: int) -> Programa | None:
        return Programa.query.get(programa_id)

    @staticmethod
    def eliminar(programa: Programa) -> None:
        db.session.delete(programa)
        db.session.commit()
