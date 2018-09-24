"""
@package docstring
Aseguramiento de la Calidad del Software

Estudiantes:
Kevin Giancarlo Montoya Meza - 2015183063
Ignacio Cantillo Valladares - 2016099060
Jose Daniel Delgado Segura - 2015001500

"""

""" Imports para Front End """

from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory

import os

UPLOAD_FOLDER = os.path.abspath("./uploads/")
STATIC_FOLDER = os.path.abspath("./static/img")

""" Imports para Macros y Objetos """

import forms
import imagen

""" Imports para Manejo de CSV con pandas """
import pandas as pd

""""
    Crear Lista para manejo de imagenes en aplicacion web
    @param tam: tamanno de la lista que se desea construir
    @return l: lista construida 
"""

def listaT(tam):
    cont = 1;
    l = []
    if (tam == 0):
        raise ValueError('Lista de Imagenes Vacia')
    while cont < tam:
        l = l + [cont]
        cont += 1
    return l

""" Manejo del CSV """

"""
    Escribir CSV con datos generados de manera ficticia apartir de la imagen
    @param nombre: nombre del CSV
    @param noAlgoritmo: numero de algoritmo aplicado a la imagen
    @param comentario: comentario acerca de la imagen
    @return nada
"""

def escribirCSV(nombre, noAlgoritmo, comentario):
    """ Datos Default para prueba POC """
    
    """ Diccionario de Datos ficticios que se agregaran al CSV """
    
    if (nombre == "" or noAlgoritmo == "" or comentario == ""):
        raise ValueError('Todos los campos deben estar llenos')
        
    diccionario = {'Algorithm Number': [noAlgoritmo], 
        'Obj_quantity': [24], 
        'Precision': [42],
        'Notes': [comentario]}

    """ Columnas de la Estructura del CSV """
    listaColumnas = ['Algorithm Number', 'Obj_quantity', 'Precision', 'Notes']
    
    """" Creando CSV """
    df = pd.DataFrame(diccionario, columns = listaColumnas)
    df.to_csv('C:/Users/Kevin MM/eclipse-workspace/SegmentacionCelulas/static/csv/'
              +nombre+'.csv') #Especificar ruta
    print("Creado con Exito")

"""
    Leer CSV del cual se desea obtener los datos
    @param nombre: nombre del CSV
    @param noAlgoritmo: numero de algoritmo aplicado a la imagen
    @param comentario: comentario acerca de la imagen
    @return nada
"""

def leerCSV(nombreArchivo):
    df = pd.read_csv('C:/Users/Kevin MM/eclipse-workspace/SegmentacionCelulas/static/csv/'
                     +nombreArchivo+'.csv')
    print(df['Algorithm Number'][4] + ' ' + df['Precision'][4]) 
    #Se escoge la columna a leer y lo demas se trata como una lista


""" Pagina Web """

""" Nuevo Objeto """
app = Flask(__name__) 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["STATIC_FOLDER"] = STATIC_FOLDER

"""
    Funcion para la llamada del archivo con los datos de la pagina web 
    @param nada
    @return nada
"""

""" Decorador que contiene la ruta """
@app.route('/', methods = ['GET', 'POST'])
def index():
    """ Llamada al formulario de datos en la pagina web """
    comment_form = forms.CommentForm(request.form)
    title = "Segmentacion de Celulas"   
    
    """ Si se recibe una solicitud POST de la paguina web y las validaciones 
        funcionan se imprimen en pantalla y se genera el documento. Si no 
        si se recibe una solicitud POST de la pagina y se tienen 
        datos en la variable del input con el nombre imgUp 
        se realiza la carga de dichas imagenes """
        
        
    if request.method == 'POST' and comment_form.validate():
        print (comment_form.algoritmo.data)
        print (comment_form.comentario.data)
        print (comment_form.nombreCSV.data)
        escribirCSV(comment_form.nombreCSV.data, comment_form.algoritmo.data, 
                    comment_form.comentario.data)
        print("CSV Generado")

        
    elif request.method == "POST" and "imgUp" in request.files:
        f= request.files.getlist("imgUp")
        fl = []
        # print(f)
        if f[0].filename != "":
            for fn in f:
                fn.save(os.path.join(app.config["STATIC_FOLDER"], fn.filename))
                fn.save(os.path.join(app.config["UPLOAD_FOLDER"], fn.filename))
                send_from_directory(app.config["UPLOAD_FOLDER"], fn.filename)
                fn.filename = "img/" + fn.filename
                # print(fn.filename)
                
                # Se almacena en una lista para futuro procesamiento
                item = imagen.Imagen(fn.filename)
                fl = fl + [item]
                
            print(f)
            ft = listaT(len(f))
            print("Imagenes Cargadas")
            # print ("Objeto Creado")
            # print (fl[0].getImagenes())
            return render_template('index.html', title = title, 
                                   form = comment_form, fp = f[0], filename= f[1:], ft = ft)
        else:
            raise ValueError('No se han seleccionado imagenes para procesar')
        
    """ Renderiza pagina web para ser visualizada """
    return render_template('index.html', title = title, form = comment_form)

""" Corre el servidor 8000 si lo dejo en default es 5000 """

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug= True, port= 8000)
