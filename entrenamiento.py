#!/usr/bin/env python3

#Punto de entrada para programa de entrenamiento
#Abrir usando python 3
#Dependecias necesarias:
#tensorflow 1.1
#wxPython 4
#h5py
#...

import entrenamientoGUI as egui
import wx
import tensorflow.contrib.keras as keras
import modelos
import os
contador=0

nombre_de_archivos='training_data-{0}.npy'

#Funcion de entrenamiento
def Entrenar(ruta_modelo, ruta_datos, tensorboard, continuarentrenamiento,
 lrperzonalizado, optimizador, lr, cambiarpropiedades):
    print("Modelo: {} | Optimizador: {} | LR: {} | TB: {} | Datos para ent: {}".format(ruta_modelo, optimizador, lr, tensorboard, ruta_datos))

    if os.path.isdir(ruta_datos):
        print("Buscando datos para entrenamiento")
        archivos_encontrados = sorted([nombre_archivo for nombre_archivo
                               in os.listdir(ruta_datos)
                               if nombre_archivo.startswith(nombre_de_archivos.split("-")[0])
                               and nombre_archivo.endswith(nombre_de_archivos.split(".")[1])])
        if(len(archivos_encontrados)!=0):
            print("Archivos encontrados:", len(archivos_encontrados))
            #print(archivos_encontrados)
        else:
            print("No se encontraron archivos")
            return
    else:
        print("Carpeta no encontrada")
        return


    if continuarentrenamiento:
        print("Abriendo archivo de modelo")
        if os.path.isfile(ruta_modelo):
            try:
                modelo = keras.models.load_model(ruta_modelo)
            except ValueError:
                print("Archivo invalido")
                return
        else:
            print("Archivo no encontrado")
            return
    else:
        print("Generando modelo")
        modelo = modelos.GenerarModelo()

if __name__ == "__main__":
    pass
