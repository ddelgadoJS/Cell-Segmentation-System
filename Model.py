"""@package docstring
Aseguramiento de la Calidad del Software
Prueba de Concepto

Estudiantes:
Kevin Giancarlo Montoya Meza - 2015183063
Ignacio Cantillo Valladares - 2016099060
Jose Daniel Delgado Segura - 2015001500
"""

# MLP for Pima Indians Dataset Serialize to JSON and HDF5
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os

def CreateModel():
    """
    Funcion CreateImage()
    @return modelo creado con Keras
    """
    
    # fix random seed for reproducibility
    numpy.random.seed(7)
    # load pima indians dataset
    dataset = numpy.loadtxt("pima-indians-diabetes.data.csv", delimiter=",")
    # split into input (X) and output (Y) variables
    X = dataset[:,0:8]
    Y = dataset[:,8]
    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=8, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(8, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
    # evaluate the model
    scores = model.evaluate(X, Y, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    
    print("Model created.")
    
    return model, X, Y

def ModelToJSON(model):
    """
    Funcion ModelToJSON()
    @param modelo creado previamente en Keras
    @return NONE
    """
    
    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk") 

def LoadJSON(X, Y):
    """
    Funcion LoadJSON()
    Archivo JSON debe encontrarse en el mismo directorio del programa
    @param X, Y
    """
    
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
     
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    score = loaded_model.evaluate(X, Y, verbose=0)
    print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


# Main
resultTuple = CreateModel() # Model at 0, X at 1, Y at 2

ModelToJSON(resultTuple[0])

LoadJSON(resultTuple[1], resultTuple[2])