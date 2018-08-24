from wtforms import Form
from wtforms import TextField
from wtforms import validators

class CommentForm(Form):
    algoritmo = TextField('No. Algoritmo', [validators.Required(message = 'Ingrese un numero de algoritmo')])
    comentario = TextField('Comentario', [validators.Required(message = 'Ingrese un nombre para el CSV')])
    nombreCSV = TextField ('Nombre del CSV', [validators.Required(message = 'Ingrese un nombre para el CSV')])
