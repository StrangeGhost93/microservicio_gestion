from collections.abc import Sequence

from app.models import AsignacionDocente, Cohorte
from app.repositories import CohorteRepository, DocenteRepository, ModuloRepository


class CohorteService:
    @staticmethod
    def crear(data: dict) -> Cohorte:
        cohorte = Cohorte(**data)
        return CohorteRepository.crear(cohorte)

    @staticmethod
    def listar(programa_id: int | None = None, estado: str | None = None) -> Sequence[Cohorte]:
        return CohorteRepository.listar(programa_id, estado)

    @staticmethod
    def obtener(cohorte_id: int) -> Cohorte | None:
        return CohorteRepository.obtener_por_id(cohorte_id)

    @staticmethod
    def actualizar(cohorte_id: int, data: dict) -> Cohorte | None:
        cohorte = CohorteRepository.obtener_por_id(cohorte_id)
        if not cohorte:
            return None
        return CohorteRepository.actualizar(cohorte, data)

    @staticmethod
    def eliminar(cohorte_id: int) -> bool:
        cohorte = CohorteRepository.obtener_por_id(cohorte_id)
        if not cohorte:
            return False
        CohorteRepository.eliminar(cohorte)
        return True

    @staticmethod
    def asignar_docente(cohorte_id: int, docente_id: int, modulo_id: int, horas: int) -> AsignacionDocente | None:
        cohorte = CohorteRepository.obtener_por_id(cohorte_id)
        docente = DocenteRepository.obtener_por_id(docente_id)
        modulo = ModuloRepository.obtener_por_id(modulo_id)
        if cohorte is None or docente is None or modulo is None:
            return None
        asignacion = AsignacionDocente(
            cohorte_id=cohorte.id,
            docente_id=docente.id,
            modulo_id=modulo.id,
            horas_semanales=horas,
        )
        return CohorteRepository.asignar_docente(asignacion)
