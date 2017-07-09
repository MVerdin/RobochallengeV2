import controlbluetooth as cbt
import time, os
import picamera
import picamera.array
import numpy as np


cbt.iniciarBT()

tamano_de_archivo=1000
if __name__ == "__main__":
    starting_value = 1

    while True:
        file_name = 'training_data-{0}.npy'.format(starting_value)
        if os.path.isfile(file_name):
            print('File {c} exists, moving along'.format(c=starting_value))
            starting_value += 1
        else:
            print('File {c} does not exist, starting fresh!'.format(c=starting_value))
            break
    datos_para_entrenamiento=[]

    with picamera.PiCamera(sensor_mode=6,resolution=(256,160)) as camera:
        with picamera.array.PiRGBArray(camera) as output:
            while True:
                if cbt.bluetoothConectado.is_set():
                    starttime=time.time()
                    camera.capture(output, 'rgb',True)
                    tiempo=time.time()-starttime
                    fps=1/tiempo
                    comando_actual=cbt.obtenerComando()
                    datos_para_entrenamiento.append([output.array, comando_actual])
                    print(len(datos_para_entrenamiento), "CMD: ", comando_actual, "FPS: ",fps)
                    output.truncate(0)
                    if (len(datos_para_entrenamiento)==tamano_de_archivo):
                        np.save(file_name, datos_para_entrenamiento)
                        print("Guardadas {i} imagenes".format(i=tamano_de_archivo))
                        datos_para_entrenamiento = []
                        starting_value += 1
                        file_name = 'training_data-{0}.npy'.format(starting_value)

                else:
                    print("Control desconectado")
                    time.sleep(1)
