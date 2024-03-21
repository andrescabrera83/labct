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
import pandas as pd
import pdfkit
from jinja2 import Environment
from babel.dates import format_datetime

# Specify path to wkhtmltopdf executable
path_wkthmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)


from flask_login import UserMixin,current_user, login_required, LoginManager, login_user
pymysql.install_as_MySQLdb()

app = Flask(__name__)
secret_key = os.environ.get('FLASK_SECRET_KEY')
app.secret_key = secret_key
app.config.from_object('config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:pass123@localhost/labct2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=62)  # Set session expiration to 62 days
db = SQLAlchemy(app)
ma = Marshmallow(app)




# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

## MODELS AND SCHEMAS ###########################################################################################################################

#GIRO MEDIO##################################################################################################################################}

# Model for storing configuration settings
class Config(db.Model):
    __tablename__ = "giromedio"
    __table_args__ = {"extend_existing": True}
    id_gm = db.Column(db.Integer, primary_key=True)
    giro_medio = db.Column(db.Integer, default=6)

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
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

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
    pesounitario_mp = db.Column(db.Numeric(10, 3))
    pesototal_mp = db.Column(db.Numeric(10, 3))
    custo_mp = db.Column(db.Numeric(10, 2))
    custoemkg_mp = db.Column(db.Numeric(10, 2))
    departamento_mp = db.Column(db.Enum('Carnes', 'Farinhas', 'Hortifruti', 'Mercearia', 'Misturas', 'Ovos', 'Queijos'))
    pedidomin_mp = db.Column(db.Numeric(10,3))
    gastomedio_mp = db.Column(db.Numeric(10, 3))
    gms_mp = db.Column(db.Numeric(10, 3))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) 

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

# ESTOQUE #####################################################################################

class Estoque(db.Model):
    __tablename__ = "estoque"
    __table_args__ = {"extend_existing": True}

    id_estq = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'), nullable=False)
    materiaprima = db.relationship("MateriasPrimas", foreign_keys=[id_mp])

    nome_mp = db.Column(db.String(75))
    unidade_mp = db.Column(db.Enum('KG','UN'))
    gms_mp = db.Column(db.Numeric(10, 3))
    pedidomin_mp = db.Column(db.Numeric(10,3))

    quantidade_estq = db.Column(db.Numeric(10,3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
   
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

# INVENTARIO HISTORICO #######################################################################

class Historico(db.Model):
    __tablename__ = "historico"
    __table_args__ = {"extend_existing": True}

    id_hst = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_change = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    id_mp = db.Column(db.Integer, nullable=False)
    

    nome_mp = db.Column(db.String(75))

    ultimaquantidade_hst = db.Column(db.Numeric(10, 3))
    novaquantidade_hst = db.Column(db.Numeric(10, 3))
    difference_hst = db.Column(db.Numeric(10, 3))
    modo_hst = db.Column(db.Enum('Registro Manual', 'Inventario'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

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

# INVENTARIO ###################################################################################

class Inventario(db.Model):
    __tablename__ = "inventario"
    __table_args__ = {"extend_existing": True}

    id_invt = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_invt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    estado_invt = db.Column(db.Enum('Aberto', 'Fechado'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
   
class InventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventario
        
    id_invt = ma.auto_field()
    estado_invt = ma.auto_field()
    data_invt = ma.auto_field()

# INVENTARIO DADOS ###################################################################################

class InventarioDados(db.Model):
    __tablename__ = "inventariodados"
    __table_args__ = {"extend_existing": True}

    id_invtdados = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_invt = db.Column(db.Integer, db.ForeignKey('inventario.id_invt'), nullable=False)
    data_invt = db.Column(db.DateTime,db.ForeignKey('inventario.data_invt'), default=datetime.now(timezone.utc),nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('materiasprimas.id_mp'), nullable=False)
    quantidade_invtdados = db.Column(db.Numeric(10, 3))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
   
class InventarioDadosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = InventarioDados
        
    id_invtdados = ma.auto_field()
    id_invt = ma.auto_field()
    data_invt = ma.auto_field()
    id_mp = ma.auto_field()
    quantidade_invtdados = ma.auto_field()

# COMPRAS #################################################################################################

class Compras(db.Model):
    __tablename__ = "compras"
    __table_args__ = {"extend_existing": True}

    id_compras = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_compras = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    estado_compras = db.Column(db.Enum('Pendente', 'Entregue'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

class ComprasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Compras
        
    id_compras = ma.auto_field()
    estado_compras = ma.auto_field()
    data_compras = ma.auto_field()   

# USERS #################################################################################################

class Usuarios(UserMixin,db.Model):

    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    materiasprimas = db.relationship('MateriasPrimas', backref='user', lazy=True)
    fornecedores = db.relationship('Fornecedores', backref='user', lazy=True)
    estoque = db.relationship('Estoque', backref='user', lazy=True)
    inventariohistorico = db.relationship('Historico', backref='user', lazy=True)
    inventario = db.relationship('Inventario', backref='user', lazy=True)
    inventariosdados = db.relationship('InventarioDados', backref='user', lazy=True)
    compras = db.relationship('Compras', backref='user', lazy=True)

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

#DELETE
@app.route('/delete-materiaprima/<int:id>', methods=['POST'])
def deleteMateriaPrima(id):
    #remove from estoque first
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
                print(id_mp, current_time,old_quantity, new_quantity, difference)
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

    selected_month = request.args.get('selected_month')

    if selected_month:
        start_date = datetime.strptime(selected_month, '%Y-%m')
        end_date = start_date.replace(day=1, month=start_date.month % 12 + 1)
        
        inventario = Inventario.query.filter(Inventario.data_invt >= start_date, Inventario.data_invt < end_date).filter_by(user_id=current_user.id).all()
       
    else:
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
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo"
}

def datetimeformat(value):
    if isinstance(value, str):
        # Adjust format string to match the datetime string format
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')  
    month_pt = MONTHS_PT[value.month]
    day_pt = DAYS_PT[value.weekday()]
    return f"{day_pt}, {value.day} de {month_pt} de {value.year}"

app.jinja_env.filters['datetimeformat'] = datetimeformat




## PEDIDO DE COMPRAS ###################################################################################################################

@app.route('/compras', methods=['GET', 'POST'])
@login_required
def compras():

    estoque = Estoque.query.filter_by(user_id=current_user.id).all()
    estoque_schema = EstoqueSchema(many=True)
    serialized_data_estq = estoque_schema.dump(estoque)

    compras = Compras.query.filter_by(user_id=current_user.id).all()
    compras_schema = ComprasSchema(many=True)
    serialized_data_compras = compras_schema.dump(compras)



    return render_template('compras.html', compras=serialized_data_compras, estoque=serialized_data_estq)


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
    '''
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
    '''
    return redirect(url_for('compras'))

############################################################################### RUN APP ################################################

if __name__ == '__main__':
    app.run(debug=True)
