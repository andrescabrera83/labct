from db import db, ma
from flask_login import UserMixin

#TODO - Rotas #################################################################################################

class Rotas(UserMixin,db.Model):

    __tablename__ = "rotas"
    __table_args__ = {"extend_existing": True}
    
    id_rota = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    veiculo = db.Column(db.String(20), nullable=False)
    placa = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(15), nullable=False)
    whatsapp = db.Column(db.String(50), nullable=False)

    #filiais = db.relationship('Filiais', back_populates="rotas", lazy=True)
    
    

        