class Imagen:
    def __init__(self, ruta):
        self.ruta = ruta
    
    def getImagenes(self):
        return self.ruta
    
    def setImagenes(self, ruta):
        self.ruta = ruta