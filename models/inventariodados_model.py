# INVENTARIO DADOS ###################################################################################
from db import db
from datetime import datetime, timezone

class InventarioDados(db.Model):
    __tablename__ = "inventariodados"
    __table_args__ = {"extend_existing": True}

    id_invtdados = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_invt = db.Column(db.Integer, db.ForeignKey('inventario.id_invt'), nullable=False)
    data_invt = db.Column(db.DateTime,db.ForeignKey('inventario.data_invt'), default=datetime.now(timezone.utc),nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'), nullable=False)
    quantidade_invtdados = db.Column(db.Numeric(10, 3))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="inventariosdados")