## IMPORTS AND CONFIGURATION ###############################

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
from flask import abort


import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:pass123@localhost/labct'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

#FORNECEDORES##################################################################################################################################

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

#MATERIAS PRIMAS##################################################################################################################################

class MateriasPrimas(db.Model):
    __tablename__ = "materiasprimas"
    __table_args__ = {"extend_existing": True}

    id_mp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_mp = db.Column(db.String(75))
    unidade_mp = db.Column(db.Enum('KG', 'UN'))
    peso_mp = db.Column(db.Numeric(10, 3))
    quantidade_mp = db.Column(db.Integer)
    custo_mp = db.Column(db.Numeric(10, 2))
    departamento_mp = db.Column(db.Enum('Carnes', 'Farinhas', 'Hortifruti', 'Mercearia', 'Misturas', 'Ovos', 'Queijos'))
    pedidomin_mp = db.Column(db.Integer)
    gastomedio_mp = db.Column(db.Numeric(10, 3))
    id_fornecedor = db.Column(db.Integer)
    nome_fornecedor = db.Column(db.String(45))

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
    nome_fornecedor = ma.auto_field()


#CLIENTES##################################################################################################################################


class Clientes(db.Model):
    __tablename__ = "clientes"
    __table_args__ = {"extend_existing": True}

    id_clt = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_clt = db.Column(db.String(45))
    cnpj_clt = db.Column(db.String(14))
    endereco_clt = db.Column(db.String(100))
    numeroende_clt = db.Column(db.String(5))
    bairro_clt = db.Column(db.String(45))
    cidade_clt = db.Column(db.String(45))
    estado_clt = db.Column(db.String(45))
    contatotel_clt = db.Column(db.String(45))
    email_clt = db.Column(db.String(75))
    responsavel_clt = db.Column(db.String(45))

class ClientesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Clientes

    id_clt = ma.auto_field()
    nome_clt = ma.auto_field()
    cnpj_clt = ma.auto_field()
    endereco_clt = ma.auto_field()
    numeroende_clt = ma.auto_field()    
    bairro_clt = ma.auto_field()
    cidade_clt = ma.auto_field()
    estado_clt = ma.auto_field()
    contatotel_clt = ma.auto_field()
    email_clt = ma.auto_field()
    responsavel_clt = ma.auto_field()


#RECEITAS##################################################################################################################################

class Receitas(db.Model):
    __tablename__ = "receitas"
    __table_args__ = {"extend_existing": True}

    id_rct = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_rct = db.Column(db.String(75))
    descricao_rct = db.Column(db.String)
    preparo_rct = db.Column(db.String)
    id_clt = db.Column(db.Integer)
    nome_clt = db.Column(db.String(45))

class ReceitasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Receitas

    id_rct = ma.auto_field()
    nome_rct = ma.auto_field()
    descricao_rct = ma.auto_field()
    preparo_rct = ma.auto_field()
    id_clt = ma.auto_field()
    nome_clt = ma.auto_field()




####################################################################################
    
class ReceitaMateriasPrimas(db.Model):
    __tablename__ = "receitamateriasprimas"
    __table_args__ = {"extend_existing": True}

    id_rct = db.Column(db.Integer, db.ForeignKey('receitas.id_rct'), primary_key=True)
    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'), primary_key=True)
    nome_mp = db.Column(db.String(75))
    quantidade = db.Column(db.Numeric(10,2))
    unidade = db.Column(db.Enum('Unidade(s)', 'Grama(s)', 'Kilogramo(s)', 'Colher(es)', 'Xícara(s)'))

class ReceitasMateriasPrimasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReceitaMateriasPrimas

    id_rct = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    quantidade = ma.auto_field()
    unidade = ma.auto_field()
    

with app.app_context():
    db.create_all()


# Custom filter to round numbers
@app.template_filter('round')
def round_filter(value):
    return round(value)

# ROUTES ########################################################################################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cleanup-fornecedores', methods=['GET'])
def cleanupFornecedor():
    with app.app_context():
        db.session.query(Fornecedores).delete()  # Delete all entries from the Entry table
        db.session.commit()
    return redirect(url_for('fornecedores'))


## FORNECEDORES ##########################################

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
    return render_template('fornecedores.html', fornecedores=serialized_data)



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
    


# MATERIAS PRIMAS ###################################

