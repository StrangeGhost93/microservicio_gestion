from collections.abc import Sequence

from app.extensions import db
from app.models import AsignacionDocente, Cohorte


class CohorteRepository:
    @staticmethod
    def crear(cohorte: Cohorte) -> Cohorte:
        db.session.add(cohorte)
        db.session.commit()
        return cohorte

    @staticmethod
    def listar(programa_id: int | None = None, estado: str | None = None) -> Sequence[Cohorte]:
        query = Cohorte.query
        if programa_id:
            query = query.filter(Cohorte.programa_id == programa_id)
        if estado:
            query = query.filter(Cohorte.estado == estado)
        return query.order_by(Cohorte.anio).all()

    @staticmethod
    def obtener_por_id(cohorte_id: int) -> Cohorte | None:
        return Cohorte.query.get(cohorte_id)

    @staticmethod
    def actualizar(cohorte: Cohorte, cambios: dict) -> Cohorte:
        for key, value in cambios.items():
            setattr(cohorte, key, value)
        db.session.commit()
        return cohorte

    @staticmethod
    def eliminar(cohorte: Cohorte) -> None:
        db.session.delete(cohorte)
        db.session.commit()

    @staticmethod
    def asignar_docente(asignacion: AsignacionDocente) -> AsignacionDocente:
        db.session.add(asignacion)
        db.session.commit()
        return asignacion
