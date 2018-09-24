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

class Model:
    
    def __init__(self, datasetCSV):
        """
        Crea el modelo en Keras
        @param datasetCSV: string con el path del csv ("pima-indians-diabetes.data.csv")
        @return model: modelo creado con Keras
        """
        
        # fix random seed for reproducibility
        numpy.random.seed(7)
        
        # load pima indians dataset
        dataset = numpy.loadtxt(datasetCSV, delimiter=",")
        
        # split into input (X) and output (Y) variables
        self.X = dataset[:,0:8]
        self.Y = dataset[:,8]
        
        # create model
        self.model = Sequential()
        self.model.add(Dense(12, input_dim=8, kernel_initializer='uniform', activation='relu'))
        self.model.add(Dense(8, kernel_initializer='uniform', activation='relu'))
        self.model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
        
        # Compile model
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        # Fit the model
        self.model.fit(self.X, self.Y, epochs=150, batch_size=10, verbose=0)
       
        # evaluate the model
        scores = self.model.evaluate(self.X, self.Y, verbose=0)
        print("%s: %.2f%%" % (self.model.metrics_names[1], scores[1]*100))
        
        print("Model created.")

    def writeJSON(self, modelFileName):
        """
        Almacena el modelo a un archivo JSON
        @param modelFileName: string con el nombre del archivo donde se guardara el modelo ("model")
        @return nada
        """
        
        # serialize model to JSON
        modelJSON = self.model.to_json()
        with open(modelFileName + ".json", "w") as json_file:
            json_file.write(modelJSON)
        # serialize weights to HDF5
        self.model.save_weights(modelFileName + ".h5")
        print("Saved model to disk")
        
    def loadJSON(self, modelJSON, modelH5):
        """
        Carga modelo previamente guardado en un archivo JSON
        Archivo JSON debe encontrarse en el mismo directorio del programa
        @param modelJSON: string con el path del JSON ("model.json")
        @param modelH5: string con el path del H5 ("model.h5")
        @return nada
        """
        
        # load json and create model
        jsonFile = open(modelJSON, 'r')
        loaded_model_json = jsonFile.read()
        jsonFile.close()
        loadedModel = model_from_json(loaded_model_json)
        # load weights into new model
        loadedModel.load_weights(modelH5)
        print("Loaded model from disk")
         
        # evaluate loaded model on test data
        loadedModel.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        score = loadedModel.evaluate(self.X, self.Y, verbose=0)
        print("%s: %.2f%%" % (loadedModel.metrics_names[1], score[1]*100))

# Main
model = Model("pima-indians-diabetes.data.csv")
model.writeJSON("model")
model.loadJSON("model.json", "model.h5")