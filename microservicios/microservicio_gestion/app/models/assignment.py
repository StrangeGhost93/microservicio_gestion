from dataclasses import dataclass

from app.extensions import db


@dataclass
class AsignacionDocente(db.Model):
    __tablename__ = "asignaciones_docentes"

    id: int = db.Column(db.Integer, primary_key=True)
    horas_semanales: int = db.Column(db.SmallInteger, nullable=False, default=4)

    docente_id: int = db.Column(
        db.Integer,
        db.ForeignKey("docentes.id", ondelete="CASCADE"),
        nullable=False,
    )
    modulo_id: int = db.Column(
        db.Integer,
        db.ForeignKey("modulos.id", ondelete="CASCADE"),
        nullable=False,
    )
    cohorte_id: int = db.Column(
        db.Integer,
        db.ForeignKey("cohortes.id", ondelete="CASCADE"),
        nullable=False,
    )

    docente = db.relationship("Docente", back_populates="asignaciones")
    modulo = db.relationship("Modulo")
    cohorte = db.relationship("Cohorte", back_populates="asignaciones")
