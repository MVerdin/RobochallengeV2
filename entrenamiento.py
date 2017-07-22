#!/usr/bin/env python3
import entrenamientoGUI as egui
import wx
import tensorflow.contrib.keras as keras
import modelos
import os
contador=0


def OnButtonEntrenar(evnt):
    ruta_modelo = app.frame.intextRutaModelo.GetValue()

    if app.frame.checkboxContinuarEnt.GetValue():
        if os.path.isfile(ruta_modelo):
            try:
                modelo = keras.models.load_model(ruta_modelo)
            except ValueError:
                print("Archivo invalido")

    ruta_datos = app.frame.intextRutaDatos.GetValue()
    lr = app.frame.intextLR.GetValue()
    optimizador = "adam" if app.frame.radioADAM.GetValue() else "cgd"
    tensorboard = app.frame.checkboxTensorboard.GetValue()


    Entrenar(modelos.GenerarModelo(180,240,5),optimizador,lr,tensorboard,ruta_datos)

def OnButtonCancelar(evnt):
    pass

def Entrenar(modelo, optimizador, lr, tb, carpetadatos):
    print(Optimizador: {} | LR: {} | TB: {} | Datos para ent: {}".format(optimizador, lr, tb, carpetadatos))


if __name__ == "__main__":
    app = egui.Aplicacion()
    app.frame.buttonEntrenar.Bind(wx.EVT_BUTTON, OnButtonEntrenar)
    app.frame.buttonCancelar.Bind(wx.EVT_BUTTON, OnButtonCancelar)
    app.MainLoop()
