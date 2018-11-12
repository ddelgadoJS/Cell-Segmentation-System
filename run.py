from flask import Flask
from flask import render_template
from flask import request
import os
import forms
import imagen
import pandas as pd

import numpy as np

from cellPostProcess import mainFunc
from cellPostProcess import predictTime

from PIL import Image
from keras.models import Model
from keras.layers import Input
from keras.layers import concatenate
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Conv2DTranspose
from keras.optimizers import Adam
from keras import backend as K
from flask.helpers import flash
from os import listdir
import timeit

UPLOAD_FOLDER = os.path.abspath("./uploads/")
STATIC_FOLDER = os.path.abspath("./static/img")

# Set channel configuration for backend
K.set_image_data_format('channels_last')

# Image size
img_rows = 256
img_cols = 256
# Dice coeficient parameter
smooth = 1.
# Paths declaration
image_path = os.path.abspath("raw/hoechst/test/*.png")
weights_path = os.path.abspath("weights/pre_0_3_5.h5")
pred_dir = os.path.abspath("preds/")

"""
@package docstring
Aseguramiento de la Calidad del Software

Estudiantes:
Kevin Giancarlo Montoya Meza - 2015183063
Ignacio Cantillo Valladares - 2016099060
Jose Daniel Delgado Segura - 2015001500

"""

def diceCoefficients():
    predictionsDirectory = ".\\Documents\\dice\\Predictions\\"
    groundTruthDirectory = ".\\Documents\\dice\\GTResized\\"
    predictionsFiles = listdir(predictionsDirectory)
    groundtruthFiles = listdir(groundTruthDirectory)

    diceCoefficients = []

    for i in range(0, len(predictionsFiles)):
        imgPathPred = predictionsFiles[i]
        imgPathGT = groundtruthFiles[i]

        imgPred = Image.open(predictionsDirectory + imgPathPred)
        imgGT = Image.open(groundTruthDirectory + imgPathGT)

        immatPred = imgPred.load()
        immatGT = imgGT.load()

        (X, Y) = imgPred.size

        S = 0.0
        commonElements = 0
        immatPredElements = 0
        immatGTElements = 0

        for x in range(X):
            for y in range(Y):
                if immatPred[(x, y)] != 0:
                    immatPred[(x, y)] = 1
                    immatPredElements += 1
                    if immatGT[(x, y)] != 0:
                        commonElements += 1
                if immatGT[(x, y)] != 0:
                    immatGT[(x, y)] = 1
                    immatGTElements += 1

        diceCoefficients.append((predictionsFiles[i], groundtruthFiles[i], (2 * commonElements) / (immatPredElements + immatGTElements)))
    return diceCoefficients

# Compute dice coeficient used in loss function
def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) +
                                           K.sum(y_pred_f) + smooth)


# Loss function
def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)


# Load test data from directory
def load_test_data(image_path):
    raw = []
    image_filename = dict()
    count = 0
    
    if len(image_path) == 0:
        raise ValueError ("Error al obtener las imagenes")
    
    for filename in image_path:
        name = filename.filename[4:-4]
        print("name", name)
        try:
            im = Image.open(filename)
            im = im.convert('L')
            im = im.resize((img_rows, img_cols))
            raw.append(np.array(im))
            image_filename[count] = name
            count += 1
            im.close()
        except IOError:
            print('Error loading image ', filename)
    return [raw, image_filename]


# Preprocess loaded images
def preprocess(imgs):
    if len(imgs) == 0:
        raise ValueError ("Error en las imagenes")
    imgs_p = np.ndarray((len(imgs), img_rows, img_cols), dtype=np.float32)
    for i in range(len(imgs)):
        imgs_p[i] = imgs[i].reshape((img_rows, img_cols))/255.

    imgs_p = imgs_p[..., np.newaxis]

    # Perform data normalization
    mean = imgs_p.mean()
    std = imgs_p.std()
    imgs_p -= mean
    imgs_p /= std

    return imgs_p


