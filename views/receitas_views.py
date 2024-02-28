from app import app
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow




#TODO função Receitas 
@app.route('/receitas')
def receitas():
    #receitas = receitas.query.all() #get values from receitas table
    #receita_schema = ReceitasSchema(many=True)
   # serialized_data = receita_schema.dump(receitas)
    return render_template('receitas/receitas.html')

##
