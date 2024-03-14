## IMPORTS AND CONFIGURATION ###############################

from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pymysql
import os
import datetime
from flask_login import UserMixin,current_user, login_required, LoginManager, login_user
pymysql.install_as_MySQLdb()

app = Flask(__name__)
secret_key = os.environ.get('FLASK_SECRET_KEY')
app.secret_key = secret_key
app.config.from_object('config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:pass123@localhost/labct2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=62)  # Set session expiration to 62 days
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config['MY_INTEGER'] = 6

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)




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
    pedidomin_mp = db.Column(db.Integer)
    gastomedio_mp = db.Column(db.Numeric(10, 3))
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


# USERS ##################################################

class Usuarios(UserMixin,db.Model):
    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    materiasprimas = db.relationship('MateriasPrimas', backref='user', lazy=True)
    fornecedores = db.relationship('Fornecedores', backref='user', lazy=True)

with app.app_context():
    db.create_all()




@app.route('/update', methods=['POST'])
def update():
    new_value = int(request.form['new_value'])
    app.config['MY_INTEGER'] = new_value
    return redirect(url_for('materiasPrimas'))

# Custom filter to round numbers
@app.template_filter('giromedio')
def round_filter(value):
    return value * app.config['MY_INTEGER']

@app.before_request
def before_request():
    if not hasattr(g, 'my_integer'):
        g.my_integer = 6

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
    cost_per_unit = 2
    if request.method == 'POST':
        id_mp = request.form.get('id_mp')
        nome_mp = request.form.get('nome_mp')
        unidade_mp = request.form.get('unidade_mp')
        pesounitario_mp = request.form.get('pesounitario_mp')
        pesototal_mp = request.form.get('pesototal_mp')
        custo_mp = request.form.get('custo_mp')
        departamento_mp = request.form.get('departamento_mp')
        pedidomin_mp = request.form.get('pedidomin_mp')
        gastomedio_mp = request.form.get('gastomedio_mp')
        
        # Convert cost and total weight to floats
        custo_mp_float = float(custo_mp)
        pesototal_mp_float = float(pesototal_mp)

        # Perform the division operation
        if pesototal_mp_float != 0:  # Avoid division by zero
            cost_per_unit = custo_mp_float / pesototal_mp_float

        materiasprimas = MateriasPrimas(
            id_mp=id_mp, 
            nome_mp=nome_mp, 
            unidade_mp=unidade_mp,
            pesounitario_mp=pesounitario_mp,
            pesototal_mp=pesototal_mp,
            custo_mp=custo_mp,
            custoemkg_mp=cost_per_unit,
            departamento_mp=departamento_mp,
            pedidomin_mp=pedidomin_mp,
            gastomedio_mp=gastomedio_mp,
            user_id=current_user.id
            
            )
        
        db.session.add(materiasprimas)
        db.session.commit()
        return redirect(url_for('materiasPrimas'))



    materiasprimas = MateriasPrimas.query.filter_by(user_id=current_user.id).all()
    materiaprima_schema = MateriasPrimasSchema(many=True)
    serialized_data_mp = materiaprima_schema.dump(materiasprimas)

    giromedio = MateriasPrimas.query.filter_by(user_id=current_user.id).all()

    return render_template('materiasprimas.html', materiasprimas = serialized_data_mp, my_integer=app.config['MY_INTEGER'])

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


# RUN APP ################################################

if __name__ == '__main__':

    
    app.run(debug=True)
