from db import db, ma
from datetime import datetime, timezone

class Produc(db.Model):
    __tablename__ = "produc"
    __table_args__ = {"extend_existing": True}

    id_pdc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_pdc = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    estado_pdc = db.Column(db.Enum('Pendente', 'Fechado'))
    nome_rct = db.Column(db.String(75))   
    filial_pdc = db.Column(db.Integer) 
    nomefilial_pdc = db.Column(db.String(50))
    departamento_rct = db.Column(db.String(45))
    class_rct = db.Column(db.String(45))
    pedidomin_rct = db.Column(db.Integer)
    fechadoem_pdc = db.Column(db.DateTime, default=datetime.now(timezone.utc)) 
    quantidade_pdc = db.Column(db.Integer)

    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="produc")
    producdados = db.relationship("ProducDados", back_populates="produc")
    

