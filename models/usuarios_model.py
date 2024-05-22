from db import db,ma
from flask_login import UserMixin

# USERS #################################################################################################

class Usuarios(UserMixin,db.Model):

    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('admin','master'), nullable=False)
    nomecompleto = db.Column(db.String(100), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    materias_primas = db.relationship('MateriasPrimas', back_populates="usuarios" , lazy=True)
    fornecedores = db.relationship('Fornecedores', back_populates="usuarios" , lazy=True)
    estoque = db.relationship('Estoque', back_populates="usuarios" , lazy=True)
    historico = db.relationship('Historico', back_populates="usuarios", lazy=True)
    inventario = db.relationship('Inventario', back_populates="usuarios", lazy=True)
    inventariosdados = db.relationship('InventarioDados', back_populates="usuarios", lazy=True)
    compras = db.relationship('Compras', back_populates="usuarios", lazy=True)
    comprasdados = db.relationship('ComprasDados', back_populates="usuarios", lazy=True)
    receitas = db.relationship('Receitas', back_populates="usuarios", lazy=True)
    receitasmateriasprimas = db.relationship('ReceitaMateriasPrimas', back_populates="usuarios", lazy=True)
    config = db.relationship('Config', back_populates="usuarios", lazy=True)
    produc = db.relationship('Produc', back_populates="usuarios", lazy=True)
    producdados = db.relationship('ProducDados', back_populates="usuarios", lazy=True)
    filiais = db.relationship('Filiais', back_populates="usuarios", lazy=True)
    

class UsuariosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuarios
        
    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    role = ma.auto_field()
    nomecompleto = ma.auto_field()
    funcao = ma.auto_field()
    whatsapp = ma.auto_field()
    cpf = ma.auto_field()
    email = ma.auto_field()