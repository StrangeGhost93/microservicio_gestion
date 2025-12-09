from dataclasses import dataclass

from app.extensions import db


@dataclass
class Docente(db.Model):
    __tablename__ = "docentes"

    id: int = db.Column(db.Integer, primary_key=True)
    nombre: str = db.Column(db.String(80), nullable=False)
    apellido: str = db.Column(db.String(80), nullable=False)
    email: str = db.Column(db.String(120), nullable=False, unique=True)
    especialidad: str = db.Column(db.String(120), nullable=True)
    horas_disponibles: int = db.Column(db.SmallInteger, nullable=False, default=10)

    asignaciones = db.relationship("AsignacionDocente", back_populates="docente")
