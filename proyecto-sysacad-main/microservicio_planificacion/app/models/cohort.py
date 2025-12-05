from dataclasses import dataclass

from flask_hashids import HashidMixin

from app.extensions import db


@dataclass
class Cohorte(HashidMixin, db.Model):
    __tablename__ = "cohortes"

    id: int = db.Column(db.Integer, primary_key=True)
    anio: int = db.Column(db.SmallInteger, nullable=False)
    campus: str = db.Column(db.String(80), nullable=False)
    modalidad: str = db.Column(db.String(40), nullable=False)
    cupo: int = db.Column(db.Integer, nullable=False)
    fecha_inicio: str = db.Column(db.String(20), nullable=False)
    fecha_fin: str = db.Column(db.String(20), nullable=True)
    estado: str = db.Column(db.String(20), nullable=False, default="planificada")

    programa_id: int = db.Column(
        db.Integer, db.ForeignKey("programas.id", ondelete="CASCADE"), nullable=False
    )
    programa = db.relationship("Programa", back_populates="cohortes")

    asignaciones = db.relationship(
        "AsignacionDocente",
        back_populates="cohorte",
        cascade="all, delete-orphan",
    )
