from wtforms import Form
from wtforms import TextField
from wtforms import validators

"""
    Form de Datos para el CSV que recibe un Form
    de parametro con los datos ingresados por el cliente
"""


class CommentForm(Form):
    procedimiento = TextField('No. Procedimiento',
                          [validators.Required
                           (message='Ingrese un numero de procedimiento')])
    nombreCSV = TextField('Nombre del CSV',
                          [validators.Required
                           (message='Ingrese un nombre para el CSV')])
