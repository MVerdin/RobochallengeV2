#!/usr/bin/env python3
import sys, os
sys.path.insert(len(sys.path), os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
import configuracion

import tensorflow.contrib.keras as keras
import picamera
import picamera.array
import numpy as np

resolucion_camara, escala_de_grises = configuracion.ObtenerConfigPelea()
with picamera.PiCamera(sensor_mode=6,resolution=resolucion_camara) as camera:
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, 'rgb',True)
        print(np.expand_dims(output.array,0).shape)
