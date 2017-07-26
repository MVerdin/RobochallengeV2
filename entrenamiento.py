#!/usr/bin/env python3

#Punto de entrada para programa de entrenamiento
#Abrir usando python 3
#Dependecias necesarias:
#tensorflow 1.1
#wxPython 4
#h5py
#numpy

#import entrenamientoGUI as egui
#import wx
import tensorflow.contrib.keras as keras
import modelos
import os, time
import numpy as np
from random import shuffle

nombre_de_archivos='training_data-{0}.npy'

def VerificarDimensiones(modelo, loteimagenes, lotesalidas):
    print("Dimensiones:")
    print("Imagenes: {} | Entrada de modelo: {}".format(loteimagenes.shape[1:],modelo.input_shape[1:]))
    print("Salidas: {} | Salida de modelo {}".format(lotesalidas.shape[1:],modelo.output_shape[1:]))
    return (modelo.input_shape[1:]==loteimagenes.shape[1:]
            and modelo.output_shape[1:]==lotesalidas.shape[1:])


def CargarModelo(ruta):
    print("Abriendo archivo de modelo")
    if os.path.isfile(ruta):
        modelo = keras.models.load_model(ruta)
        print("Modelo cargado correctamente")
    else:
        raise Exception("Archivo no encontrado")
    return modelo

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
            archivos_encontrados = [os.path.join(ruta,nombre) for nombre in archivos_encontrados]
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
 lrperzonalizado, optimizador, lr, cambiarpropiedades, epochs):
    def Limpiar():
        keras.backend.clear_session()

    print("Modelo: {} | Optimizador: {} | LR: {} | TB: {} | Datos para ent: {} | Epochs: {}"
          .format(ruta_modelo if continuarentrenamiento else "Nuevo",
                  optimizador if cambiarpropiedades else "Sin modificar",
                  lr if lrperzonalizado else "Sin modificar",
                  tensorboard, ruta_datos, epochs))

    try:
        archivos_entrenamiento = BuscarArchivosEntrenamiento(ruta_datos)
    except Exception as e:
        print(e)
        Limpiar()
        return False

    try:
        imagenes, salidas = CargarySepararArchivo(archivos_entrenamiento[0])

    except Exception as e:
        print(e)
        print("Error al cargar archivo")
        Limpiar()
        return False

    if continuarentrenamiento:
        try:
            modelo = CargarModelo(ruta_modelo)
        except Exception as e:
            print(e)
            Limpiar()
            return False

        if (VerificarDimensiones(modelo,imagenes,salidas)):
            print("Dimensiones correctas")
        else:
            print("Las dimesiones del modelo no coinciden con las dimensiones de los datos")
            Limpiar()
            return False

    else:
        print("Generando modelo nuevo")
        modelo = modelos.GenerarModelo(imagenes.shape[1],imagenes.shape[2],imagenes.shape[3],salidas.shape[1])
        print("Modelo generado correctamente")

    if cambiarpropiedades:
        print("Compilando modelo")
        try:
            if lrperzonalizado:
                if optimizador == "adam":
                    modelo.compile(optimizer=keras.optimizers.Adam(lr=lr),loss="categorical_crossentropy")
                elif optimizador == "sgd":
                    modelo.compile(optimizer=keras.optimizers.SGD(lr=lr),loss="categorical_crossentropy")
            else:
                modelo.compile(optimizer=optimizador,loss="categorical_crossentropy")
        except Exception as e:
            print("Error compilando modelo")
        else:
            print("Modelo compilado correctamente")



    modelo.save(os.path.join(ruta_datos, "modeloPrueba.h5"))
    del modelo
    time.sleep(5)
    print("Entrenamiento terminado")
    Limpiar()
    return True
if __name__ == "__main__":
    pass