# Define unet architecture
def get_unet():
    inputs = Input((img_rows, img_cols, 1))
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)
    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)

    up6 = concatenate([Conv2DTranspose(256, (2, 2), strides=(2, 2),
                                       padding='same')(conv5), conv4], axis=3)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(up6)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)

    up7 = concatenate([Conv2DTranspose(128, (2, 2), strides=(2, 2),
                                       padding='same')(conv6), conv3], axis=3)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(up7)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)

    up8 = concatenate([Conv2DTranspose(64, (2, 2), strides=(2, 2),
                                       padding='same')(conv7), conv2], axis=3)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(up8)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv8)

    up9 = concatenate([Conv2DTranspose(32, (2, 2), strides=(2, 2),
                                       padding='same')(conv8), conv1], axis=3)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(up9)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv9)

    conv10 = Conv2D(1, (1, 1), activation='sigmoid')(conv9)

    model = Model(inputs=[inputs], outputs=[conv10])

    model.compile(optimizer=Adam(lr=1e-4), loss=dice_coef_loss,
                  metrics=[dice_coef])

    return model


def predict(ruta):
    print('-'*30)
    print('Loading and preprocessing test data...')
    print('-'*30)

    if len(ruta) == 0:
        raise ValueError("Error al cargar las imagenes")

    # Load test data
    cell_segmentation_data = load_test_data(ruta)

    # Preprocess and reshape test data
    
    if len(cell_segmentation_data) == 0:
        raise ValueError("Error en el retorno del procesamiento")
    x_test = preprocess(cell_segmentation_data[0])
    test_id = cell_segmentation_data[1]

    print('-'*30)
    print('Creating and compiling model...')
    print('-'*30)
    # Get model
    model = get_unet()

    print('-'*30)
    print('Loading saved weights...')
    print('-'*30)
    
    if len(weights_path) == 0:
        raise ValueError("Error en la carga de los pesos")
    
    # Load weights
    model.load_weights(weights_path)

    print('-'*30)
    print('Predicting masks on test data...')
    print('-'*30)
    # Make predictions
    imgs_mask_predict = model.predict(x_test, verbose=1)

    print('-' * 30)
    print('Saving predicted masks to files...')
    np.save('imgs_mask_predict.npy', imgs_mask_predict)
    print('-' * 30)
    if not os.path.exists(pred_dir):
        os.mkdir(pred_dir)
    # Save predictions as images
    flp = []
    for image_pred, index in zip(imgs_mask_predict, range(x_test.shape[0])):
        image_pred = image_pred[:, :, 0]
        image_pred[image_pred > 0.5] *= 255.
        im = Image.fromarray(image_pred.astype(np.uint8))
        flp = flp + [str(test_id[index]) + '_pred.png']
        im.save(os.path.join(pred_dir, str(test_id[index]) + '_pred.png'))
        im.save(os.path.join(app.config["STATIC_FOLDER"],
                             str(test_id[index]) + '_pred.png'))

    K.clear_session()

    return flp


""" Nuevo Objeto """
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["STATIC_FOLDER"] = STATIC_FOLDER


""""
    Crear Lista para manejo de imagenes en aplicacion web
    @param tam: tamanno de la lista que se desea construir
    @return l: lista construida
"""


def listaT(tam):
    cont = 1
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
    @param noProcedimiento: numero de procedimiento aplicado a la imagen
    @return nada
"""

def escribirDice(dc):
    diccionario = {'Prediction': [value[0] for value in dc],
                   'Ground Truth': [value[1] for value in dc],
                   'Percentage': [value[2] for value in dc]}

    """ Columnas de la Estructura del CSV """
    listaColumnas = ['Prediction', 'Ground Truth', 'Percentage']

    """" Creando CSV """
    df = pd.DataFrame(diccionario, columns=listaColumnas)
    df.to_csv( STATIC_FOLDER[:-4] + '/csv/' + 
              "CoeficienteDice" + '.csv')   # Especificar ruta
    print("Creado con Exito")

def escribirCSV(nombre, noProcedimiento, cellsArea, cellsCenter, imageName):
    """ Datos Default para prueba POC """
    """ Diccionario de Datos ficticios que se agregaran al CSV """
    if (nombre == "" or noProcedimiento == "" or nombre == None or noProcedimiento == None):
        raise ValueError('Todos los campos deben estar llenos')
    elif (cellsArea == [] or cellsCenter == []):
        raise ValueError('Datos no validos')
    diccionario = {'Cell Number': list(range(1, len(cellsArea))),
                   'Area': cellsArea[1:],
                   'Center': cellsCenter[1:]}

    """ Columnas de la Estructura del CSV """
    listaColumnas = ['Cell Number', 'Area', 'Center']

    """" Creando CSV """
    df = pd.DataFrame(diccionario, columns=listaColumnas)
    df.to_csv( STATIC_FOLDER[:-4] + '/csv/' + 
              nombre + "(" + imageName + ")" + "(" + noProcedimiento + ")" + '.csv')   # Especificar ruta
    print("Creado con Exito")

