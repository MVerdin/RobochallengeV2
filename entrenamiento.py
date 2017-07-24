#!/usr/bin/env python3

#Punto de entrada para programa de entrenamiento
#Abrir usando python 3
#Dependecias necesarias:
#tensorflow 1.1
#wxPython 4
#h5py
#numpy

import entrenamientoGUI as egui
import wx
import tensorflow.contrib.keras as keras
import modelos
import os
import numpy as np
from random import shuffle
contador=0

nombre_de_archivos='training_data-{0}.npy'

def VerificarDimensiones(modelo, loteimagenes, lotesalidas):
    return (modelo.input_shape[1:]==loteimagenes.shape[1:]
            and modelo.output_shape[1:]==lotesalidas.shape[1:])

def CargarModelo(ruta):
    print("Abriendo archivo de modelo")
    if os.path.isfile(ruta):
        modelo = keras.models.load_model(ruta)
    else:
        raise Exception("Archivo no encontrado")

def BuscarArchivosEntrenamiento(ruta):
    if os.path.isdir(ruta):
        print("Buscando datos para entrenamiento")
        archivos_encontrados = [nombre_archivo for nombre_archivo
                               in os.listdir(ruta)
                               if nombre_archivo.startswith(nombre_de_archivos.split("-")[0])
                               and nombre_archivo.endswith(nombre_de_archivos.split(".")[1])]
        if(len(archivos_encontrados)!=0):
            print("Archivos encontrados:", len(archivos_encontrados))
            for archivo in sorted(archivos_encontrados):
                print(archivo)
            archivos_encontrados = [ruta + "/" + nombre for nombre in archivos_encontrados]
            shuffle(archivos_encontrados)
            return archivos_encontrados
        else:
            raise Exception("No se encontraron archivos")
    else:
        raise Exception("Carpeta no encontrada")

def CargarySepararArchivo(ruta_archivo):
    datos_para_entrenamiento = np.load(ruta_archivo)
    imagenes = np.array([dato[0] for dato in datos_para_entrenamiento])
    salidas = np.array([dato[1] for dato in datos_para_entrenamiento])
    return imagenes, salidas

#Funcion de entrenamiento
def Entrenar(ruta_modelo, ruta_datos, tensorboard, continuarentrenamiento,
 lrperzonalizado, optimizador, lr, cambiarpropiedades):
    print("Modelo: {} | Optimizador: {} | LR: {} | TB: {} | Datos para ent: {}".format(ruta_modelo, optimizador, lr, tensorboard, ruta_datos))

    try:
        archivos_entrenamiento = BuscarArchivosEntrenamiento(ruta_datos)
    except Exception as e:
        print(e)
        return

    imagenes, salidas = CargarySepararArchivo(archivos_entrenamiento[0])

    if continuarentrenamiento:
        try:
            modelo = CargarModelo(ruta_modelo)
        except Exception as e:
            print(e)
            return

        if (VerificarDimensiones(modelo,imagenes,salidas)):
            print("Dimensiones correctas")
        else:
            print("Las dimesiones del modelo no coinciden con las dimensiones de los datos")
            return

    else:
        print("Generando modelo")
        modelo = modelos.GenerarModelo(imagenes.shape[1],imagenes.shape[2],imagenes.shape[3],salidas.shape[1])
        print("Modelo generado correctamente")

if __name__ == "__main__":
    pass
