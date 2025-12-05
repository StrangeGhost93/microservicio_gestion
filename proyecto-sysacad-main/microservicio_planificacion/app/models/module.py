from dataclasses import dataclass

from flask_hashids import HashidMixin

from app.extensions import db


@dataclass
class Modulo(HashidMixin, db.Model):
    __tablename__ = "modulos"

    id: int = db.Column(db.Integer, primary_key=True)
    titulo: str = db.Column(db.String(120), nullable=False)
    duracion_semanas: int = db.Column(db.SmallInteger, nullable=False)
    creditos: int = db.Column(db.SmallInteger, nullable=False, default=0)
    resultados: str = db.Column(db.Text, nullable=True)

    programa_id: int = db.Column(
        db.Integer, db.ForeignKey("programas.id", ondelete="CASCADE"), nullable=False
    )
    programa = db.relationship("Programa", back_populates="modulos")
