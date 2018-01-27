#!/usr/bin/env python3

import numpy as np
import cv2

def procesar_img(imagen, lim_inf, lim_sup):
    
    if(imagen.shape[2] == 3):
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    th1, salida_blanco = cv2.threshold(gray, lim_sup, 255, cv2.THRESH_BINARY)
    th2, salida_negro = cv2.threshold(gray, lim_inf, 255, cv2.THRESH_BINARY_INV)
    

    oponente = cv2.add(salida_blanco,salida_negro)
    oponente = cv2.bitwise_not(oponente)

    out = cv2.merge((oponente, gray))
    
    # print("In:",imagen.shape)
    # print("ByN:", gray.shape)
    # print("S3:",oponente.shape)
    # print("Out:",out.shape)

    
    
    if len(oponente.shape) == 2:
        oponente = np.expand_dims(oponente, 2)
    if len(gray.shape) == 2:
        gray = np.expand_dims(gray, 2)

        
    return out