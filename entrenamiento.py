#!/usr/bin/env python3
'''Modulo con funciones necesarias para llevar a cabo el entrenamiento del modelo'''
#Dependecias necesarias:
#tensorflow 1.1
#wxPython 4
#h5py
#numpy

#import entrenamientoGUI as egui
import wx.lib.newevent
import sys, os, threading
from math import ceil
import configuracion
import datetime, time
#import keras
import tensorflow.contrib.keras as keras
import modelos
import numpy as np
from random import shuffle

if __name__ != "__main__":
    import wx
    import entrenamientoGUI as gui
    myEVT_ENTRENAMIENTO = wx.NewEventType()
    EVT_ENTRENAMIENTO = wx.PyEventBinder(myEVT_ENTRENAMIENTO, 1)
    seguirEntrenamiento = threading.Event()

    EventoActualizarGraficas, EVT_ACTUALIZAR_GRAFICAS = wx.lib.newevent.NewEvent()

NOMBRE_ARCHIVOS = configuracion.NOMBRE_DE_ARCHIVOS


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
                               if nombre_archivo.startswith(NOMBRE_ARCHIVOS.split("-")[0])
                               and nombre_archivo.endswith(NOMBRE_ARCHIVOS.split(".")[1])]
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


def CargarySepararArchivos(lista_archivos, ARCHIVOS_POR_ENTRENAMIENTO):
    for i in range(ceil(len(lista_archivos)/ARCHIVOS_POR_ENTRENAMIENTO)):
        archivos = lista_archivos[:ARCHIVOS_POR_ENTRENAMIENTO]
        print("Cargando archivos:")
        for a in archivos:
            print(a)
        datos_para_entrenamiento = np.load(archivos[0])
        if len(archivos)>1:
            for archivo in archivos[1:]:
                datos_para_entrenamiento = np.concatenate((datos_para_entrenamiento, np.load(archivo)))
        del lista_archivos[:ARCHIVOS_POR_ENTRENAMIENTO]
        print("Muestras:", len(datos_para_entrenamiento))
        imagenes = np.array([dato[0] for dato in datos_para_entrenamiento])
        salidas = np.array([dato[1] for dato in datos_para_entrenamiento])
        yield imagenes, salidas

class RecolectorDatos(keras.callbacks.Callback):
    def __init__(self, ventana):
        self.ventana= ventana
        self.perdidas=[]
        self.precisiones=[]
        self.perdidas_promedio=[]
        self.precisiones_promedio=[]
    def on_batch_end(self, batch, logs=None):
        perdida=logs["loss"]
        precision=logs["acc"]
        tiempo=time.time()
        #print("\n","Perdida:",perdida)
        #print("Precision:",logs["acc"])
        self.perdidas.append((tiempo,perdida))
        self.precisiones.append((tiempo,precision))
        self.perdidas_promedio.append((tiempo, 
            float(sum([x[1] for x in self.perdidas])) / max(len([x[1] for x in self.perdidas]), 1)))
        self.precisiones_promedio.append((tiempo,
            float(sum([x[1] for x in self.precisiones])) / max(len([x[1] for x in self.precisiones]), 1)))
        evt = EventoActualizarGraficas(recolector=self)
        wx.PostEvent(self.ventana, evt)
        



def EntrenarModelo(modelo, ruta_guardar, imagenes, salidas, epochs, tensorboard, recolector_datos):
    if seguirEntrenamiento.is_set():
        if tensorboard:
            print("TensorBoard no disponible")
            modelo.fit(x=imagenes, y=salidas, epochs=epochs, validation_split=0.01, callbacks = [recolector_datos])
        else:
            modelo.fit(x=imagenes, y=salidas, epochs=epochs, validation_split=0.01)
        tiempo=datetime.datetime.today()
        nombre_de_archivo="modelo-{}{}{}-{}{}{}.h5 guardado".format(str(tiempo.year).zfill(4),
                                                                    str(tiempo.month).zfill(2),
                                                                    str(tiempo.day).zfill(2),
                                                                    str(tiempo.hour).zfill(2),
                                                                    str(tiempo.minute).zfill(2),
                                                                    str(tiempo.second).zfill(2))
        modelo.save(os.path.join(ruta_guardar, nombre_de_archivo))
        print(nombre_de_archivo, "guardado")
    return modelo


