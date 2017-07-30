import sys, os
sys.path.insert(len(sys.path), os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
import configuracion

import tensorflow.contrib.keras as keras
import picamera

resolucion_camara, escala_de_grises = configuracion.ObtenerConfigPelea()
with picamera.PiCamera(sensor_mode=6,resolution=resolucion_camara) as camera:
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, 'rgb',True)
        print(output.shape)
