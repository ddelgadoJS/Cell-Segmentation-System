"""@package docstring
Aseguramiento de la Calidad del Software
Prueba de Concepto

Estudiantes:
Kevin Giancarlo Montoya Meza - 2015183063
Ignacio Cantillo Valladares - 2016099060
Jose Daniel Delgado Segura - 2015001500
"""

from keras.preprocessing import image
import matplotlib.pyplot as plt

import scipy.misc

def LoadImage(file_name):
    """
    Carga imagen en un Numpy array 
    @param file_name: path a imagen por cargar
    @return image_array: imagen convertida a Numpy array
    """
    
    image_array = image.img_to_array(image.load_img(file_name, grayscale = False, target_size = None))
    
    return image_array

def ShowImage(image_array):
    """
    Muestra imagen de un Numpy array en pantalla
    @param image_array: imagen almacenada en un Numpy array
    @return nada
    """
    
    plt.imshow(image_array/255.)
    plt.show()
    
def SaveImage(file_name, image_array):
    """
    Guarda una imagen en un Numpy array a un archivo jpg
    @param file_name: 'image/folder/image_name'
    @param image_array: imagen almacenada en un Numpy array
    :return: nada
    """
    scipy.misc.imsave(file_name + ".jpg", image_array)
    
image_array = LoadImage("image.jpg")
ShowImage(image_array)
SaveImage("test_name", image_array)