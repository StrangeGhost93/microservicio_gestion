from collections.abc import Sequence

from app.models import Modulo
from app.repositories import ModuloRepository


class ModuloService:
    @staticmethod
    def crear(data: dict) -> Modulo:
        modulo = Modulo(**data)
        return ModuloRepository.crear(modulo)

    @staticmethod
    def listar(programa_id: int | None = None) -> Sequence[Modulo]:
        return ModuloRepository.listar(programa_id)

    @staticmethod
    def obtener(modulo_id: int) -> Modulo | None:
        return ModuloRepository.obtener_por_id(modulo_id)

    @staticmethod
    def eliminar(modulo_id: int) -> bool:
        modulo = ModuloRepository.obtener_por_id(modulo_id)
        if not modulo:
            return False
        ModuloRepository.eliminar(modulo)
        return True