@app.route('/materiasprimas', methods=['GET', 'POST'])
def materiasPrimas():

    fornecedores = Fornecedores.query.all() #get values from fornecedores table
    fornecedor_schema = FornecedorSchema(many=True)
    serialized_data_f = fornecedor_schema.dump(fornecedores)

    if request.method == 'POST':
        id_mp = request.form.get('id_mp')
        nome_mp = request.form.get('nome_mp')
        unidade_mp = request.form.get('unidade_mp')
        peso_mp = request.form.get('peso_mp')
        quantidade_mp = request.form.get('quantidade_mp')
        custo_mp = request.form.get('custo_mp')
        departamento_mp = request.form.get('departamento_mp')
        pedidomin_mp = request.form.get('pedidomin_mp')
        gastomedio_mp = request.form.get('gastomedio_mp')
        id_fornecedor = request.form.get('id_fornecedor')

        # Fetch the nome_fornecedor corresponding to the id_fornecedor from the Fornecedor table
        fornecedor = Fornecedores.query.filter_by(id_fornecedor=id_fornecedor).first()
        nome_fornecedor = fornecedor.nome_fornecedor if fornecedor else None

        materiasprimas = MateriasPrimas(
            id_mp=id_mp, 
            nome_mp=nome_mp, 
            unidade_mp=unidade_mp,
            peso_mp=peso_mp,
            quantidade_mp=quantidade_mp,
            custo_mp=custo_mp,
            departamento_mp=departamento_mp,
            pedidomin_mp=pedidomin_mp,
            gastomedio_mp=gastomedio_mp,
            id_fornecedor=id_fornecedor,
            nome_fornecedor=nome_fornecedor
            )
        db.session.add(materiasprimas)
        db.session.commit()
        return redirect(url_for('materiasPrimas'))

    materiasprimas = MateriasPrimas.query.all()
    materiaprima_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiaprima_schema.dump(materiasprimas)
    return render_template('materiasprimas.html', fornecedores=serialized_data_f, materiasprimas = serialized_data_mp)

#DELETE
@app.route('/delete-materiaprima/<int:id>', methods=['POST'])
def deleteMateriaPrima(id):
    materiasprimas = MateriasPrimas.query.get_or_404(id)
    db.session.delete(materiasprimas)
    db.session.commit()
    return redirect(url_for('materiasPrimas', id=id) )

#EDIT
@app.route('/edit-materiaprima/<int:id>', methods=['POST'])
def editMateriaPrima(id):
    if request.method == 'POST':
        materiasprimas = MateriasPrimas.query.get_or_404(id)
        materiasprimas.nome_mp = request.form.get('nome_mp')
        materiasprimas.unidade_mp = request.form.get('unidade_mp')
        materiasprimas.peso_mp = request.form.get('peso_mp')
        materiasprimas.quantidade_mp = request.form.get('quantidade_mp')
        materiasprimas.custo_mp = request.form.get('custo_mp')
        materiasprimas.departamento_mp = request.form.get('departamento_mp')
        materiasprimas.pedidomin_mp = request.form.get('pedidomin_mp')
        materiasprimas.gastomedio_mp = request.form.get('gastomedio_mp')
        materiasprimas.id_fornecedor = request.form.get('id_fornecedor')
        
        
        db.session.commit()
        return redirect(url_for('materiasPrimas', id=id))


# CLIENTES #####################################################
    

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():

    if request.method == 'POST':
        nome_clt = request.form.get('nome_clt')
        cnpj_clt = request.form.get('cnpj_clt')
        endereco_clt = request.form.get('endereco_clt')
        numeroende_clt = request.form.get('numeroende_clt')   
        bairro_clt = request.form.get('bairro_clt')
        cidade_clt = request.form.get('cidade_clt')
        estado_clt = request.form.get('estado_clt')
        responsavel_clt = request.form.get('responsavel_clt')
        contatotel_clt = request.form.get('contatotel_clt')
        email_clt = request.form.get('email_clt')
       

        clientes = Clientes(
            
            nome_clt=nome_clt,
            cnpj_clt=cnpj_clt,
            endereco_clt=endereco_clt,
            numeroende_clt=numeroende_clt,
            bairro_clt=bairro_clt,
            cidade_clt=cidade_clt,
            estado_clt=estado_clt,
            contatotel_clt=contatotel_clt,
            email_clt=email_clt,
            responsavel_clt=responsavel_clt
        )
        db.session.add(clientes)
        db.session.commit()
        return redirect(url_for('clientes')) 

   
    clientes = Clientes.query.all()
    clientes_schema = ClientesSchema(many=True)
    serialized_data_clt = clientes_schema.dump(clientes)
    
    return render_template('clientes.html', clientes=serialized_data_clt)


#DELETE
@app.route('/delete-cliente/<int:id>', methods=['POST'])
def deleteCliente(id):
    clientes = Clientes.query.get_or_404(id)
    db.session.delete(clientes)
    db.session.commit()
    return redirect(url_for('clientes', id=id) )

