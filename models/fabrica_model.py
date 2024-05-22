from db import db, ma
from datetime import datetime, timezone
from sqlalchemy import func

class Fabrica(db.Model):
    __tablename__ = "fabrica"
    __table_args__ = {"extend_existing": True}  # indica que a tabela deve ser estendida se ela já existir no banco de dados.
    
    id_fab = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome_fab = db.Column(db.String(150), nullable=False)
    endereco_fab = db.Column(db.String(150), nullable=False)
    bairro_fab = db.Column(db.String(50), nullable=False)
    cidade_fab = db.Column(db.String(50), nullable=False)
    estado_fab = db.Column(db.String(50), nullable=False)
    telefone_fab = db.Column(db.String(30), nullable=False)
    email_fab = db.Column(db.String(50), nullable=False)
    responsavel_fab = db.Column(db.String(50), nullable=False)
    wpp_fab = db.Column(db.String(50), nullable=False)
    cnpj_fab = db.Column(db.String(17), nullable=True)
    status_fab = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em_fab = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    atualizado_em_fab = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    

class FabricaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabrica
        
    id_fab = ma.auto_field()
    nome_fab = ma.auto_field()
    endereco_fab = ma.auto_field()
    bairro_fab = ma.auto_field()
    cidade_fab = ma.auto_field()
    estado_fab = ma.auto_field()
    telefone_fab = ma.auto_field()
    email_fab = ma.auto_field()
    responsavel_fab = ma.auto_field()
    wpp_fab = ma.auto_field()
    cnpj_fab = ma.auto_field()
    status_fab = ma.auto_field()
    cadastrado_em_fab = ma.auto_field()
    atualizado_em_fab = ma.auto_field()
