from collections.abc import Sequence

from app.extensions import db
from app.models import Modulo


class ModuloRepository:
    @staticmethod
    def crear(modulo: Modulo) -> Modulo:
        db.session.add(modulo)
        db.session.commit()
        return modulo

    @staticmethod
    def listar(programa_id: int | None = None) -> Sequence[Modulo]:
        query = Modulo.query
        if programa_id:
            query = query.filter(Modulo.programa_id == programa_id)
        return query.order_by(Modulo.titulo).all()

    @staticmethod
    def obtener_por_id(modulo_id: int) -> Modulo | None:
        return Modulo.query.get(modulo_id)

    @staticmethod
    def eliminar(modulo: Modulo) -> None:
        db.session.delete(modulo)
        db.session.commit()
