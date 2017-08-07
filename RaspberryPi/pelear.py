#!/usr/bin/env python3
'''Script de pelea, carga el modelo Keras guardado como "modelo_pelea.h5" en la misma carpeta, lo alimenta con imagenes obtenidas de la camara y usa las predicciones para accionar los motores'''
import sys
import os
import tensorflow.contrib.keras as keras
import picamera
import picamera.array
import numpy as np
import cv2

sys.path.insert(len(sys.path), os.path.abspath(
    os.path.join(os.getcwd(), os.pardir)))
import configuracion
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

(RESOLUCION_CAMARA,
    ESCALA_DE_GRISES,
    COMANDOS_MOTORES,
    CANALES_MOTORES,
    IMAGENES_POR_DECISION) = configuracion.ObtenerConfigPelea()

GPIO.cleanup(CANALES_MOTORES)
GPIO.setup(CANALES_MOTORES, GPIO.OUT)


def cargar_modelo(ruta):
    print("Abriendo archivo de modelo")
    if os.path.isfile(ruta):
        modelo = keras.models.load_model(ruta)
        print("Modelo cargado correctamente")
    else:
        raise Exception("Archivo no encontrado")
    return modelo


def verificar_dimensiones(modelo):
    dimensiones_camara = (
        RESOLUCION_CAMARA[1], RESOLUCION_CAMARA[0], 1 if ESCALA_DE_GRISES else 3)
    dimensiones_salida = (len(COMANDOS_MOTORES),)
    print("Dimensiones:")
    print("Camara: {} | Entrada de modelo: {}".format(
        dimensiones_camara, modelo.input_shape[1:]))
    print("Comandos: {} | Salida de modelo {}".format(
        dimensiones_salida, modelo.output_shape[1:]))
    return (modelo.input_shape[1:] == dimensiones_camara
            and modelo.output_shape[1:] == dimensiones_salida)


def tomar_foto():
    with picamera.PiCamera(sensor_mode=6, resolution=RESOLUCION_CAMARA) as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb', True)
            imagen = output.array
            if ESCALA_DE_GRISES:
                imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY) 
            imagen = np.expand_dims(imagen, 0)

    return imagen


def procesar_predicciones(arreglo_predicciones):
    if len(arreglo_predicciones) > 1:
        prediccion = np.mean(arreglo_predicciones, axis=0)
    else:
        prediccion = arreglo_predicciones

    if(len(prediccion) == len(COMANDOS_MOTORES)):
        comando = np.eye(len(COMANDOS_MOTORES), dtype=int)[
            np.argmax(prediccion)]
        if comando in COMANDOS_MOTORES:
            GPIO.output(CANALES_MOTORES, COMANDOS_MOTORES[comando])
        else:
            print("Prediccion invalida")
    else:
        print("Dimensiones de salida invalidas")


def main():
    modelo = cargar_modelo("modelo_pelea.h5")
    if verificar_dimensiones(modelo) is False:
        return

    while True:
        imagenes = tomar_foto()
        while len(imagenes) < IMAGENES_POR_DECISION:
            imagenes = np.concatenate(
                (imagenes, tomar_foto()))

        predicciones = modelo.predict(
            imagenes, batch_size=len(imagenes), verbose=0)

        procesar_predicciones(predicciones)


if __name__ == "__main__":
    main()
    GPIO.cleanup(CANALES_MOTORES)
