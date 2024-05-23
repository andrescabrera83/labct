from db import db, ma

class Filiais(db.Model):
    __tablename__ = "filiais"
    __table_args__ = {"extend_existing": True}
    
    id_fil = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loja_fil = db.Column(db.String(50), nullable=False)
    endereco_fil = db.Column(db.String(50), nullable=False)
    bairro_fil = db.Column(db.String(50), nullable=False)
    cidade_fil = db.Column(db.String(50), nullable=False)
    codigorota_fil = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuarios = db.relationship("Usuarios", back_populates="filiais")
    
