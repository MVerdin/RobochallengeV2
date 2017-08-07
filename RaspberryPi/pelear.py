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

RESOLUCION_CAMARA, ESCALA_DE_GRISES, COMANDOS_MOTORES = configuracion.ObtenerConfigPelea()


def cargar_modelo(ruta):
    print("Abriendo archivo de modelo")
    if os.path.isfile(ruta):
        modelo = keras.models.load_model(ruta)
        print("Modelo cargado correctamente")
    else:
        raise Exception("Archivo no encontrado")
    return modelo

def verificar_dimensiones(modelo):
    dimensiones_camara = (RESOLUCION_CAMARA[1],RESOLUCION_CAMARA[0],1 if ESCALA_DE_GRISES else 3)
    dimensiones_salida = (len(COMANDOS_MOTORES),)
    print("Dimensiones:")
    print("Camara: {} | Entrada de modelo: {}".format(dimensiones_camara,modelo.input_shape[1:]))
    print("Comandos: {} | Salida de modelo {}".format(dimensiones_salida,modelo.output_shape[1:]))
    return (modelo.input_shape[1:]==dimensiones_camara
            and modelo.output_shape[1:]==dimensiones_salida)

if __name__ == "__main__":
    modelo = cargar_modelo("modelo_pelea.h5")
    
    with picamera.PiCamera(sensor_mode=6, resolution=RESOLUCION_CAMARA) as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb', True)
            print(np.expand_dims(output.array, 0).shape)
