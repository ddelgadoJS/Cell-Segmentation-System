from keras.preprocessing import image
import matplotlib.pyplot as plt

def LoadImage(path):
    img = image.img_to_array(image.load_img(path, grayscale = False, target_size = None))
    
    return img

def ShowImage(img):
    
    plt.imshow(img/255.)
    plt.show()
    
img = LoadImage("image.jpg")
ShowImage(img)