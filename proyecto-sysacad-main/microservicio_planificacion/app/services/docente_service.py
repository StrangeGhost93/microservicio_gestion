from collections.abc import Sequence

from app.models import Docente
from app.repositories import DocenteRepository


class DocenteService:
    @staticmethod
    def crear(data: dict) -> Docente:
        docente = Docente(**data)
        return DocenteRepository.crear(docente)

    @staticmethod
    def listar(especialidad: str | None = None) -> Sequence[Docente]:
        return DocenteRepository.listar(especialidad)

    @staticmethod
    def obtener(docente_id: int) -> Docente | None:
        return DocenteRepository.obtener_por_id(docente_id)

    @staticmethod
    def actualizar(docente_id: int, data: dict) -> Docente | None:
        docente = DocenteRepository.obtener_por_id(docente_id)
        if not docente:
            return None
        return DocenteRepository.actualizar(docente, data)

    @staticmethod
    def eliminar(docente_id: int) -> bool:
        docente = DocenteRepository.obtener_por_id(docente_id)
        if not docente:
            return False
        DocenteRepository.eliminar(docente)
        return True
