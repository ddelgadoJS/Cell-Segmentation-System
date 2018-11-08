# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:36:43 2018

@author: Daniel Delgado
"""

from PIL import Image
from os import listdir

if __name__ == '__main__':
    predictionsDirectory = "PREDICTIONSFOLDER"
    groundTruthDirectory = "GROUNDTRUTHFOLDER"
    predictionsFiles = listdir(predictionsDirectory)
    groundtruthFiles = listdir(groundTruthDirectory)
    
    diceCoefficients = []
   
    for i in range(0, len(predictionsFiles)):
        imgPathPred = predictionsFiles[i]
        imgPathGT = groundtruthFiles[i]

        imgPred = Image.open(predictionsDirectory + imgPathPred)
        imgGT = Image.open(groundTruthDirectory + imgPathGT)

        immatPred = imgPred.load()
        immatGT = imgGT.load()

        (X, Y) = imgPred.size
    
        S = 0.0
        commonElements = 0
        immatPredElements = 0
        immatGTElements = 0
    
        for x in range(X):
            for y in range(Y):
                if immatPred[(x, y)] != 0:
                    immatPred[(x, y)] = 1
                    immatPredElements += 1
                    if immatGT[(x, y)] != 0:
                        commonElements += 1
                if immatGT[(x, y)] != 0:
                    immatGT[(x, y)] = 1
                    immatGTElements += 1
                    
        diceCoefficients.append((predictionsFiles[i], groundtruthFiles[i], (2 * commonElements) / (immatPredElements + immatGTElements)))