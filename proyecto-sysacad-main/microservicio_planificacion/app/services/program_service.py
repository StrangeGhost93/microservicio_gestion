from collections.abc import Sequence

from app.models import Programa
from app.repositories import ProgramaRepository


class ProgramaService:
    @staticmethod
    def crear(data: dict) -> Programa:
        programa = Programa(**data)
        return ProgramaRepository.crear(programa)

    @staticmethod
    def listar(vigente: bool | None = None) -> Sequence[Programa]:
        return ProgramaRepository.listar(vigente)

    @staticmethod
    def obtener(programa_id: int) -> Programa | None:
        return ProgramaRepository.obtener_por_id(programa_id)

    @staticmethod
    def actualizar(programa_id: int, data: dict) -> Programa | None:
        programa = ProgramaRepository.obtener_por_id(programa_id)
        if not programa:
            return None
        return ProgramaRepository.actualizar(programa, data)

    @staticmethod
    def eliminar(programa_id: int) -> bool:
        programa = ProgramaRepository.obtener_por_id(programa_id)
        if not programa:
            return False
        ProgramaRepository.eliminar(programa)
        return True
