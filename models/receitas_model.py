#RECEITAS##################################################################################################################################
from db import db, ma

class Receitas(db.Model):
    __tablename__ = "receitas"
    __table_args__ = {"extend_existing": True}

    id_rct = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_rct = db.Column(db.String(75))
    cod_rct = db.Column(db.String(10))
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
    
    estoque_rct = db.Column(db.Integer)
    
    contador_rct = db.Column(db.Integer)

    usuarios = db.relationship("Usuarios", back_populates="receitas")
    receitasmateriasprimas = db.relationship("ReceitaMateriasPrimas", back_populates="receitas")
    #producdados = db.relationship("ProducDados", back_populates="receitas")
