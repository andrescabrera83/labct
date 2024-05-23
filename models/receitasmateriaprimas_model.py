####################################################################################
from db import db, ma

class ReceitaMateriasPrimas(db.Model):
    __tablename__ = "receitamateriasprimas"
    __table_args__ = {"extend_existing": True}

    id_rctmp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_rct = db.Column(db.Integer, db.ForeignKey('receitas.id_rct'))
    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'))
    nome_mp = db.Column(db.String(75))
    quantidade = db.Column(db.Numeric(10,3))
    unidade = db.Column(db.Enum('KG', 'UN'))
    tipo_rctmp = db.Column(db.Enum('Ingrediente', 'Embalagem'))
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="receitasmateriasprimas")
    materias_primas = db.relationship("MateriasPrimas", back_populates="receitasmateriasprimas")
    receitas = db.relationship("Receitas", back_populates="receitasmateriasprimas")