#EDIT
@app.route('/edit-cliente/<int:id>', methods=['POST'])
def editCliente(id):
    if request.method == 'POST':
        clientes = Clientes.query.get_or_404(id)
        clientes.nome_clt = request.form.get('nome_clt')
        clientes.cnpj_clt = request.form.get('nome_clt')
        clientes.endereco_clt = request.form.get('endereco_clt')
        clientes.numeroende_clt = request.form.get('numeroende_clt')   
        clientes.bairro_clt = request.form.get('bairro_clt')
        clientes.cidade_clt = request.form.get('cidade_clt')
        clientes.estado_clt = request.form.get('estado_clt')
        clientes.responsavel_clt = request.form.get('responsavel_clt')
        clientes.contatotel_clt = request.form.get('contatotel_clt')
        clientes.email_clt = request.form.get('email_clt')
        
        
        db.session.commit()
        return redirect(url_for('clientes', id=id))


# RECEITAS #####################################################
    

@app.route('/receitas', methods=['GET', 'POST'])
def receitas():

    materiasprimas = MateriasPrimas.query.all()
    materiasprimas_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiasprimas_schema.dump(materiasprimas)

    clientes = Clientes.query.all()
    clientes_schema = ClientesSchema(many=True)
    serialized_data_clt = clientes_schema.dump(clientes)

    #if request
    if request.method == 'POST':
        nome_rct = request.form.get('nome_rct')
        id_clt = request.form.get('id_clt')
        descricao_rct = request.form.get('descricao_rct')
        preparo_rct = request.form.get('preparo_rct')

        # Fetch the nome_mp corresponding to the id_mp from the MP table
        cliente = Clientes.query.filter_by(id_clt=id_clt).first()
        nome_clt = cliente.nome_clt if cliente else None

        receitas = Receitas(
            nome_rct=nome_rct,
            id_clt=id_clt,
            nome_clt=nome_clt,
            descricao_rct=descricao_rct,
            preparo_rct=preparo_rct
        )

        db.session.add(receitas)
        db.session.commit()

        # Handle ingredients insertion
        ingredient_count = int(request.form.get('ingredient_count'))

        for i in range(ingredient_count):
            id_mp = request.form.get(f'id_mp_{i}')
            quantidade = request.form.get(f'quantidade_{i}')
            unidade = request.form.get(f'unidade_{i}')

            #print(quantidade)

             # Fetch the nome_mp corresponding to the id_mp from the MP table
            materiaprima = MateriasPrimas.query.filter_by(id_mp=id_mp).first()
            nome_mp = materiaprima.nome_mp if materiaprima else None

            receita_mp = ReceitaMateriasPrimas(
                id_rct=receitas.id_rct,
                id_mp=id_mp,
                nome_mp=nome_mp,
                quantidade=quantidade,
                unidade=unidade
            )
        
            db.session.add(receita_mp)
            db.session.commit()
        
        return redirect(url_for('receitas')) 
    
    receitas = Receitas.query.all()
    receitas_schema = ReceitasSchema(many=True)
    serialized_data_rct = receitas_schema.dump(receitas)

    receitasmp = ReceitaMateriasPrimas.query.all()
    receitasmp_schema = ReceitasMateriasPrimasSchema(many=True)
    serialized_data_rctmp = receitasmp_schema.dump(receitasmp)
    



    return render_template('receitas.html', 
    materiasprimas=serialized_data_mp, 
    clientes=serialized_data_clt,
    receitas=serialized_data_rct,
    receitasmp=serialized_data_rctmp)


#EDIT
@app.route('/edit-receita/<int:id>', methods=['POST'])
def editReceita(id):
    if request.method == 'POST':
        receitas = Receitas.query.get_or_404(id)
        receitas.nome_rct = request.form.get('nome_rct')
        receitas.descricao_rct = request.form.get('descricao_rct')
        receitas.preparo_rct = request.form.get('preparo_rct')
        #receitas.id_clt = request.form.get('id_clt')
        
        
        
        db.session.commit()
        return redirect(url_for('receitas', id=id))
    
#DELETE
@app.route('/delete-receita/<int:id>', methods=['POST'])
def deleteReceita(id):
    
     # Fetch the receitas record
    receitas = Receitas.query.get_or_404(id)
    
    try:
        # Delete child records from ReceitaMateriasPrimas table
        ReceitaMateriasPrimas.query.filter_by(id_rct=id).delete()
        
        # Delete the parent record from Receitas table
        db.session.delete(receitas)
        db.session.commit()
    except IntegrityError:
        # If there's an integrity error, rollback changes and abort with error message
        db.session.rollback()
        abort(500, "Cannot delete or update a parent row: a foreign key constraint fails")
    
    return redirect(url_for('receitas', id=id) )


# RUN APP ################################################

if __name__ == '__main__':

    
    app.run(debug=True)
