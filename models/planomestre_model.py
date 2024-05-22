from db import db
from datetime import datetime, timezone

class PlanoMestre(db.Model):
    __tablename__ = "planomestre"
    __table_args__ = {"extend_existing": True}
    
    
    id_pm = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_rct = db.Column(db.Integer)
    nome_rct = db.Column(db.String(75))
    class_rct = db.Column(db.String(45))
    departamento_rct = db.Column(db.String(45))
    data_pm = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    estoque_pm = db.Column(db.Integer)
    
    pedidototal_pm = db.Column(db.Integer)
    pedidokgtotal_pm = db.Column(db.Numeric(10, 3))
    
    rctnecessaria_pm = db.Column(db.Integer)
    