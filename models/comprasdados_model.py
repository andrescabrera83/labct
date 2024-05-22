# COMPRASDADOS #################################################################################################

from db import db, ma
from datetime import datetime, timezone
from sqlalchemy import ForeignKey

class ComprasDados(db.Model):
    __tablename__ = "comprasdados"
    __table_args__ = {"extend_existing": True}

    id_comprasd = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_compras = db.Column(db.Integer,  ForeignKey('compras.id_compras'))

    nome_mp = db.Column(db.String(75))
    unidade_mp = db.Column(db.Enum('KG', 'UN'))
    pedido_comprasd = db.Column(db.Numeric(10, 3))
    fornecedor_comprasd = db.Column(db.String(45))
    valorpedido_comprasd = db.Column(db.Numeric(10, 2))
    departamento_comprasd = db.Column(db.Enum('Carnes', 'Farinhas', 'Hortifruti', 'Mercearia', 'Misturas', 'Ovos', 'Queijos'))
    previsao_comprasd = db.Column(db.DateTime)
    vencimento_comprasd = db.Column(db.DateTime)
    fechado_comprasd = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="comprasdados")
    compras = db.relationship("Compras", back_populates="comprasdados")



class ComprasDadosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ComprasDados
        
    id_comprasd = ma.auto_field()
    id_compras = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    pedido_comprasd = ma.auto_field()
    fornecedor_comprasd = ma.auto_field()
    valorpedido_comprasd = ma.auto_field()
    departamento_comprasd = ma.auto_field()
    previsao_comprasd = ma.auto_field()
    vencimento_comprasd = ma.auto_field()
    fechado_comprasd = ma.auto_field()
