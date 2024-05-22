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
    
    
class FiliaisSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Filiais
    
    id_fil = ma.auto_field()
    loja_fil = ma.auto_field()
    endereco_fil = ma.auto_field()
    bairro_fil = ma.auto_field()
    cidade_fil = ma.auto_field()
    codigorota_fil = ma.auto_field()
     