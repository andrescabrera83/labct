from db import db


class ProducDados(db.Model):
    __tablename__ = "producdados"
    __table_args__ = {"extend_existing": True}

    id_pdcd = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pdc = db.Column(db.Integer, db.ForeignKey('produc.id_pdc'), nullable=False)
    id_rct = db.Column(db.Integer, db.ForeignKey('receitas.id_rct'), nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'), nullable=False)
    nome_mp = db.Column(db.String(75))
    quantidade_pdcd = db.Column(db.Numeric(10,3))
    unidade_pdcd = db.Column(db.Enum('KG', 'UN'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="producdados")
    #receitas = db.relationship("Receitas", back_populates="producdados")
    #materias_primas = db.relationship("MateriasPrimas", back_populates="producdados")
    produc = db.relationship("Produc", back_populates="producdados")