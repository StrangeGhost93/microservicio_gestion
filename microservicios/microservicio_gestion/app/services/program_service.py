"""Domain-level orchestration for entidades Programa."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from app.models import Programa
from app.repositories import ProgramaRepository


class ProgramaService:
    """Stateless façade that encapsulates business rules for programas."""

    @staticmethod
    def crear(data: Mapping) -> Programa:
        """Crear un programa a partir del payload validado."""
        programa = Programa(**data)
        return ProgramaRepository.crear(programa)

    @staticmethod
    def listar(vigente: bool | None = None) -> Sequence[Programa]:
        """Listar programas opcionalmente filtrando por vigencia."""
        return ProgramaRepository.listar(vigente)

    @staticmethod
    def obtener(programa_id: int) -> Programa | None:
        """Obtener un programa por su identificador interno."""
        return ProgramaRepository.obtener_por_id(programa_id)

    @staticmethod
    def actualizar(programa_id: int, data: Mapping) -> Programa | None:
        """Actualizar un programa existente si se encuentra en la base."""
        programa = ProgramaRepository.obtener_por_id(programa_id)
        if not programa:
            return None
        return ProgramaRepository.actualizar(programa, data)

    @staticmethod
    def eliminar(programa_id: int) -> bool:
        """Eliminar (soft) un programa devolviendo si existía o no."""
        programa = ProgramaRepository.obtener_por_id(programa_id)
        if not programa:
            return False
        ProgramaRepository.eliminar(programa)
        return True
