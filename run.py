##
# Imports para Front End
#
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import send_from_directory

##
# Imports para Macros
#

import forms

##
# Imports para Manejo de CSV con pandas
#
import pandas as pd

# import numpy as np
# from numpy.distutils.conv_template import header

##
# Manejo del CSV
#

def escribirCSV(nombre, noAlgoritmo, comentario):
    # Datos Default para pueba POC
    
    diccionario = {'Algorithm Number': [noAlgoritmo], 
        'Obj_quantity': [24], 
        'Precision': [42],
        'Notes': [comentario]}

    listaColumnas = ['Algorithm Number', 'Obj_quantity', 'Precision', 'Notes']
    
    #Creando CSV
    
    df = pd.DataFrame(diccionario, columns = listaColumnas)
    df.to_csv('C:/Users/Kevin MM/eclipse-workspace/SegmentacionCelulas/static/csv/'+nombre+'.csv') #Especificar ruta
    print("Creado con Exito")

def leerCSV(nombreArchivo):
    df = pd.read_csv('C:/Users/Kevin MM/eclipse-workspace/SegmentacionCelulas/static/csv/'+nombreArchivo+'.csv')
    print(df['Algorithm Number'][4] + ' ' + df['Precision'][4]) #Se escoge la columna a leer y lo demas se trata como una lista

##
#Pagina Web
#

app = Flask(__name__) #nuevo objeto

@app.route('/', methods = ['GET', 'POST']) #wrap o decorador que tiene la ruta
def index():
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        print (comment_form.algoritmo.data)
        print (comment_form.comentario.data)
        print (comment_form.nombreCSV.data)
        escribirCSV(comment_form.nombreCSV.data, comment_form.algoritmo.data, comment_form.comentario.data)
        print("CSV Generado")
    title = "Segmentacion de Celulas"
    return render_template('index.html', title = title, form = comment_form)

if __name__ == '__main__':
    app.run(debug = True, port= 8000) # Corre el servidor 8000 si lo dejo en default es 5000
