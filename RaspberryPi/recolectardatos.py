#!/usr/bin/env python3

import sys
import time
import os
sys.path.insert(len(sys.path), os.path.abspath(
    os.path.join(os.getcwd(), os.pardir)))
import configuracion
import controlbluetooth as cbt
import picamera
import picamera.array
import cv2
import numpy as np
import RPi.GPIO as GPIO
import led

(NOMBRE_DE_ARCHIVOS,
 MUESTRAS_POR_ARCHIVO,
 RESOLUCION_CAMARA,
 ESCALA_DE_GRISES,
 CMD2ONEHOT,
 PIN_INTERRUPTOR,
 CANALES_LED_RGB) = configuracion.ObtenerConfigRecoleccion()

GPIO.cleanup(CANALES_LED_RGB)
GPIO.cleanup(PIN_INTERRUPTOR)
led_estado = led.LEDEstado(CANALES_LED_RGB,"apagado")

cbt.iniciarBT()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_INTERRUPTOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buscar_unidad_usb():
    if len(os.listdir("/media")) == 1:
        if len(os.listdir(os.path.join("/media",os.listdir("/media")[0]))) == 1:
            print("Unidad USB encontrada")
            ruta = os.path.join("/media", 
                                os.listdir("/media")[0], 
                                os.listdir(os.path.join("/media",os.listdir("/media")[0]))[0])
            return ruta
    print("Unidad USB no encontrada")

def obtener_ruta_de_guardado():
    ruta_unidad_usb = buscar_unidad_usb()
    if ruta_unidad_usb is not None:
        return ruta_unidad_usb
    else:
        if not os.path.isdir("Datos"):
            os.mkdir(os.path.join(os.getcwd(),"Datos"))

        nombre_carpeta="datos-{}{}{}-{}{}{}".format(str(tiempo.year).zfill(4),
                                                    str(tiempo.month).zfill(2),
                                                    str(tiempo.day).zfill(2),
                                                    str(tiempo.hour).zfill(2),
                                                    str(tiempo.minute).zfill(2),
                                                    str(tiempo.second).zfill(2))
        ruta_carpeta=os.path.join(os.getcwd(),"Datos",nombre_carpeta)
        os.mkdir(ruta_carpeta)
        return ruta_carpeta



if __name__ == "__main__":
    starting_value = 1

    while True:
        file_name = NOMBRE_DE_ARCHIVOS.format(starting_value)
        if os.path.isfile(file_name):
            print('Archivo {c} ya existe, buscando siguiente'.format(
                c=starting_value))
            starting_value += 1
        else:
            print('Archivo {c} no existe, empezando'.format(c=starting_value))
            break
    datos_para_entrenamiento = []

    with picamera.PiCamera(sensor_mode=6, resolution=RESOLUCION_CAMARA) as camera:
        with picamera.array.PiRGBArray(camera) as output:
            while True:
                if cbt.bluetoothConectado.is_set() and not GPIO.input(PIN_INTERRUPTOR):
                    starttime = time.time()
                    led_estado.cambiar_estado("encendido")
                    camera.capture(output, 'rgb', True)
                    imagen = output.array
                    if ESCALA_DE_GRISES:
                        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                        imagen = np.expand_dims(imagen, 2)
                    comando_actual = np.array(CMD2ONEHOT[cbt.obtenerComando()])
                    datos_para_entrenamiento.append([imagen, comando_actual])
                    output.truncate(0)
                    if (len(datos_para_entrenamiento) == MUESTRAS_POR_ARCHIVO):
                        np.save(file_name, datos_para_entrenamiento)
                        print("Guardadas {i} imagenes".format(
                            i=MUESTRAS_POR_ARCHIVO))
                        datos_para_entrenamiento = []
                        starting_value += 1
                        file_name = NOMBRE_DE_ARCHIVOS.format(starting_value)

                    tiempo = time.time() - starttime
                    fps = 1 / tiempo
                    print(len(datos_para_entrenamiento),
                          "CMD: ", comando_actual, "FPS: ", fps)
                else:
                    #print("Control desconectado")
                    led_estado.cambiar_estado("listo")
                    time.sleep(1)
