#!/usr/bin/env python3
import entrenamientoGUI as egui
import wx
import tensorflow.contrib.keras as keras
import modelos
contador=0


def OnButtonEntrenar(evnt):
#    global contador
#    contador += 1
#    app.frame.textConsola.SetLabel("Hola {}-{}".format(contador,app.frame.intextRutaModelo.GetValue()))

    ruta_modelo=app.frame.intextRutaModelo.GetValue()
    ruta_datos=app.frame.intextRutaDatos.GetValue()
    lr=app.frame.intextLR.GetValue()
    optimizador="adam" if app.frame.radioADAM.GetValue() else "cgd"
    tensorboard=app.frame.checkboxTensorboard.GetValue()
    Entrenar(modelos.GenerarModelo(180,240,5),optimizador,lr,tensorboard,ruta_datos)

def OnButtonCancelar(evnt):
#    global contador
#    contador -= 1
#    app.frame.textConsola.SetLabel("Hola {}".format(contador))
    pass

def Entrenar(modelo, optimizador, lr, tb, carpetadatos):
    print("Modelo: {} |Optimizador: {} |LR: {} |TB: {} |Datos para ent: {}".format(modelo, optimizador, lr, tb, carpetadatos))


if __name__ == "__main__":
    app = egui.Aplicacion()
    app.frame.buttonEntrenar.Bind(wx.EVT_BUTTON, OnButtonEntrenar)
    app.frame.buttonCancelar.Bind(wx.EVT_BUTTON, OnButtonCancelar)
    app.MainLoop()
