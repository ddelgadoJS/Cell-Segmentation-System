"""@package docstring
Aseguramiento de la Calidad del Software
Prueba de Concepto

Estudiantes:
Kevin Giancarlo Montoya Meza - 2015183063
Ignacio Cantillo Valladares - 2016099060
Jose Daniel Delgado Segura - 2015001500
"""

from keras.preprocessing import image as kImage
import matplotlib.pyplot as plt
import scipy.misc


class Images:
    
    def loadImage(self, fileName):
        """
        Carga imagen en un Numpy array 
        @param fileName: path a imagen por cargar
        @return image_array: imagen convertida a Numpy array
        """
        
        self.im = kImage.load_img(fileName,
                                  color_mode="grayscale",
                                  target_size=None)
        self.imageArray = kImage.img_to_array(self.im)
        
        # For the tests
        total = 0        
        for i in range(self.imageArray.shape[0]):
            for j in range(self.imageArray.shape[1]):
                total += int(self.imageArray[i][j])
                
        return total
        
    def showImage(self):
        """
        Muestra imagen de un Numpy array en pantalla
        @return nada
        """
        
        plt.imshow(self.imageArray/255.)
        plt.show()
        
    def saveImage(self, fileName):
        """
        Guarda una imagen en un Numpy array a un archivo jpg
        @param file_name: 'image/folder/image_name'
        @param image_array: imagen almacenada en un Numpy array
        @return: nada
        """
        scipy.misc.imsave(fileName + ".jpg", self.imageArray)
  
    
#image = Images()
#print(image.loadImage("WhitePixels.jpg"))
#image.showImage()
#image.saveImage("Hello")