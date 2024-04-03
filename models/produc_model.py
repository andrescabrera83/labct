from db import db
from datetime import datetime, timezone

class Produc(db.Model):
    __tablename__ = "produc"
    __table_args__ = {"extend_existing": True}

    id_pdc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_pdc = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    estado_pdc = db.Column(db.Enum('Pendente', 'Fechado'))

    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="produc")
    producdados = db.relationship("ProducDados", back_populates="produc")
