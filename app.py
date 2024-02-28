
import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields


import pymysql
from sqlalchemy import func
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/labct24'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)



class Fornecedores(db.Model):
    __tablename__ = "fornecedores"
    __table_args__ = {"extend_existing": True}

    id_fornecedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_fornecedor = db.Column(db.String(45))
    tempo_entrega = db.Column(db.Integer)
    prazo_pagamento = db.Column(db.Integer)
    dia_pedido = db.Column(db.Enum('Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo'))
    nome_vendedor = db.Column(db.String(45))
    contato_tel = db.Column(db.String(45))
    email_vendedor = db.Column(db.String(100))


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


class Receita(db.Model):
    __tablename__ = "receitas"
    __table_args__ = {"extend_existing": True}
   # include_relationships = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descricao_mix = db.Column(db.Text, nullable=False)
    modo_preparo = db.Column(db.Text, nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    rend_kg = db.Column(db.Float, nullable=False)
    rend_unid = db.Column(db.Float, nullable=False)
    validade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=1, nullable=True)
    cadastrado_em = db.Column(db.DateTime, nullable=False, default=func.now)
    #atualizado_em = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    # TODO relacionando Receita c/ usuario 1/1
   # usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)
    # TODO relacionando RECEITA c/ cliente N/1
   # cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
   # cliente = db.relationship("Cliente", back_populates="receitas", foreign_keys=[cliente_id])
    # TODO relacionando RECEITA c/ mixprodutos 1/1
   # mixprodutos = db.relationship("MixProduto", back_populates="receita", uselist=False, cascade="all, delete-orphan", lazy="joined", foreign_keys=MixProduto.receita_id)
    # TODO Relacionamento 1/N com a tabela PedidoProducao
   # pedidosprod = db.relationship("PedidoProducao", back_populates="receitas")


    
# Schema for serialization
class FornecedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fornecedores

    id_fornecedor = ma.auto_field()
    nome_fornecedor = ma.auto_field()
    tempo_entrega = ma.auto_field()
    prazo_pagamento = ma.auto_field()
    dia_pedido = ma.auto_field()
    nome_vendedor = ma.auto_field()
    contato_tel = ma.auto_field()
    email_vendedor = ma.auto_field()


class MateriasPrimasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MateriasPrimas

    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    peso_mp = ma.auto_field()
    quantidade_mp = ma.auto_field()
    custo_mp = ma.auto_field()
    departamento_mp = ma.auto_field()
    pedidomin_mp = ma.auto_field()
    gastomedio_mp = ma.auto_field()
    id_fornecedor = ma.auto_field()




#TODO ** Classe ReceitaSchema_Modelo ** este esquema define como os objetos da classe Receita devem ser convertidos em um formato serializado (como JSON) e vice-versa. Ele fornece uma estrutura clara para lidar com a validação e formatação de dados ao interagir com os modelos.
class ReceitasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Receita

    id = ma.auto_field()
    descricao_mix = ma.auto_field()
    modo_preparo = ma.auto_field()
    departamento = ma.auto_field()
    rend_kg = ma.auto_field()
    rend_unid = ma.auto_field()
    validade = ma.auto_field()
    status = ma.auto_field()
    cadastrado_em = ma.auto_field()
    #atualizado_em = ma.auto_field()
    #usuario = ma.auto_field()
    #cliente = ma.auto_field()
    #mixprodutos = ma.auto_field()
    #pedidosprod = ma.auto_field()


with app.app_context():
        db.create_all()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contatos')
def contatos():
    return render_template('contatos.html')




#TODO função Receitas 
@app.route('/receitas')
def receitas():

    #receitas = receitas.query.all() #get values from receitas table
    #receita_schema = ReceitasSchema(many=True)
   # serialized_data = receita_schema.dump(receitas)
    return render_template('receitas/receitas.html')

##


@app.route('/materiasprimas')
def materiasPrimas():

    fornecedores = Fornecedores.query.all() #get values from fornecedores table
    fornecedor_schema = FornecedorSchema(many=True)
    serialized_data = fornecedor_schema.dump(fornecedores)
    return render_template('materiasprimas/materiasprimas.html', fornecedores=serialized_data)


@app.route('/cleanup-fornecedores', methods=['GET'])
def cleanupFornecedor():
    with app.app_context():
        db.session.query(Fornecedores).delete()  # Delete all entries from the Entry table
        db.session.commit()
    return redirect(url_for('fornecedores'))


@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    if request.method == 'POST':
        nome_fornecedor = request.form.get('nome_fornecedor')
        tempo_entrega = request.form.get('tempo_entrega')
        prazo_pagamento = request.form.get('prazo_pagamento')
        dia_pedido = request.form.get('dia_pedido')
        nome_vendedor = request.form.get('nome_vendedor')
        contato_tel = request.form.get('contato_tel')
        email_vendedor = request.form.get('email_vendedor')
        
        fornecedores = Fornecedores(
            nome_fornecedor=nome_fornecedor, 
            tempo_entrega=tempo_entrega,
            prazo_pagamento=prazo_pagamento,
            dia_pedido=dia_pedido,
            nome_vendedor=nome_vendedor,
            contato_tel=contato_tel,
            email_vendedor=email_vendedor
            )
        db.session.add(fornecedores)
        db.session.commit()
        return redirect(url_for('fornecedores'))  # Redirect to GET request after form submission

    fornecedores = Fornecedores.query.all()
    fornecedor_schema = FornecedorSchema(many=True)
    serialized_data = fornecedor_schema.dump(fornecedores)
    return render_template('fornecedor/fornecedores.html', fornecedores=serialized_data)



@app.route('/delete-fornecedor/<int:id>', methods=['POST'])
def deleteFornecedor(id):
    fornecedores = Fornecedores.query.get_or_404(id)
    db.session.delete(fornecedores)
    db.session.commit()
    return redirect(url_for('fornecedores', id=id) )

@app.route('/edit-fornecedor/<int:id>', methods=['POST'])
def editFornecedor(id):
    if request.method == 'POST':
        fornecedores = Fornecedores.query.get_or_404(id)
        fornecedores.nome_fornecedor = request.form.get('nome_fornecedor')
        fornecedores.tempo_entrega = request.form.get('tempo_entrega')
        fornecedores.prazo_pagamento = request.form.get('prazo_pagamento')
        fornecedores.dia_pedido = request.form.get('dia_pedido')
        fornecedores.nome_vendedor = request.form.get('nome_vendedor')
        fornecedores.contato_tel = request.form.get('contato_tel')
        fornecedores.email_vendedor = request.form.get('email_vendedor')
        
        db.session.commit()
        return redirect(url_for('fornecedores', id=id))


if __name__ == '__main__':    
    app.run(debug=True)

