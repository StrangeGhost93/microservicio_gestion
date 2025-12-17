from dataclasses import dataclass

from app import db


@dataclass(init=False, repr=True, eq=True)
class Especialidad(db.Model):
    __tablename__ = "especialidades"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    especialidad: str = db.Column(db.String(120), nullable=False)
    facultad: str = db.Column(db.String(120), nullable=False)
    universidad: str = db.Column(db.String(120), nullable=False)

    def __init__(self, especialidad: str, facultad: str, universidad: str):
        self.especialidad = especialidad
        self.facultad = facultad
        self.universidad = universidad