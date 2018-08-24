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

def LoadImage(path):
    """
    Funcion LoadImage()
    @param path a imagen
    @return imagen convertida a array
    """
    
    img = image.img_to_array(image.load_img(path, grayscale = False, target_size = None))
    
    return img

def ShowImage(img):
    """
    Funcion ShowImage()
    @param array de imagen
    @return NONE
    """
    
    plt.imshow(img/255.)
    plt.show()
    
img = LoadImage("image.jpg")
ShowImage(img)