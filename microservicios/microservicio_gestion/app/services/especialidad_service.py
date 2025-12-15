"""Servicio en memoria para mockear especialidades."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Mapping

# Fuente liviana de datos sintéticos para simular la API pedida
_ESPECIALIDADES: list[Mapping[str, object]] = [
    {"id": 1, "especialidad": "Ingenieria en Sistemas", "facultad": "Facultad de Ingenieria", "universidad": "UNL"},
    {"id": 2, "especialidad": "Administracion de Empresas", "facultad": "Ciencias Economicas", "universidad": "UBA"},
    {"id": 3, "especialidad": "Medicina", "facultad": "Ciencias Medicas", "universidad": "UNC"},
    {"id": 4, "especialidad": "Arquitectura", "facultad": "Arquitectura y Urbanismo", "universidad": "UTN"},
    {"id": 5, "especialidad": "Derecho", "facultad": "Ciencias Juridicas", "universidad": "UNR"},
    {"id": 6, "especialidad": "Psicologia", "facultad": "Humanidades", "universidad": "UNLP"},
    {"id": 7, "especialidad": "Biotecnologia", "facultad": "Ciencias Exactas", "universidad": "UNC"},
    {"id": 8, "especialidad": "Diseno Grafico", "facultad": "Artes", "universidad": "UNA"},
]


class EspecialidadService:
    """Fachada sin estado para especialidades mockeadas."""

    @staticmethod
    def listar() -> Sequence[Mapping[str, object]]:
        """Devolver todas las especialidades disponibles."""
        return _ESPECIALIDADES

    @staticmethod
    def obtener(especialidad_id: int) -> Mapping[str, object] | None:
        """Buscar una especialidad por ID dentro del mock."""
        return next((esp for esp in _ESPECIALIDADES if esp["id"] == especialidad_id), None)
