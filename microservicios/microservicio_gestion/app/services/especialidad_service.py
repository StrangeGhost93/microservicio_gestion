"""Servicio de especialidades respaldado por base de datos."""

from __future__ import annotations
from collections.abc import Sequence

from app.models.especialidad import Especialidad
from app.repositories.especialidad_repository import EspecialidadRepository


class EspecialidadService:
    def __init__(self, repository: EspecialidadRepository | None = None) -> None:
        self.repository = repository or EspecialidadRepository()

    def listar(self) -> Sequence[Especialidad]:
        return list(self.repository.list_all())

    def obtener(self, especialidad_id: int) -> Especialidad | None:
        return self.repository.get_by_id(especialidad_id)
