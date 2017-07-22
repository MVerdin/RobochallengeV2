#!/usr/bin/env python3
import entrenamientoGUI as egui
import wx
import tensorflow.contrib.keras as keras
import modelos
import os
contador=0


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

def OnButtonCancelar(evnt):
    pass


def Entrenar(modelo, optimizador, lr, tb, carpetadatos):
    print("Modelo: {} | Optimizador: {} | LR: {} | TB: {} | Datos para ent: {}".format(modelo, optimizador, lr, tb, carpetadatos))


if __name__ == "__main__":
    app = egui.Aplicacion()
    app.frame.buttonEntrenar.Bind(wx.EVT_BUTTON, OnButtonEntrenar)
    app.frame.buttonCancelar.Bind(wx.EVT_BUTTON, OnButtonCancelar)

    app.MainLoop()
