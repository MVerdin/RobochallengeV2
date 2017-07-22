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

#Funcion llamada por el boton "Entrenar"
def OnButtonEntrenar(evnt):
    (ruta_modelo, ruta_datos, tensorboard, continuarentrenamiento,
     lrperzonalizado, optimizador, lr) = app.frame.ObtenerValores()
    if continuarentrenamiento:
        if os.path.isfile(ruta_modelo):
            try:
                modelo = keras.models.load_model(ruta_modelo)
            except ValueError:
                print("Archivo invalido")
    else:
        modelo = modelos.GenerarModelo()
    Entrenar(ruta_modelo,optimizador,lr,tensorboard,ruta_datos)
#Funcion llamada por el boton "Cancelar"
def OnButtonCancelar(evnt):
    pass

#Funcion de entrenamiento
def Entrenar(modelo, optimizador, lr, tb, carpetadatos):
    print("Modelo: {} | Optimizador: {} | LR: {} | TB: {} | Datos para ent: {}".format(modelo, optimizador, lr, tb, carpetadatos))


if __name__ == "__main__":
    app = egui.Aplicacion()
    app.frame.buttonEntrenar.Bind(wx.EVT_BUTTON, OnButtonEntrenar)
    app.frame.buttonCancelar.Bind(wx.EVT_BUTTON, OnButtonCancelar)

    app.MainLoop()
