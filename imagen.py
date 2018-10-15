class Imagen:
    def __init__(self, ruta):
        self.ruta = ruta

    def getImagenes(self):
        return self.ruta
    
    def getNombre(self):
        return self.ruta[4:-4]

    def setImagenes(self, ruta):
        self.ruta = ruta
