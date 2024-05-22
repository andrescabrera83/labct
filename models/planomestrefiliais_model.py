from db import db

class PlanoMestreFiliais(db.Model):
    __tablename__ = "planomestrefiliais"
    __table_args__ = {"extend_existing": True}
    
    id_pmf = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pm = db.Column(db.Integer)
    filial_pdc = db.Column(db.Integer) 
    nomefilial_pdc = db.Column(db.String(50))
    
    quantidade_pdc = db.Column(db.Integer)
    
    