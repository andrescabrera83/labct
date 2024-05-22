#RECEITAS##################################################################################################################################
from db import db, ma

class Receitas(db.Model):
    __tablename__ = "receitas"
    __table_args__ = {"extend_existing": True}

    id_rct = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_rct = db.Column(db.String(75))
    descricao_rct = db.Column(db.Text)
    preparo_rct = db.Column(db.Text)
    rendimento_rct = db.Column(db.Integer)
    class_rct = db.Column(db.String(45))
    departamento_rct = db.Column(db.String(45))
    validade_rct = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    rendimentokg_rct = db.Column(db.Numeric(10, 3))
    unidadeporkg_rct = db.Column(db.Integer)
    pedidomin_rct = db.Column(db.Integer)

    usuarios = db.relationship("Usuarios", back_populates="receitas")
    receitasmateriasprimas = db.relationship("ReceitaMateriasPrimas", back_populates="receitas")
    #producdados = db.relationship("ProducDados", back_populates="receitas")
    
class ReceitasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Receitas

    id_rct = ma.auto_field()
    nome_rct = ma.auto_field()
    descricao_rct = ma.auto_field()
    preparo_rct = ma.auto_field()
    rendimento_rct = ma.auto_field()
    rendimentokg_rct = ma.auto_field()
    class_rct = ma.auto_field()
    departamento_rct = ma.auto_field()
    validade_rct = ma.auto_field()
    unidadeporkg_rct = ma.auto_field()
    pedidomin_rct = ma.auto_field()
    
