from typing import Iterable

from app import db
from app.models.especialidad import Especialidad


class EspecialidadRepository:
    def create(self, especialidad: str, facultad: str, universidad: str) -> Especialidad:
        record = Especialidad(especialidad=especialidad, facultad=facultad, universidad=universidad)
        db.session.add(record)
        db.session.commit()
        return record

    def get_by_id(self, especialidad_id: int) -> Especialidad | None:
        return db.session.get(Especialidad, especialidad_id)

    def list_all(self) -> Iterable[Especialidad]:
        return Especialidad.query.all()

    def bulk_seed(self, rows: list[dict]) -> None:
        objects = [Especialidad(**row) for row in rows]
        db.session.bulk_save_objects(objects)
        db.session.commit()
