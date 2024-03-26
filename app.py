## IMPORTS AND CONFIGURATION ###############################

from flask import Flask, render_template, request, redirect, url_for, session, g, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship
import pymysql
import os
from datetime import datetime, timedelta, timezone
from babel.dates import format_date

import pdfkit
from decimal import Decimal

#from models.materiasprimas import MateriasPrimas


from models.estoque_model import Estoque
from models.materiasprimas_model import MateriasPrimas  
from models.fornecedores_model import Fornecedores
from models.historico_model import Historico
from models.inventario_model import Inventario
from models.inventariodados_model import InventarioDados
from models.compras_model import Compras
from models.comprasdados_model import ComprasDados
from models.usuarios_model import Usuarios
from models.config_model import Config
from db import db, ma, app

# Specify path to wkhtmltopdf executable
path_wkthmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)


from flask_login import UserMixin,current_user, login_required, LoginManager, login_user
pymysql.install_as_MySQLdb()



# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

## MODELS AND SCHEMAS ###########################################################################################################################

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
    quantidade_invtdados = ma.auto_field()   

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



####################################################################### APP ###################################################################################################
    
with app.app_context():
    db.create_all()

# FUNCOES DO GIRO MEDIO ########################################################################################################

def some_function(giro_medio):
    config = Config.query.filter_by(giro_medio=giro_medio).first()

    # Create or update configuration settings
def update_config(new_value):
    config = Config.query.first()
    if config:
        config.giro_medio = new_value
    else:
        config = Config(giro_medio=new_value)
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
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuarios(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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

    
    # Fetch the nome_fornecedor corresponding to the id_fornecedor from the Fornecedor table
    config = Config.query.first()
    giromedio = config.giro_medio if config else None

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
        custo_mp_float = float(custo_mp)
        pesototal_mp_float = float(pesototal_mp)
        gastomedio_mp_float = float(gastomedio_mp)
        giromedio_float = float(giromedio)

        

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

    #GIRO MEDIO####

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

    today_date = datetime.today()
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
            current_time = datetime.now().strftime('%Y-%m-%d // %H:%M:%S.%f')[:-3]

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

    available_months = db.session.query(func.DATE_FORMAT(Inventario.data_invt, '%Y-%m')).distinct().all()
    available_months = [date[0] for date in available_months]

    current_month = datetime.now().strftime('%Y-%m')

   
    inventario = Inventario.query.filter_by(user_id=current_user.id).all()
    inventario_schema = InventarioSchema(many=True)
    serialized_data_invt = inventario_schema.dump(inventario)
    
    

    return render_template('inventario.html', 
                           historico=serialized_data_hst , 
                           estoque=serialized_data_estq, 
                           today_date=formatted_date,
                            materiasprimas=serialized_data_mp,
                            datetime=datetime,
                            available_months=available_months,
                            inventario=serialized_data_invt,
                            current_month=current_month
                            )

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

def custom_datetime_format(value):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    formatted_date = value.strftime("%Y-%m-%d (%H:%M)")
    return formatted_date
app.jinja_env.filters['custom_datetime_format'] = custom_datetime_format

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
        inventariodados = InventarioDados( 
            id_invt=inventario.id_invt,
            data_invt=date_object,
            id_mp=item_id,
            quantidade_invtdados=0.0,
            user_id=current_user.id
            )
        db.session.add(inventariodados)
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
     # Dictionary to store fechado_comprasd values for each compras_id
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

    
    # Commit the changes to the database
    db.session.commit()

    # Serialize the data for rendering in the template
    serialized_data_f = fornecedores_schema.dump(fornecedores)
    serialized_data_estq = estoque_schema.dump(estoque)
    serialized_data_compras = compras_schema.dump(compras)
    serialized_data_comprasdados = comprasdados_schema.dump(comprasdados)

    return render_template('compras.html', 
                           compras=serialized_data_compras,
                           comprasdados=serialized_data_comprasdados, 
                           estoque=serialized_data_estq,
                           fornecedores=serialized_data_f)


@app.route('/salvar_compra', methods=['POST'])
def salvar_compra():
    
    print('salvando')
    current_time = datetime.now().strftime('%Y-%m-%d // %H:%M:%S.%f')[:-3]

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

        formatted_previsao = previsao_comprasd.strftime('%Y-%m-%dT%H:%M:%S')
        formatted_vencimento = vencimento_comprasd.strftime('%Y-%m-%dT%H:%M:%S')      

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
            previsao_comprasd = formatted_previsao,
            vencimento_comprasd = formatted_vencimento,
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
        current_time = datetime.now().strftime('%Y-%m-%d // %H:%M:%S.%f')[:-3]

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

        

        # system that knows if all items were closed to close the purchase order

        db.session.commit()


    return redirect(url_for('compras'))
############################################################################### RUN APP ################################################

if __name__ == '__main__':

    app.run(debug=True)
