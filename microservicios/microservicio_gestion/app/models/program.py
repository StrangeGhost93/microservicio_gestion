from dataclasses import dataclass

from flask_hashids import HashidMixin

from app.extensions import db


@dataclass
class Programa(HashidMixin, db.Model):
    __tablename__ = "programas"

    id: int = db.Column(db.Integer, primary_key=True)
    nombre: str = db.Column(db.String(120), nullable=False)
    version: str = db.Column(db.String(40), nullable=False)
    modalidad: str = db.Column(db.String(40), nullable=False)
    descripcion: str = db.Column(db.Text, nullable=True)
    duracion_meses: int = db.Column(db.Integer, nullable=False, default=12)
    creditos_totales: int = db.Column(db.Integer, nullable=False, default=0)
    vigente: bool = db.Column(db.Boolean, default=True, nullable=False)

    modulos = db.relationship(
        "Modulo",
        back_populates="programa",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    cohortes = db.relationship(
        "Cohorte",
        back_populates="programa",
        cascade="all, delete-orphan",
    )
