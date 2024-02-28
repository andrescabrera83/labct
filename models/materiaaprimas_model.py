from app import db



class MateriasPrimas(db.Model):
    __tablename__ = "materiasprimas"
    __table_args__ = {"extend_existing": True}

    id_mp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_mp = db.Column(db.String(45))
    unidade_mp = db.Column(db.Enum('KG', 'UN'))
    peso_mp = db.Column(db.Numeric(10, 3))
    quantidade_mp = db.Column(db.Integer)
    custo_mp = db.Column(db.Numeric(10, 3))
    departamento_mp = db.Column(db.Enum('Carnes', 'Farinhas', 'Hortifruti', 'Mercearia', 'Misturas', 'Ovos', 'Queijos'))
    pedidomin_mp = db.Column(db.Integer)
    gastomedio_mp = db.Column(db.Numeric(10, 3))
    id_fornecedor = db.Column(db.Integer)