def Limpiar(ventana):
    keras.backend.clear_session()
    if __name__ != "__main__":
        evnt = gui.EntEvent(myEVT_ENTRENAMIENTO, 1, False)
        wx.PostEvent(ventana, evnt)

#Funcion de entrenamiento
def Entrenar(ruta_modelo, ruta_datos, tensorboard, continuarentrenamiento,
 lrperzonalizado, optimizador, lr, cambiarpropiedades, epochs, ARCHIVOS_POR_ENTRENAMIENTO, ventana):


    print("Modelo: {} | Optimizador: {} | LR: {} | TB: {} | Datos para ent: {} | Epochs: {}"
          .format(ruta_modelo if continuarentrenamiento else "Nuevo",
                  optimizador if cambiarpropiedades else "Sin modificar",
                  lr if lrperzonalizado else "Sin modificar",
                  tensorboard, ruta_datos, epochs))
    keras.backend.clear_session()
    if __name__ != "__main__":
        evnt = gui.EntEvent(myEVT_ENTRENAMIENTO, 1, True)
        wx.PostEvent(ventana, evnt)

    try:
        archivos_entrenamiento = BuscarArchivosEntrenamiento(ruta_datos)
    except Exception as e:
        print(e)
        Limpiar(ventana)
        return False

    try:
        datos_para_entrenamiento = np.load(archivos_entrenamiento[0])
        imagenes = np.array([dato[0] for dato in datos_para_entrenamiento])
        salidas = np.array([dato[1] for dato in datos_para_entrenamiento])

    except Exception as e:
        print(e)
        print("Error al cargar archivo")
        Limpiar(ventana)
        return False

    if continuarentrenamiento:
        try:
            modelo = CargarModelo(ruta_modelo)
        except Exception as e:
            print(e)
            Limpiar(ventana)
            return False

        if (VerificarDimensiones(modelo,imagenes,salidas)):
            print("Dimensiones correctas")
        else:
            print("Las dimesiones del modelo no coinciden con las dimensiones de los datos")
            Limpiar(ventana)
            return False

    else:
        print("Generando modelo nuevo")
        modelo = modelos.GenerarModelo(imagenes.shape[1],imagenes.shape[2],imagenes.shape[3],salidas.shape[1])
        print("Modelo generado correctamente | Entrada: {} | Salida: {}".format(imagenes.shape[1:],salidas.shape[1]))

    if cambiarpropiedades:
        print("Compilando modelo")
        try:
            if lrperzonalizado:
                if optimizador == "adam":
                    modelo.compile(optimizer=keras.optimizers.Adam(lr=float(lr)),loss="categorical_crossentropy",metrics=['accuracy'])
                elif optimizador == "sgd":
                    modelo.compile(optimizer=keras.optimizers.SGD(lr=float(lr)),loss="categorical_crossentropy",metrics=['accuracy'])
            else:
                modelo.compile(optimizer=optimizador,loss="categorical_crossentropy",metrics=['accuracy'])
        except Exception as e:
            print(e)
            print("Error compilando modelo")
            Limpiar(ventana)
            return 0

        else:
            print("Modelo compilado correctamente")

    print("Empezando entrenamiento")

    del imagenes
    del salidas
    del datos_para_entrenamiento
    recolector_datos = RecolectorDatos(ventana)

    for epoch in range(epochs):
        for imagenes, salidas in CargarySepararArchivos(archivos_entrenamiento, ARCHIVOS_POR_ENTRENAMIENTO):
            modelo = EntrenarModelo(modelo, ruta_datos, imagenes, salidas, 1, tensorboard, recolector_datos)
            if not seguirEntrenamiento.is_set():
                break
        if not seguirEntrenamiento.is_set():
            print("Entrenamiento cancelado")
            break

    #modelo.save(os.path.join(ruta_datos, "modelo-final.h5"))
    del modelo
    time.sleep(2)
    print("Entrenamiento terminado")
    Limpiar(ventana)
    return True


if __name__ == "__main__":
    pass
