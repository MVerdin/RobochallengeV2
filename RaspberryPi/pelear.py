#!/usr/bin/env python3
'''Script de pelea, carga el modelo Keras guardado como "modelo_pelea.h5" en la misma carpeta, lo alimenta con imagenes obtenidas de la camara y usa las predicciones para accionar los motores'''
import sys
import os
import tensorflow.contrib.keras as keras
import picamera
import picamera.array
import numpy as np
sys.path.insert(len(sys.path), os.path.abspath(
    os.path.join(os.getcwd(), os.pardir)))
import configuracion

RESOLUCION_CAMARA, ESCALA_DE_GRISES = configuracion.ObtenerConfigPelea()


def cargar_modelo(ruta):
    print("Abriendo archivo de modelo")
    if os.path.isfile(ruta):
        modelo = keras.models.load_model(ruta)
        print("Modelo cargado correctamente")
    else:
        raise Exception("Archivo no encontrado")
    return modelo


if __name__ == "__main__":
    with picamera.PiCamera(sensor_mode=6, resolution=RESOLUCION_CAMARA) as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb', True)
            print(np.expand_dims(output.array, 0).shape)
