from wtforms import Form
from wtforms import TextField
from wtforms import validators

"""
    Form de Datos para el CSV que recibe un Form
    de parametro con los datos ingresados por el cliente
"""


class CommentForm(Form):
    algoritmo = TextField('No. Algoritmo',
                          [validators.Required
                           (message='Ingrese un numero de algoritmo')])
    comentario = TextField('Comentario',
                           [validators.Required
                            (message='Ingrese un comentario para el CSV')])
    nombreCSV = TextField('Nombre del CSV',
                          [validators.Required
                           (message='Ingrese un nombre para el CSV')])