"""
    Leer CSV del cual se desea obtener los datos
    @param nombre: nombre del CSV
    @param noProcedimiento: numero de procedimiento aplicado a la imagen
    @return nada
"""


def leerCSV(nombreArchivo):
    df = pd.read_csv('C:/Users/Kevin MM/eclipse-workspace/' +
                     'SegmentacionCelulas/static/csv/' +
                     nombreArchivo + '.csv')
    print(df['Algorithm Number'][4] + ' ' + df['Precision'][4])
    # Se escoge la columna a leer y lo demas se trata como una lista


""" Pagina Web """

"""
    Funcion para la llamada del archivo con los datos de la pagina web
    @param nada
    @return nada
"""

""" Decorador que contiene la ruta """


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Llamada al formulario de datos en la pagina web """
    comment_form = forms.CommentForm(request.form)
    title = "Segmentacion de Celulas"
    dc = diceCoefficients()
    escribirDice(dc)
    
    av = 0
            
    for j in dc:
        av += j[2]
                
    av /= len(dc)
    
    """ Si se recibe una solicitud POST de la paguina web y las validaciones
        funcionan se imprimen en pantalla y se genera el documento. Si no
        si se recibe una solicitud POST de la pagina y se tienen
        datos en la variable del input con el nombre imgUp
        se realiza la carga de dichas imagenes """


    if request.method == "POST" and "imgUp" in request.files:
        f = request.files.getlist("imgUp")
        fl = []
        print(f)
        if f[0].filename != "":
            for fn in f:
                fn.save(os.path.join(app.config["STATIC_FOLDER"], fn.filename))
                # fn.save(os.path.join(app.config["UPLOAD_FOLDER"],fn.filename))
                # send_from_directory(app.config["UPLOAD_FOLDER"],fn.filename)
                fn.filename = "img/" + fn.filename
                # print(fn.filename)
 
                # Se almacena en una lista para futuro procesamiento
                item = imagen.Imagen(fn.filename)
                fl = fl + [item]
 
            # print(f)
            ft = listaT(len(f))
            print("Imagenes Cargadas")
            # print ("Objeto Creado")
            # print (fl[0].getImagenes())
 
            start = timeit.default_timer()
            flp = predict(f)
 
            i = 0
            while i < len(flp):
                flp[i] = "img/" + flp[i]
                i += 1
                
            print("SEGMENTATION PROCESS: ", flp)
  
            # POST PROCESS

            for pl in flp:
                print("HOLA", pred_dir + "/" + pl[4:], pl[4:])
                cellArea, cellCenter = mainFunc(pred_dir + "/" + pl[4:], pl[4:])
                escribirCSV(comment_form.nombreCSV.data, comment_form.procedimiento.data, cellArea, cellCenter, pl[4:-4])
            
            print("ADIOS" ,cellArea, cellCenter)
                # mainFunc("C:\\Users\\Kevin MM\\eclipse-workspace\\SegmentacionCelulas\\preds\\2_pred.png", "2_pred.png")
            
            flash("CSV de Resultados generado con exito")
            
            i = 0
            while i < len(flp):
                flp[i] = "img/post_" + flp[i][4:]
                i += 1
                
            print("POST SEGMENTATION PROCESS: ", flp)
            
            print("DICE COEFFICIENT", dc)
            
            paths = []
            
            i = 0
            while i < len(flp):
                paths += [STATIC_FOLDER + "\\" + flp[i][4:]]
                i += 1
            
            times = []
            times, totalTime = predictTime(paths, start)
            
            flash("Tiempo total de Ejecucion: " + str(format(totalTime, 'f')))
            
            i = 0
            while i < len(flp):
                flp[i] = [flp[i], times[i]]
                i += 1

            
            return render_template('index.html', title=title,
                                   form=comment_form, av=av, fp=f[0],
                                   filename=f[1:], ft=ft, fpp=flp[0],
                                   filenameP=flp[1:])
        else:
            raise ValueError('No se han seleccionado imagenes para procesar')

    """ Renderiza pagina web para ser visualizada """
    return render_template('index.html', title=title, form=comment_form, av=av)

""" Corre el servidor 8000 si lo dejo en default es 5000 """
        
if __name__ == '__main__':
    app.secret_key = 'nothing'
    app.run(host='0.0.0.0', debug=True, port=8000)
    
