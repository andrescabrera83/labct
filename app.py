## IMPORTS AND CONFIGURATION ###############################

from flask import Flask, render_template, request, redirect, url_for, session, g, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship
import pymysql
import os
from datetime import datetime
from datetime import timedelta
#from datetime import datetime, timedelta, timezone
from babel.dates import format_date
from flask import abort  # Import abort function from Flask to handle HTTP errors
from sqlalchemy.exc import IntegrityError
import math
from sqlalchemy import func


from decimal import Decimal

#from models.materiasprimas import MateriasPrimas
from db import db, ma, app

from models.materiasprimas_model import MateriasPrimas
from models.estoque_model import Estoque

from models.fornecedores_model import Fornecedores
from models.historico_model import Historico
from models.inventario_model import Inventario
from models.inventariodados_model import InventarioDados
from models.compras_model import Compras
from models.comprasdados_model import ComprasDados
from models.usuarios_model import Usuarios
from models.config_model import Config
from models.receitas_model import Receitas
from models.receitasmateriaprimas_model import ReceitaMateriasPrimas
from models.produc_model import Produc
from models.producdados_model import ProducDados
from models.fabrica_model import Fabrica
from models.filiais_model import Filiais
from models.rotas_model import Rotas
from models.planomestre_model import PlanoMestre
from models.planomestrefiliais_model import PlanoMestreFiliais





from flask_login import UserMixin,current_user, login_required, LoginManager, login_user
pymysql.install_as_MySQLdb()


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


####################################################################### APP ###################################################################################################
    
with app.app_context():
    db.create_all()
## MODELS AND SCHEMAS ###########################################################################################################################

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
    pesounitario_mp = ma.auto_field()
    pesototal_mp = ma.auto_field()
    custo_mp = ma.auto_field()
    custoemkg_mp = ma.auto_field()
    departamento_mp = ma.auto_field()
    pedidomin_mp = ma.auto_field()
    gastomedio_mp = ma.auto_field()
    gms_mp = ma.auto_field()

class EstoqueSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Estoque
        
    id_estq = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    quantidade_estq = ma.auto_field()
    gms_mp = ma.auto_field()
    pedidomin_mp = ma.auto_field()

class HistoricoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Historico
        
    id_hst = ma.auto_field() 
    date_change = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    ultimaquantidade_hst = ma.auto_field()
    novaquantidade_hst = ma.auto_field()
    difference_hst = ma.auto_field()
    modo_hst = ma.auto_field()

class InventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventario
        
    id_invt = ma.auto_field()
    estado_invt = ma.auto_field()
    data_invt = ma.auto_field()
 
class InventarioDadosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = InventarioDados
        
    id_invtdados = ma.auto_field()
    id_invt = ma.auto_field()
    data_invt = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    quantidade_invtdados = ma.auto_field()   
    quantidade_estq = ma.auto_field()   

class ComprasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Compras
        
    id_compras = ma.auto_field()
    estado_compras = ma.auto_field()
    data_compras = ma.auto_field()   

class ComprasDadosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ComprasDados
        
    id_comprasd = ma.auto_field()
    id_compras = ma.auto_field()
    nome_mp = ma.auto_field()
    unidade_mp = ma.auto_field()
    pedido_comprasd = ma.auto_field()
    fornecedor_comprasd = ma.auto_field()
    valorpedido_comprasd = ma.auto_field()
    departamento_comprasd = ma.auto_field()
    previsao_comprasd = ma.auto_field()
    vencimento_comprasd = ma.auto_field()
    fechado_comprasd = ma.auto_field()

class ReceitasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Receitas

    id_rct = ma.auto_field()
    nome_rct = ma.auto_field()
    descricao_rct = ma.auto_field()
    preparo_rct = ma.auto_field()
    rendimento_rct = ma.auto_field()
    rendimentokg_rct = ma.auto_field()
    class_rct = ma.auto_field()
    departamento_rct = ma.auto_field()
    validade_rct = ma.auto_field()
    unidadeporkg_rct = ma.auto_field()
    pedidomin_rct = ma.auto_field()
    contador_rct = ma.auto_field()
    estoque_rct = ma.auto_field()

class ReceitasMateriasPrimasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReceitaMateriasPrimas

    id_rctmp = ma.auto_field()
    id_rct = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    quantidade = ma.auto_field()
    tipo_rctmp = ma.auto_field()
    unidade = ma.auto_field()

class ProducSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Produc

    id_pdc = ma.auto_field()
    data_pdc = ma.auto_field()
    estado_pdc = ma.auto_field()
    nome_rct = ma.auto_field()
    filial_pdc = ma.auto_field()
    nomefilial_pdc = ma.auto_field()
    departamento_rct = ma.auto_field()
    class_rct = ma.auto_field()
    pedidomin_rct = ma.auto_field()
    fechadoem_pdc = ma.auto_field()
    quantidade_pdc = ma.auto_field()
    
class ProducDadosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProducDados

    id_pdcd = ma.auto_field()
    id_pdc = ma.auto_field()
    id_rct = ma.auto_field()
    id_mp = ma.auto_field()
    nome_mp = ma.auto_field()
    quantidade_pdcd = ma.auto_field()
    unidade_pdcd = ma.auto_field()
    
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
    
class FiliaisSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Filiais
    
    id_fil = ma.auto_field()
    loja_fil = ma.auto_field()
    endereco_fil = ma.auto_field()
    bairro_fil = ma.auto_field()
    cidade_fil = ma.auto_field()
    codigorota_fil = ma.auto_field()
    
    
class RotasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Rotas
    
    id_rota = ma.auto_field()
    nome = ma.auto_field()
    veiculo = ma.auto_field()
    placa = ma.auto_field()
    horario = ma.auto_field()
   # filiais = ma.auto_field()
    whatsapp = ma.auto_field()
    

class PlanoMestreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PlanoMestre
        
    id_pm = ma.auto_field()
    codigo_rct = ma.auto_field()
    nome_rct = ma.auto_field()
    class_rct = ma.auto_field()
    departamento_rct = ma.auto_field()
    data_pm = ma.auto_field()
    estoque_pm = ma.auto_field() 
    pedidototal_pm = ma.auto_field()
    pedidokgtotal_pm = ma.auto_field()
    rctnecessaria_pm = ma.auto_field()

# FUNCOES DO GIRO MEDIO ########################################################################################################

def some_function(giro_medio):
    config = Config.query.filter_by(giro_medio=giro_medio).first()

    # Create or update configuration settings
