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

def VerificarDimensiones(modelo, loteimagenes, lotesalidas):
    return (modelo.input_shape[1:]==loteimagenes.shape[1:]
            and modelo.output_shape[1:]==lotesalidas.shape[1:])

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

    datos_para_entrenamiento = np.load(archivos_encontrados[0])

    imagenes = np.array([dato[0] for dato in datos_para_entrenamiento])
    salidas = np.array([dato[1] for dato in datos_para_entrenamiento])

    if continuarentrenamiento:
        print("Abriendo archivo de modelo")
        if os.path.isfile(ruta_modelo):
            try:
                modelo = keras.models.load_model(ruta_modelo)
            except ValueError:
                print("Archivo invalido")
                return
            if (VerificarDimensiones(modelo,imagenes,salidas)
                print("Modelo cargado correctamente")
            else:
                print("Las dimesiones del modelo no coinciden con las dimensiones de los datos")
                return
        else:
            print("Archivo no encontrado")
            return
    else:
        print("Generando modelo")
        modelo = modelos.GenerarModelo(imagenes.shape[1],imagenes.shape[2],imagenes.shape[3],salidas.shape[1])
        print("Modelo generado correctamente")

if __name__ == "__main__":
    pass
