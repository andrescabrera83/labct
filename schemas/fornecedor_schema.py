from app import ma
from models import fornecedor_model

# Schema for serialization
class FornecedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = fornecedor_model.Fornecedores

    id_fornecedor = ma.auto_field()
    nome_fornecedor = ma.auto_field()
    tempo_entrega = ma.auto_field()
    prazo_pagamento = ma.auto_field()
    dia_pedido = ma.auto_field()
    nome_vendedor = ma.auto_field()
    contato_tel = ma.auto_field()
    email_vendedor = ma.auto_field()

