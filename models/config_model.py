# Model for storing configuration settings
from db import db

class Config(db.Model):
    __tablename__ = "giromedio"
    __table_args__ = {"extend_existing": True}
    id_gm = db.Column(db.Integer, primary_key=True)
    giro_medio = db.Column(db.Integer, default=6)

    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship('Usuarios', back_populates="config", lazy=True)