def update_config(new_value):
    config = Config.query.first()
    if config:
        config.giro_medio = new_value
    else:
        config = Config(giro_medio=new_value,user_id=current_user.id)
        db.session.add(config)
    db.session.commit()
    
# Route to update the GM ###############
    
@app.route('/giromedio', methods=['POST'])
def update():
    new_value = int(request.form['new_value'])
    update_config(new_value)

    materiaprima = MateriasPrimas.query.filter_by(user_id=current_user.id).all()

    for mp in materiaprima:
        if mp.gastomedio_mp is not None:
            gm_float = float(mp.gastomedio_mp)
            new_value_float = float(new_value)

            new_gm = gm_float * new_value_float

            mp.gms_mp = new_gm  # Update the gms_mp column of the existing MateriasPrimas object


    db.session.commit()


    return redirect(url_for('materiasPrimas'))

# Custom filter to round numbers
@app.template_filter('giromedio')
def round_filter(value):
    config = Config.query.first()
    if config:
        return value * config.giro_medio
    else:
        return value * 6  # Default value if not found

#################################################################################################################################

# ROUTES ########################################################################################################################

@login_manager.user_loader
def user_loader(user_id):
    return Usuarios.query.get(int(user_id))

@app.route('/')
def index():
    
    if 'username' in session:
        return render_template('inventario.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nomecompleto = request.form['nomecompleto']
        funcao = request.form['funcao']
        whatsapp = request.form['whatsapp']
        email = request.form['email']
        cpf = request.form['cpf']
        
        username = request.form['username']
        password = request.form['password']
        
        gm = 6
        role = 'master'
        
        user = Usuarios(
            nomecompleto=nomecompleto,
            funcao=funcao,
            whatsapp=whatsapp,
            email=email,
            cpf=cpf,
            role=role,
            username=username, 
            password=password)
        db.session.add(user)
        db.session.commit()
        
        config = Config(giro_medio=gm, user_id=user.id)
        db.session.add(config)
        db.session.commit()
        
        return redirect(url_for('usuarios'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if 'username' in session:  # Check if the user is already logged in
        return redirect(url_for('inventario'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next_url = request.form.get("next")

      

        user = Usuarios.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id 
            login_user(user)

            
            # Redirect to the originally requested URL if available, or else redirect to the index route
            next_page = request.args.get('next')  # Get the 'next' parameter from the request URL
            return redirect(next_page or url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/cleanup-fornecedores', methods=['GET'])
def cleanupFornecedor():
    with app.app_context():
        db.session.query(Fornecedores).delete()  # Delete all entries from the Entry table
        db.session.commit()
    return redirect(url_for('fornecedores'))

@app.route('/cleanup-mp', methods=['GET'])
def cleanupMP():
    with app.app_context():
        db.session.query(MateriasPrimas).delete()  # Delete all entries from the Entry table
        db.session.commit()
    return redirect(url_for('materiasprimas'))

# Define a function to provide global context variables
def global_context():
    # Check if 'username' is in the session
    if 'username' in session:
        # Retrieve the username from the session
        username_in_session = session.get('username')

        # Query the database for the user
        user = Usuarios.query.filter_by(username=username_in_session).first()
        if user:
            role = user.role

            # Return the variables to be available globally
            return {
                'username': username_in_session,
                'role': role,
            }
    # Return empty if 'username' is not in session or user not found
    return {}

# Register the global context processor
@app.context_processor
def inject_global_context():
    return global_context()

## PERFIL ###########################################################################

@app.route('/perfil')
@login_required
def perfil():
    
    return render_template('perfil.html')


## FILIAIS ###################################################################

@app.route('/filiais', methods=['GET', 'POST'])
@login_required
def filiais():
    
    if request.method == 'POST':
        loja_fil = request.form.get('loja_fil')
        endereco_fil = request.form.get('endereco_fil')
        bairro_fil = request.form.get('bairro_fil')
        cidade_fil = request.form.get('cidade_fil')
        
        codigorota = 1
        
        
        filiais = Filiais(
            loja_fil=loja_fil,
            endereco_fil=endereco_fil,
            bairro_fil=bairro_fil,
            cidade_fil=cidade_fil,
            codigorota_fil=codigorota,
            user_id=current_user.id 
        )
        
        
        
        db.session.add(filiais)
        db.session.commit()
        return redirect(url_for('filiais'))
    
    filiais = Filiais.query.all()
    filiais_schema = FiliaisSchema(many=True)
    serialized_filiais = filiais_schema.dump(filiais)
    
    return render_template('filiais.html', filiais=serialized_filiais)

## Usuarios #############################################################

@app.route('/usuarios')
@login_required
def usuarios():
    usuarios = Usuarios.query.all()
    usuarios_schema = UsuariosSchema(many=True)
    usuarios_serialized = usuarios_schema.dump(usuarios)
    return render_template('usuarios.html', usuarios=usuarios_serialized)




## Usuarios #############################################################

@app.route('/rotas', methods=['GET', 'POST'])
@login_required
def rotas():
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        veiculo = request.form.get('veiculo')
        placa = request.form.get('placa')
        horario = request.form.get('horario')
        whatsapp = request.form.get('whatsapp')
        
        rotas = Rotas(
            nome=nome,
            veiculo=veiculo,
            placa=placa,
            horario=horario,
            whatsapp=whatsapp
        )
        
        db.session.add(rotas)
        db.session.commit()
        return redirect(url_for('rotas'))
        
    
    rotas = Rotas.query.all()
    rotas_schema = RotasSchema(many=True)
    rotas_serialized = rotas_schema.dump(rotas)
    return render_template('rotas.html', rotas=rotas_serialized)




## FABRICAS ############################################################################

@app.route('/fabricas', methods=['GET', 'POST'])
@login_required
def fabricas():
    if request.method == 'POST':
        
        nome_fab = request.form.get('nome_fab')
        cnpj_fab = request.form.get('cnpj_fab')
        endereco_fab = request.form.get('endereco_fab')
        bairro_fab = request.form.get('bairro_fab')
        cidade_fab = request.form.get('cidade_fab')
        estado_fab = request.form.get('estado_fab')
        telefone_fab = request.form.get('telefone_fab')
        email_fab = request.form.get('email_fab')
        responsavel_fab = request.form.get('responsavel_fab')
        wpp_fab = request.form.get('wpp_fab')
        
        
        status = 1
        created_at = datetime.now()
        modified_at = datetime.now()
        
        fabrica = Fabrica(
            nome_fab=nome_fab,
            endereco_fab=endereco_fab,
            bairro_fab=bairro_fab,
            cidade_fab=cidade_fab,
            estado_fab=estado_fab,
            telefone_fab=telefone_fab,
            email_fab=email_fab,
            responsavel_fab=responsavel_fab,
            wpp_fab=wpp_fab,
            cnpj_fab=cnpj_fab,
            status_fab=status,
            cadastrado_em_fab=created_at,
            atualizado_em_fab=modified_at
        )
        
        db.session.add(fabrica)
        db.session.commit()
        return redirect(url_for('fabricas'))
        
    fabricas = Fabrica.query.all()
    fabricas_schema = FabricaSchema(many=True)
    serialized_fabrica = fabricas_schema.dump(fabricas)
    
        
    return render_template('fabricas.html', fabricas=serialized_fabrica)

@app.route('/edit-fabrica/<int:id>', methods=['POST'])
def editFabrica(id):
    if request.method == 'POST':
        fabricas = Fabrica.query.get_or_404(id)
        fabricas.nome_fab = request.form.get('nome_fab')
        fabricas.cnpj_fab = request.form.get('cnpj_fab')
        fabricas.endereco_fab = request.form.get('endereco_fab')
        fabricas.bairro_fab = request.form.get('bairro_fab')
        fabricas.cidade_fab = request.form.get('cidade_fab')
        fabricas.estado_fab = request.form.get('estado_fab')
        fabricas.telefone_fab = request.form.get('telefone_fab')
        fabricas.email_fab = request.form.get('email_fab')
        fabricas.responsavel_fab = request.form.get('responsavel_fab')
        fabricas.wpp_fab = request.form.get('wpp_fab')
        
        db.session.commit()
        return redirect(url_for('fabricas', id=id))

@app.route('/delete-fabrica/<int:id>', methods=['POST'])
def deleteFabrica(id):
    fabricas = Fabrica.query.get_or_404(id)
    db.session.delete(fabricas)
    db.session.commit()
    return redirect(url_for('fabricas', id=id) )
    

## FORNECEDORES ##########################################

@app.route('/fornecedores', methods=['GET', 'POST'])
@login_required
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
            email_vendedor=email_vendedor,
            user_id=current_user.id 
            )
        db.session.add(fornecedores)
        db.session.commit()
        return redirect(url_for('fornecedores'))  # Redirect to GET request after form submission

    
    fornecedores = Fornecedores.query.filter_by(user_id=current_user.id).all()
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
@login_required
def materiasPrimas():

    
    #giro medio
    config = Config.query.filter_by(user_id=current_user.id).first()
    giromedio = config.giro_medio if config else 6

    print(giromedio)

    cost_per_unit = 2
    if request.method == 'POST':
        #id_mp = request.form.get('id_mp')
        nome_mp = request.form.get('nome_mp')
        unidade_mp = request.form.get('unidade_mp')
        pesounitario_mp = request.form.get('pesounitario_mp')
        pesototal_mp = request.form.get('pesototal_mp')
        custo_mp = request.form.get('custo_mp')
        departamento_mp = request.form.get('departamento_mp')
        pedidomin_mp = request.form.get('pedidomin_mp')
        gastomedio_mp = request.form.get('gastomedio_mp')


        
        # Convert to floats
        custo_mp_float = Decimal(custo_mp)
        pesototal_mp_float =Decimal(pesototal_mp)
        gastomedio_mp_float = Decimal(gastomedio_mp)
        giromedio_float =Decimal(giromedio)

        

        gmps = gastomedio_mp_float * giromedio_float

        # Perform the division operation
        if pesototal_mp_float != 0:  # Avoid division by zero
            cost_per_unit = custo_mp_float / pesototal_mp_float

        materiasprimas = MateriasPrimas( 
            nome_mp=nome_mp, 
            unidade_mp=unidade_mp,
            pesounitario_mp=pesounitario_mp,
            pesototal_mp=pesototal_mp,
            custo_mp=custo_mp,
            custoemkg_mp=cost_per_unit,
            departamento_mp=departamento_mp,
            pedidomin_mp=pedidomin_mp,
            gastomedio_mp=gastomedio_mp,
            gms_mp=gmps,
            user_id=current_user.id
            )
        
        db.session.add(materiasprimas)
        db.session.commit()

        id_mp = materiasprimas.id_mp
        gms = materiasprimas.gms_mp
        pedidomin = materiasprimas.pedidomin_mp


        estoque = Estoque(
            id_mp=id_mp,
            nome_mp=nome_mp,
            unidade_mp=unidade_mp,
            quantidade_estq=0,
            gms_mp=gms,
            pedidomin_mp=pedidomin,  
            user_id=current_user.id
        )
        
        
        db.session.add(estoque)
        db.session.commit()

        return redirect(url_for('materiasPrimas'))

    materiasprimas = MateriasPrimas.query.filter_by(user_id=current_user.id).all()
    materiaprima_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiaprima_schema.dump(materiasprimas)

    
    config = Config.query.first()
    if config:
        giro_medio = config.giro_medio
    else:
        giro_medio = 6

    return render_template('materiasprimas.html', materiasprimas = serialized_data_mp, giromedio=giro_medio)

@app.route('/delete-materiaprima/<int:id>', methods=['POST'])
def deleteMateriaPrima(id):
    # Get the MateriasPrimas object to delete
    materiasprimas = MateriasPrimas.query.get_or_404(id)
    
    # Delete related records in the estoque table
    estoque_items = Estoque.query.filter_by(id_mp=id).all()
    for estoque_item in estoque_items:
        db.session.delete(estoque_item)
    
    # Commit the session to delete the related records
    db.session.commit()

    # Now, delete the MateriasPrimas object
    db.session.delete(materiasprimas)
    db.session.commit()

    return redirect(url_for('materiasPrimas', id=id))


@app.route('/edit-materiaprima/<int:id>', methods=['POST'])
def editMateriaPrima(id):
    if request.method == 'POST':
        # Get the MateriasPrimas object to edit
        materiasprimas = MateriasPrimas.query.get_or_404(id)

        # Update attributes of the MateriasPrimas object
        materiasprimas.nome_mp = request.form.get('nome_mp')
        materiasprimas.unidade_mp = request.form.get('unidade_mp')
        materiasprimas.pesounitario_mp = request.form.get('pesounitario_mp')
        materiasprimas.pesototal_mp = request.form.get('pesototal_mp')
        materiasprimas.custo_mp = request.form.get('custo_mp')
        materiasprimas.departamento_mp = request.form.get('departamento_mp')
        materiasprimas.pedidomin_mp = request.form.get('pedidomin_mp')
        materiasprimas.gastomedio_mp = request.form.get('gastomedio_mp')

        # Convert cost and total weight to floats
        custo_mp_float = float(materiasprimas.custo_mp)
        pesototal_mp_float = float(materiasprimas.pesototal_mp)  
        
        if pesototal_mp_float != 0:
            materiasprimas.custoemkg_mp = custo_mp_float / pesototal_mp_float

        # Commit the changes to the MateriasPrimas object
        db.session.commit()

        # Update corresponding values in the related Estoque table
        estoque_items = Estoque.query.filter_by(id_mp=id).all()
        for estoque_item in estoque_items:
            estoque_item.nome_mp = materiasprimas.nome_mp
            estoque_item.unidade_mp = materiasprimas.unidade_mp
            estoque_item.gms_mp = materiasprimas.gms_mp
            estoque_item.pedidomin_mp = materiasprimas.pedidomin_mp

        # Commit the changes to the related Estoque records
        db.session.commit()

        return redirect(url_for('materiasPrimas', id=id))

# INVENTARIO ############################################################################

@app.route('/inventario', methods=['GET', 'POST'])
def inventario():


    today_date = datetime.now()
    formatted_date = format_date(today_date, format='full', locale='pt')

    estoque = Estoque.query.filter_by(user_id=current_user.id).all()
    estoque_schema = EstoqueSchema(many=True)
    serialized_data_estq = estoque_schema.dump(estoque)

    materiasprimas = MateriasPrimas.query.filter_by(user_id=current_user.id).all()
    materiasprimas_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiasprimas_schema.dump(materiasprimas)

    

    if request.method == 'POST':
        new_quantities = request.form.getlist('quantidade_estq')

        for index, invt in enumerate(estoque):
            id_mp=invt.id_mp
            nome_mp = invt.nome_mp
            old_quantity = invt.quantidade_estq
            new_quantity = new_quantities[index]

            #diference between old quantity and new quantity
            old_quantity_float = float(old_quantity)
            new_quantity_float = float(new_quantity)
            difference = new_quantity_float - old_quantity_float

            # Get current timestamp with microseconds
            current_time = datetime.now()

            modo = 'Registro Manual'

            # Fetch the nome_fornecedor corresponding to the id_fornecedor from the Fornecedor table
            

            if difference != 0:
                #print(id_mp, current_time,old_quantity, new_quantity, difference)
                historico = Historico(
                date_change=current_time,
                id_mp=id_mp,
                nome_mp=nome_mp,
                ultimaquantidade_hst=old_quantity,
                novaquantidade_hst=new_quantity,
                difference_hst=difference,
                modo_hst=modo,
                user_id=current_user.id
                )

                db.session.add(historico)

            invt.quantidade_estq = new_quantities[index]

        db.session.commit()


        return redirect(url_for('inventario'))
    
    historico = Historico.query.filter_by(user_id=current_user.id).all()
    historico_schema = HistoricoSchema(many=True)
    serialized_data_hst = historico_schema.dump(historico)

   
    inventario = Inventario.query.filter_by(user_id=current_user.id).all()
    inventario_schema = InventarioSchema(many=True)
    

    # Separate compras into two lists based on estado_compras
    inventario_aberto = [invt for invt in inventario if invt.estado_invt == "Aberto"]
    inventario_fechado = [invt for invt in inventario if invt.estado_invt == "Fechado"]

    serialized_data_invtAberto = inventario_schema.dump(inventario_aberto)
    serialized_data_invtFechado = inventario_schema.dump(inventario_fechado)


    inventariodados = InventarioDados.query.filter_by(user_id=current_user.id).all()
    inventariodados_schema = InventarioDadosSchema(many=True)
    serialized_data_invtDados = inventariodados_schema.dump(inventariodados)
    
    

    return render_template('inventario.html', 
                           historico=serialized_data_hst , 
                           estoque=serialized_data_estq, 
                           today_date=formatted_date,
                            materiasprimas=serialized_data_mp,
                            datetime=datetime,
                            inventarioAberto=serialized_data_invtAberto,
                            inventarioFechado=serialized_data_invtFechado,
                            inventarioDados=serialized_data_invtDados,

                            )

#########################################################################################################################################
# Translation dictionaries for months and days in Portuguese
MONTHS_PT = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

DAYS_PT = {
    0: "seg",
    1: "ter",
    2: "qua",
    3: "qui",
    4: "sex",
    5: "sáb",
    6: "dom"
}

def datetimeformat(value):
    if isinstance(value, str):
        # Adjust format string to match the datetime string format
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')  
    formatted_date = value.strftime("%d/%m/%Y")
    day_of_week = DAYS_PT[value.weekday()]  # Get the day of the week in Portuguese
    return f"{formatted_date} ({day_of_week})"
app.jinja_env.filters['datetimeformat'] = datetimeformat


def datetimeformat2(value):
    if isinstance(value, str):
        # Adjust format string to match the datetime string format
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')  
    formatted_date = value.strftime("%d/%m/%Y")
    day_of_week = DAYS_PT[value.weekday()]  # Get the day of the week in Portuguese
    return f"{formatted_date} ({day_of_week})"
app.jinja_env.filters['datetimeformat2'] = datetimeformat2

def custom_datetime_format(value):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    formatted_date = value.strftime("%Y-%m-%d (%H:%M)")
    return formatted_date
app.jinja_env.filters['custom_datetime_format'] = custom_datetime_format

def custom_datetime_format2(value):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    formatted_date = value.strftime("%Y-%m-%d (%H:%M)")
    return formatted_date
app.jinja_env.filters['custom_datetime_format2'] = custom_datetime_format2


###########################################################################################################################################

@app.route('/salvar_inventario', methods=['POST'])
def salvar_inventario():
    date_str = request.form['datePicker']
    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    inventario = Inventario(
        data_invt=date_object,
        estado_invt='Aberto',
        user_id=current_user.id
        )
    db.session.add(inventario)
    db.session.commit()

    selected_items = request.form.getlist('selected_items')
    for item_id in selected_items:
        

        item = MateriasPrimas.query.filter_by(id_mp=item_id).first()
        # Check if the item exists
        if item:
        # If the item exists, access its attributes
            nome_mp = item.nome_mp
            unidades_mp = item.unidade_mp
        else:
        # Handle the case where the item does not exist
        # You can log a message, skip this item, or handle it in any other appropriate way
            print(f"Item with nome_mp '{item_id}' does not exist in the database.")
        
        quantidade_estq = Estoque.query.filter_by(id_mp=item_id).first().quantidade_estq

        inventariodados = InventarioDados( 
            id_invt=inventario.id_invt,
            data_invt=date_object,
            id_mp=item_id,
            nome_mp=nome_mp,
            unidade_mp=unidades_mp,
            quantidade_invtdados=0.0,
            quantidade_estq=quantidade_estq,
            user_id=current_user.id
            )
        db.session.add(inventariodados)
    db.session.commit()


    return redirect(url_for('inventario'))

@app.route('/fechar_inventario', methods=['POST'])
def fechar_inventario():
    
    new_quantities = request.form.getlist('quantidade_invtdados')
    id_mps = request.form.getlist('id_mp')
    id_invts = request.form.getlist('id_invt')


    for new_quantity, id_mp, id_invt in zip(new_quantities, id_mps, id_invts):
        estoque = Estoque.query.filter_by(id_mp=id_mp).first()

        inventario = Inventario.query.filter_by(id_invt=id_invt).first()
        inventario.estado_invt = 'Fechado'

        # Check if estoque is found
        if estoque:
            nome_mp = estoque.nome_mp
            old_quantity = estoque.quantidade_estq

            old_quantity_float = float(old_quantity)
            new_quantity_float = float(new_quantity)

            difference = new_quantity_float - old_quantity_float

        # Add history if there's a difference
            if difference != 0:
                current_time = datetime.now()
                modo = 'Inventario'

                historico = Historico(
                date_change=current_time,
                id_mp=id_mp,
                nome_mp=nome_mp,
                ultimaquantidade_hst=old_quantity,
                novaquantidade_hst=new_quantity,
                difference_hst=difference,
                modo_hst=modo,
                user_id=current_user.id
                )
                db.session.add(historico)

        # Update the quantity in estoque
        estoque.quantidade_estq = new_quantity

        #change the status of the inventory to 'Fechado'
        

        # Commit changes to the database
        db.session.commit()
    return redirect(url_for('inventario'))







## PEDIDO DE COMPRAS ###################################################################################################################

@app.route('/compras', methods=['GET', 'POST'])
@login_required
def compras():

    fornecedores = Fornecedores.query.filter_by(user_id=current_user.id).all()
    fornecedores_schema = FornecedorSchema(many=True)
    

    estoque = Estoque.query.filter_by(user_id=current_user.id).all()
    estoque_schema = EstoqueSchema(many=True)
    

    compras = Compras.query.filter_by(user_id=current_user.id).all()
    compras_schema = ComprasSchema(many=True)
    

    comprasdados = ComprasDados.query.filter_by(user_id=current_user.id).all()
    comprasdados_schema = ComprasDadosSchema(many=True)
    

    # Dictionary to store counts of fechado_comprasd for each compras_id
    fechado_comprasd_counts = {}

    # Counting fechado_comprasd values for each compras_id
    for dado in comprasdados:
        if dado.id_compras not in fechado_comprasd_counts:
            fechado_comprasd_counts[dado.id_compras] = []
        fechado_comprasd_counts[dado.id_compras].append(dado.fechado_comprasd)

    # Updating estado_compras for compras with all fechado_comprasd values set to 1
    for compra in compras:
        fechado_comprasd_values = fechado_comprasd_counts.get(compra.id_compras, [])
        if all(value == 1 for value in fechado_comprasd_values):
            compra.estado_compras = "Entregue"
    
    # Separate compras into two lists based on estado_compras
    compras_entregue = [compra for compra in compras if compra.estado_compras == "Entregue"]
    compras_pendente = [compra for compra in compras if compra.estado_compras == "Pendente"]
    
    # Commit the changes to the database
    db.session.commit()

    # Serialize the data for rendering in the template
    serialized_data_f = fornecedores_schema.dump(fornecedores)
    serialized_data_estq = estoque_schema.dump(estoque)
    serialized_data_compras_entregue = compras_schema.dump(compras_entregue)
    serialized_data_compras_pendente = compras_schema.dump(compras_pendente)
    serialized_data_comprasdados = comprasdados_schema.dump(comprasdados)

    return render_template('compras.html', 
                           comprasEntregue=serialized_data_compras_entregue,
                           comprasPendente=serialized_data_compras_pendente,
                           comprasdados=serialized_data_comprasdados, 
                           estoque=serialized_data_estq,
                           fornecedores=serialized_data_f)


@app.route('/salvar_compra', methods=['POST'])
def salvar_compra():
    
    print('salvando')
    current_time = datetime.now()

    compras = Compras(
        data_compras=current_time,
        estado_compras='Pendente',
        user_id=current_user.id
        )
    db.session.add(compras)
    db.session.commit()
    
    selected_items = request.form.getlist('selected_items[]')
    for item_id in selected_items:
        item = MateriasPrimas.query.filter_by(nome_mp=item_id).first()
# Check if the item exists
        if item:
        # If the item exists, access its attributes
            unidade_mp = item.unidade_mp
            cost_per_unit = item.custoemkg_mp
            departamento_comprasd = item.departamento_mp
        else:
        # Handle the case where the item does not exist
        # You can log a message, skip this item, or handle it in any other appropriate way
            print(f"Item with nome_mp '{item_id}' does not exist in the database.")
        # Fetch form data
        pedido_comprasd = Decimal(request.form.get(f'pedido_comprasd_{item_id}'))
        fornecedor_comprasd = request.form.get(f'fornecedores_{item_id}')

        forn = Fornecedores.query.filter_by(nome_fornecedor=fornecedor_comprasd).first()
        previsao = forn.tempo_entrega
        vencimento = forn.prazo_pagamento

        # Get today's date
        today = datetime.now()

        previsao_comprasd = today + timedelta(days=previsao)        
        vencimento_comprasd = today + timedelta(days=vencimento)  

             

        #Calculate purchase order value
        valorpedido_comprasd = pedido_comprasd * cost_per_unit

        comprasdados = ComprasDados(  
            id_compras = compras.id_compras,
            nome_mp = item_id,
            unidade_mp = unidade_mp,
            pedido_comprasd = pedido_comprasd,
            fornecedor_comprasd = fornecedor_comprasd,
            valorpedido_comprasd =  valorpedido_comprasd,
            departamento_comprasd=departamento_comprasd,
            previsao_comprasd = previsao_comprasd,
            vencimento_comprasd = vencimento_comprasd,
            fechado_comprasd = False,
            user_id=current_user.id
            )
        db.session.add(comprasdados)

    db.session.commit()
    
    return redirect(url_for('compras'))


@app.route('/fechar_compra', methods=['POST'])
def fechar_compra():

    selected_items = request.form.getlist('selected_dados[]')

    for item_id in selected_items:

        print(item_id)

        
        comprasd = ComprasDados.query.get_or_404(item_id)
        comprasd.fechado_comprasd = True
        #update stock
        estoquemp = Estoque.query.filter_by(nome_mp=comprasd.nome_mp).first()
        estoquequantidade = estoquemp.quantidade_estq
        estoquenome = estoquemp.nome_mp
        pedidoFloat = Decimal(comprasd.pedido_comprasd)
        estoquemp.quantidade_estq = estoquequantidade + pedidoFloat
        #add history

        # Fetch the nome_fornecedor corresponding to the id_fornecedor from the Fornecedor table
        materiap = MateriasPrimas.query.filter_by(nome_mp=estoquenome).first()
        id_materiaprima = materiap.id_mp if materiap else None

        # Get current timestamp with microseconds
        current_time = datetime.now()

        modo = 'Compra'

        historico = Historico(
            date_change=current_time,
            id_mp=id_materiaprima,
            nome_mp=comprasd.nome_mp,
            ultimaquantidade_hst=estoquequantidade,
            novaquantidade_hst=estoquequantidade + pedidoFloat,
            difference_hst=pedidoFloat,
            modo_hst=modo,
            user_id=current_user.id
            )
        
        db.session.add(historico)
        db.session.commit()


    return redirect(url_for('compras'))
############################################################################### RUN APP ################################################

@app.route('/historico', methods=['GET'])
@login_required
def historico():




    filter_option = request.args.get('filterOption', 'all')
    
    if filter_option == 'all':
        # Retrieve all data if filter_option is 'all'
        historico = Historico.query.filter_by(user_id=current_user.id).all()
    else:
        # Retrieve data based on the selected mode
        historico = Historico.query.filter_by(user_id=current_user.id, modo_hst=filter_option).all()

    # Render the template with the filtered data
    return render_template('historico.html', historico=historico)

# RECEITAS #####################################################
    

@app.route('/receitas', methods=['GET', 'POST'])
@login_required
def receitas():

    materiasprimas = MateriasPrimas.query.filter_by(user_id=current_user.id).all()
    materiasprimas_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiasprimas_schema.dump(materiasprimas)



    #if request
    if request.method == 'POST':
        nome_rct = request.form.get('nome_rct')
        
        descricao_rct = request.form.get('descricao_rct')
        preparo_rct = request.form.get('preparo_rct')
        rendimento_rct = request.form.get('rendimento_rct')
        class_rct = request.form.get('class_rct')
        departamento_rct = request.form.get('departamento_rct')
        validade_rct = request.form.get('validade_rct')
        pedidomin_rct = request.form.get('pedidomin_rct')
        cod_rct = request.form.get('cod_rct')
        
        
        rendimentokg_rct = 0.0 #initial empty value
        unidadeporkg_rct = 0.0

        receitas = Receitas(
            nome_rct=nome_rct,
            cod_rct=cod_rct,
            descricao_rct=descricao_rct,
            preparo_rct=preparo_rct,
            rendimento_rct=rendimento_rct,
            rendimentokg_rct=rendimentokg_rct,
            class_rct=class_rct,
            departamento_rct=departamento_rct,
            pedidomin_rct=pedidomin_rct,
            validade_rct=validade_rct,
            unidadeporkg_rct=unidadeporkg_rct,
            user_id=current_user.id,
            contador_rct=0,
            estoque_rct=0
        )

        db.session.add(receitas)
        db.session.commit()

        id_rct = receitas.id_rct
        
        
        # Handle ingredients insertion
        ingredient_count = int(request.form.get('ingredient_count'))
        
        # rendimentototal = sum(float(request.form.get(f'quantidade_{i}')) for i in range(ingredient_count))
        rendimentototal = sum(float(request.form.get(f'quantidade_{i}')) for i in range(ingredient_count) if request.form.get(f'tipo_rctmp_{i}') == 'Ingrediente')

        for i in range(ingredient_count):
            id_mp = request.form.get(f'id_mp_{i}')
            quantidade = request.form.get(f'quantidade_{i}')
            tipo = request.form.get(f'tipo_rctmp_{i}')
        

             # Fetch the nome_mp corresponding to the id_mp from the MP table
            materiaprima = MateriasPrimas.query.filter_by(id_mp=id_mp).first()
            nome_mp = materiaprima.nome_mp if materiaprima else None
            unidade_mp = materiaprima.unidade_mp if materiaprima else None
            print('############## ', unidade_mp)

            receita_mp = ReceitaMateriasPrimas(
                id_rct=id_rct,
                id_mp=id_mp,
                nome_mp=nome_mp,
                quantidade=quantidade,
                tipo_rctmp=tipo,
                unidade=unidade_mp,
                user_id=current_user.id
            )
            
            #Update receitas with new total rendimento value
            unidadedividido =  receitas.rendimento_rct / rendimentototal
            
            # Round unidadedividido to the nearest higher integer
            unidadedividido_rounded = math.ceil(unidadedividido)
            
            receitas.unidadeporkg_rct = unidadedividido_rounded
            
            receitas.rendimentokg_rct = rendimentototal
        
            db.session.add(receita_mp)
            db.session.commit()
            
            
        
        return redirect(url_for('receitas')) 
    
    receitas = Receitas.query.filter_by(user_id=current_user.id).all()
    receitas_schema = ReceitasSchema(many=True)
    serialized_data_rct = receitas_schema.dump(receitas)

    receitasmp = ReceitaMateriasPrimas.query.filter_by(user_id=current_user.id).all()
    receitasmp_schema = ReceitasMateriasPrimasSchema(many=True)
    serialized_data_rctmp = receitasmp_schema.dump(receitasmp)
    



    return render_template('receitas2.html', 
    materiasprimas=serialized_data_mp, 
    receitas=serialized_data_rct,
    receitasmp=serialized_data_rctmp)
    

@app.route('/edit-receita/<int:id>', methods=['POST'])
def editReceita(id):
    if request.method == 'POST':
        receita = Receitas.query.get_or_404(id)
        receita.nome_rct = request.form.get('nome_rct')
        receita.descricao_rct = request.form.get('descricao_rct')
        receita.rendimento_rct = request.form.get('rendimento_rct')
        receita.class_rct = request.form.get('class_rct')
        receita.departamento_rct = request.form.get('departamento_rct')
        receita.validade_rct = request.form.get('validade_rct')
        receita.pedidomin_rct = request.form.get('pedidomin_rct')

        db.session.commit()
        return redirect(url_for('receitas', id=id))


@app.route('/edit-receita-ingrediente/<int:id>', methods=['POST'])
def editReceitaIngrediente(id):
    if request.method == 'POST':
        receitaIngrediente = ReceitaMateriasPrimas.query.get_or_404(id)
        receitaIngrediente.quantidade = request.form.get('quantidade_rct')
       

        db.session.commit()
        return redirect(url_for('receitas', id=id))
    

@app.route('/delete-receita-ingrediente/<int:id>', methods=['POST'])
def deleteReceitaIngrediente(id):
    ReceitaMateriasPrimas.query.filter_by(id_rctmp=id).delete()
       

    db.session.commit()
    return redirect(url_for('receitas', id=id))

    
#DELETE
@app.route('/delete-receita/<int:id>', methods=['POST'])
def deleteReceita(id):
    
     # Fetch the receitas record
    receitas = Receitas.query.get_or_404(id)
    
    try:
        # Delete child records from ReceitaMateriasPrimas table
        ReceitaMateriasPrimas.query.filter_by(id_rctmp=id).delete()
        
        # Delete the parent record from Receitas table
        db.session.delete(receitas)
        db.session.commit()
    except IntegrityError:
        # If there's an integrity error, rollback changes and abort with error message
        db.session.rollback()
        abort(500, "Cannot delete or update a parent row: a foreign key constraint fails")
    
    return redirect(url_for('receitas', id=id) )
   

@app.route('/produccao', methods=['GET', 'POST'])
def produccao():

    receitas = Receitas.query.filter_by(user_id=current_user.id).all()
    receitas_schema = ReceitasSchema(many=True)
    serialized_data_rct = receitas_schema.dump(receitas)
    
    filiais = Filiais.query.filter_by(user_id=current_user.id).all()
    filiais_schema = FiliaisSchema(many=True)
    serialized_data_filiais = filiais_schema.dump(filiais)

    produc = Produc.query.filter_by(user_id=current_user.id).all()
    produc_schema = ProducSchema(many=True)

    producdados = ProducDados.query.filter_by(user_id=current_user.id).all()
    producdados_schema = ProducDadosSchema(many=True)

    produc_pendente = [pdc for pdc in produc if pdc.estado_pdc == "Pendente"]
    produc_fechado = [pdc for pdc in produc if pdc.estado_pdc == "Fechado"]

    serialized_data_produc_pendente = produc_schema.dump(produc_pendente)
    serialized_data_produc_fechado = produc_schema.dump(produc_fechado)
    serialized_data_produc_dados = producdados_schema.dump(producdados)

    return render_template('produccao.html', 
                           receitas=serialized_data_rct,
                           producPendente=serialized_data_produc_pendente,
                           producFechado=serialized_data_produc_fechado,
                           producDados=serialized_data_produc_dados,
                           filiais=serialized_data_filiais)


@app.route('/salvar_pdc', methods=['POST'])
def salvar_pdc():
    current_time = datetime.now()

     # Extract the data from the request body
    request_data = request.get_json()

    # Access the rows data sent from the frontend
    rct_id = request_data.get('rct_id')
    rows = request_data.get('rows', [])
    filial = request_data.get('filial')
    quantidade = request_data.get('quantidade')

    receitas = Receitas.query.filter_by(id_rct=rct_id).first()
    nome_rct = receitas.nome_rct
    departamento_rct = receitas.departamento_rct
    class_rct = receitas.class_rct
    pedidominimo_rct = receitas.pedidomin_rct
    codigo_rct = receitas.cod_rct
    
    
    # Increment contador_rct by 1
    receitas.contador_rct = int(receitas.contador_rct) + 1
    
    #logic insert 
    
   
    
    
    filiais = Filiais.query.filter_by(id_fil=filial).first()
    nomefilial = filiais.loja_fil
    
    planomestre = PlanoMestre(
        codigo_rct=codigo_rct,
        nome_rct=nome_rct,
        class_rct=class_rct,
        departamento_rct=departamento_rct,
        data_pm=current_time,
        
        estoque_pm=0,
        
        pedidototal_pm=0,
        pedidokgtotal_pm=0.000,
        
        rctnecessaria_pm=0
        
    )
    
    db.session.add(planomestre)
    db.session.commit()
    
    planomestref = PlanoMestreFiliais(
        id_pm=planomestre.id_pm,
        filial_pdc=filial,
        nomefilial_pdc=nomefilial,
        quantidade_pdc=quantidade
    )
    
    db.session.add(planomestref)
    db.session.commit()
    
    

    
    print(' #########################',nomefilial)

    produccao = Produc(
        data_pdc=current_time,
        estado_pdc='Pendente',
        nome_rct=nome_rct,
        filial_pdc=filial,
        nomefilial_pdc=nomefilial,
        departamento_rct=departamento_rct,
        class_rct=class_rct,
        pedidomin_rct=pedidominimo_rct,
        quantidade_pdc=quantidade,
        user_id=current_user.id
        )
    db.session.add(produccao)
    db.session.commit()
    
  
    

     # Process the received data as needed
    for row in rows:
        id_mp = row.get('id_mp')
        nome_mp = row.get('nome_mp')
        quantidade = row.get('quantidade')
        multiplied_value = row.get('multiplied_value')
        unidade = row.get('unidade')

        #print(rct_id,id_mp, nome_mp, quantidade, multiplied_value, unidade)
        
            
        producdados = ProducDados(
            id_pdc = produccao.id_pdc,
            id_rct = rct_id,
            id_mp = id_mp,
            nome_mp = nome_mp,
            quantidade_pdcd = multiplied_value,
            unidade_pdcd = unidade,
            user_id=current_user.id
        )
        db.session.add(producdados)
    
        db.session.commit()
        
        
        
        
      
    # Assuming 'produccao_url' is the URL to which you want to redirect
    produccao_url = url_for('produccao')

    # Return a JSON response with the redirect URL
    return jsonify({'redirect_url': produccao_url})
    
@app.route('/fechar_pdc', methods=['POST'])
def fechar_pdc():
    
    current_time = datetime.now()

    selected_items = request.form.getlist('nome_mp[]')
    selected_id = request.form.getlist('id_pdc[]')


    for mp,id_pdc in zip(selected_items,selected_id):

        
        print(mp,id_pdc)

        produc = Produc.query.get_or_404(id_pdc)
        produc.estado_pdc = 'Fechado'
        produc.fechadoem_pdc = current_time
        

        producd = ProducDados.query.filter_by(nome_mp=mp, id_pdc=id_pdc).first()
        
        estoque = Estoque.query.filter_by(nome_mp=mp).first()
        estoquequantidade = estoque.quantidade_estq
        
        receita = Receitas.query.filter_by(nome_rct=produc.nome_rct).first()
        receita.estoque_rct = int(receita.estoque_rct) + produc.quantidade_pdc
        receita.contador_rct = int(receita.contador_rct) - 1


        pedidoFloat = Decimal(producd.quantidade_pdcd)

        current_time = datetime.now()

        modo = 'Produção'

        
        
        historico = Historico(
            date_change=current_time,
            id_mp=producd.id_mp,
            nome_mp=producd.nome_mp,
            ultimaquantidade_hst=estoquequantidade,
            novaquantidade_hst=estoquequantidade - pedidoFloat,
            difference_hst=-pedidoFloat,
            modo_hst=modo,
            user_id=current_user.id
            )
        
        db.session.add(historico)
        
        estoque.quantidade_estq = estoquequantidade - pedidoFloat
    
        db.session.commit()
        

    return redirect(url_for('produccao'))

@app.route('/get_recipe_info', methods=['POST'])
def get_recipe_info():
    selected_recipe_name = request.json.get('selected_recipe')
    # Query the database for the recipe with the selected name
    receita = Receitas.query.filter_by(id_rct=selected_recipe_name).first()
    receitamps = ReceitaMateriasPrimas.query.filter_by(id_rct=selected_recipe_name).all()
    estoque = Estoque.query.filter_by(user_id=current_user.id).all()
    

    if receita:
        # If the recipe is found, return its information
        recipe_info = {
            'nome': receita.nome_rct,
            'rendimento': receita.rendimento_rct,
            'receitamps_info': [],  # Initialize the list outside the loop
            'estoque_info': []
        }

          # Create a set to store the id_mp values from receitamps
        receitamp_ids = set(receitamp.id_mp for receitamp in receitamps)

        for receitamp in receitamps:
            receitamp_info = {
                'id_mp': receitamp.id_mp,
                'nome_mp': receitamp.nome_mp,
                'quantidade': receitamp.quantidade,
                'unidade': receitamp.unidade
            }
            recipe_info['receitamps_info'].append(receitamp_info)
            
        for estq in estoque:

            if estq.id_mp in receitamp_ids:

                estq_info = {
                    'id_mp': estq.id_mp,
                    'nome_mp': estq.nome_mp,
                    'quantidade_estq': estq.quantidade_estq,
                }
                recipe_info['estoque_info'].append(estq_info)

        return jsonify(recipe_info)
    else:
        # If the recipe is not found, return an empty response or an error message
        return jsonify({}), 404


from collections import defaultdict  


@app.route('/planomestre')
def planomestre():
    
    ## DATABASE COLLECTION
    
    produc = Produc.query.filter_by(user_id=current_user.id).all()
    produc_schema = ProducSchema(many=True)

    produc_pendente = [pdc for pdc in produc if pdc.estado_pdc == "Pendente"]
    serialized_data_produc_pendente = produc_schema.dump(produc_pendente)
    
    receitas = Receitas.query.filter_by(user_id=current_user.id).all()
    receitas_schema = ReceitasSchema(many=True)
    serialized_data_rct = receitas_schema.dump(receitas)
    
    filiais = Filiais.query.filter_by(user_id=current_user.id).all()
    
    
    
    
   
    
    ## DICTIONARIO PLANO MESTRE
    
    planomestre = {}
    
    for rct in receitas:
        
        try:
            contador_rct = int(rct.contador_rct)  # Convert to integer
        except ValueError:
            continue  # Skip this recipe if conversion fails
    
        if contador_rct > 0:
            
            planomestre[rct.id_rct] = {
                'detalhes':{
                    'nome_rct':rct.nome_rct,
                    'id_rct':rct.id_rct,
                    'rendimento_rct':rct.rendimento_rct,
                    'class_rct':rct.class_rct,
                    'departamento_rct':rct.departamento_rct,
                    'rendimentokg_rct':rct.rendimentokg_rct,
                    'unidadeporkg_rct':rct.unidadeporkg_rct,
                    'contador_rct':rct.contador_rct,
                    'estoque_rct':rct.estoque_rct
                    
                },
                
                'pedidos': {},
                'totales': {
                    'pedido_total_em_un':0,
                    'pedido_em_kg_total':0.0,
                    'num_receitas_necessaria':0.0
                    
                }
                
            }
            
            total_total = 0
            
            for f in filiais:
                pedido_total_por_loja = 0
                
                planomestre[rct.id_rct]['pedidos'][f.loja_fil] = {}
                
                for pdc in produc:
                    if pdc.estado_pdc == "Pendente":
                        if pdc.nomefilial_pdc == f.loja_fil:
                        
                            pedido_total_por_loja += pdc.quantidade_pdc
                    
                
                total_total += pedido_total_por_loja
                
                print(total_total)

                
                planomestre[rct.id_rct]['pedidos'][f.loja_fil] = {
                'pedido_total': pedido_total_por_loja
                }
                
                pedido_total_em_un = total_total - rct.estoque_rct
                pedido_em_kg_total = round(pedido_total_em_un / rct.rendimentokg_rct, 3)
                num_receitas_necessaria = round(pedido_total_em_un / rct.unidadeporkg_rct, 3)
                
                
                # fill the dictionarie totales with corresponding values
                planomestre[rct.id_rct]['totales']['pedido_total_em_un'] = pedido_total_em_un
                planomestre[rct.id_rct]['totales']['pedido_em_kg_total'] = pedido_em_kg_total
                planomestre[rct.id_rct]['totales']['num_receitas_necessaria'] = num_receitas_necessaria
                
                
    
    
    return render_template('planomestre.html', 
                           producPendente=serialized_data_produc_pendente,
                           receitas=serialized_data_rct,
                           planomestre=planomestre
                          )


#host='93.127.210.253'

if __name__ == '__main__':

    app.run()
