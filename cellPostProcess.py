# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:36:43 2018

@author: Daniel
"""

from random import randint
import numpy as np
from pylab import *
from PIL import Image
from scipy.ndimage import measurements

# Taken from 
# https://stackoverflow.com/questions/25664682/
# how-to-find-cluster-sizes-in-2d-numpy-array
def getCellCenter(immat, X, Y):
    m = np.zeros((X, Y))
    
    for x in range(X):
        for y in range(Y):
            m[x, y] = immat[(x, y)] != 0
    m = m / np.sum(np.sum(m))
    
    # Marginal distributions
    dx = np.sum(m, 1)
    dy = np.sum(m, 0)
    
    # Expected values
    cx = np.sum(dx * np.arange(X))
    cy = np.sum(dy * np.arange(Y))
    
    return (cx, cy)

def countCells(clusteredArray, X, Y):
    numCells = 0
    for x in range(X):
        for y in range(Y):
            if clusteredArray[x, y] > numCells:
                numCells = clusteredArray[x, y]
    return numCells

def getRandomColor():
    return ((randint(0, 255), randint(0, 255), randint(0, 255), 255))

# Counts, gets the area, gets the centroid and labels cells
# Works with predictions, with raw images may generate inconsistencies
# [labelCells] = boolean to know if user wants to label and color the cells
def cellPostProcess(image_path, labelCells = False):
    img = Image.open(image_path)
    rgbimg = Image.new("RGBA", img.size)
    rgbimg.paste(img)
    
    immat = rgbimg.load()

    (X, Y) = rgbimg.size
    m = np.zeros((X, Y))
    slicedIm = np.zeros((X, Y))
    
    for x in range(X):
        for y in range(Y):
            # To find the clusters 
            if immat[(x, y)] != (0, 0, 0, 255):
                m[x, y] = 1
    
    # Making clusters
    lw, num = measurements.label(m)
    np.set_printoptions(threshold=np.nan)
    
    # Getting number of cells
    cellsCount = countCells(lw, X, Y)
    
    # This is an array containing the area of each cell, in order
    # The first element represents the image black area
    cellsArea = measurements.sum(m, lw, index=arange(lw.max() + 1))
    
    for cell in range(1, cellsCount+1):
        cellColor = getRandomColor()
        for y in range(Y):
            for x in range(X):
                if lw[x, y] == cell:
                    slicedIm[x, y] = 1
                    if labelCells: immat[(x, y)] = cellColor
                
        immat[getCellCenter(slicedIm, X, Y)] = (255, 0, 0, 255)
        slicedIm = np.zeros((X, Y))
    
    # Kevin, please, rename this correctly
    # This is the file that should be showed
    rgbimg.save('centerIm.png')            

if __name__ == '__main__':
    cellPostProcess('C:\\Users\\Daniel\\Desktop\\preds\\1_pred.png', True)
    print("Done :)")