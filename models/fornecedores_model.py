#FORNECEDORES##################################################################################################################################

from db import db, ma

class Fornecedores(db.Model):
    __tablename__ = "fornecedores"
    __table_args__ = {"extend_existing": True}

    id_fornecedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_fornecedor = db.Column(db.String(45))
    tempo_entrega = db.Column(db.Integer)
    prazo_pagamento = db.Column(db.Integer)
    dia_pedido = db.Column(db.Enum('Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo'))
    nome_vendedor = db.Column(db.String(45))
    contato_tel = db.Column(db.String(45))
    email_vendedor = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="fornecedores")
    
    
class FornecedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fornecedores

    id_fornecedor = ma.auto_field()
    nome_fornecedor = ma.auto_field()
    tempo_entrega = ma.auto_field()
    prazo_pagamento = ma.auto_field()
    dia_pedido = ma.auto_field()
    nome_vendedor = ma.auto_field()
    contato_tel = ma.auto_field()
    email_vendedor = ma.auto_field()