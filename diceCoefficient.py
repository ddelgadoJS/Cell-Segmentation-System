# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:36:43 2018

@author: Daniel Delgado
"""

from PIL import Image

if __name__ == '__main__':
    imagePath1 = "C:\\Users\\Daniel\\Desktop\\predSelfAlgorithm.png"  
    imagePath2 = "C:\\Users\\Daniel\\Desktop\\predSaulAlgorithm.png"  
    
    img1 = Image.open(imagePath1)
    img2 = Image.open(imagePath2)

    immat1 = img1.load()
    immat2 = img2.load()

    (X, Y) = img1.size
    
    S = 0.0
    commonElements = 0
    immat1Elements = 0
    immat2Elements = 0
    
    for x in range(X):
        for y in range(Y):
            if immat1[(x, y)] != 0:
                immat1[(x, y)] = 1
                immat1Elements += 1
                if immat2[(x, y)] != 0:
                    commonElements += 1
            if immat2[(x, y)] != 0:
                immat2[(x, y)] = 1
                immat2Elements += 1

    print((2 * commonElements) / (immat1Elements + immat2Elements))