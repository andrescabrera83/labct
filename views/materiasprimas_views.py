from app import app, db
from flask import render_template, redirect
from models import fornecedor_model
from schemas import fornecedor_schema



@app.route('/materiasprimas')
def materiasPrimas():

    materiasPrimas = materiasPrimas.query.all() #get values from fornecedores table
    fornecedor_schema = fornecedor_schema.FornecedorSchema(many=True)
    serialized_data = fornecedor_schema.dump(fornecedor_schema.FornecedorSchema, materiasPrimas)
    return render_template('materiasprimas/materiasprimas.html', fornecedores=serialized_data, materiasPrimas=materiasPrimas)

