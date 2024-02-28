from app import ma
from models import materiaaprimas_model


class MateriasPrimasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = materiaaprimas_model.MateriasPrimas

    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    peso_mp = ma.auto_field()
    quantidade_mp = ma.auto_field()
    custo_mp = ma.auto_field()
    departamento_mp = ma.auto_field()
    pedidomin_mp = ma.auto_field()
    gastomedio_mp = ma.auto_field()
    id_fornecedor = ma.auto_field()


