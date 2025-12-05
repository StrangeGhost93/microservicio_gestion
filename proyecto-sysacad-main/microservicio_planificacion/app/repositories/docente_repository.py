from collections.abc import Sequence

from app.extensions import db
from app.models import Docente


class DocenteRepository:
    @staticmethod
    def crear(docente: Docente) -> Docente:
        db.session.add(docente)
        db.session.commit()
        return docente

    @staticmethod
    def listar(especialidad: str | None = None) -> Sequence[Docente]:
        query = Docente.query
        if especialidad:
            query = query.filter(Docente.especialidad == especialidad)
        return query.order_by(Docente.apellido, Docente.nombre).all()

    @staticmethod
    def obtener_por_id(docente_id: int) -> Docente | None:
        return Docente.query.get(docente_id)

    @staticmethod
    def actualizar(docente: Docente, cambios: dict) -> Docente:
        for key, value in cambios.items():
            setattr(docente, key, value)
        db.session.commit()
        return docente

    @staticmethod
    def eliminar(docente: Docente) -> None:
        db.session.delete(docente)
        db.session.commit()
