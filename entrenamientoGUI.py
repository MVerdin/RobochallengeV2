#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade on Wed Jul 19 16:06:23 2017
#

import wx
import gettext
import entrenamiento
import modelos
import os, sys, threading

class Consola(wx.TextCtrl):
    def __init__(self, *args, **kwds):
        wx.TextCtrl.__init__(self, *args, **kwds)
    #Metodo necesario para recibir los mensajes y mandarlos a la ventana
    def write(self, message):
        wx.CallAfter(self.WriteText, message)

#Clase generada en wxGlade para la creacion de la ventana
class Ventana(wx.Frame):
    #Creacion de componentes de la ventana
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, *args, **kwds)
        self.panelprincipal = wx.Panel(self)
        self.checkboxContinuarEnt = wx.CheckBox(self.panelprincipal, wx.ID_ANY, "Continuar entrenamiento")
        self.intextRutaModelo = wx.FilePickerCtrl(self.panelprincipal,message="Ruta del modelo guardado", style=wx.FLP_USE_TEXTCTRL)
        self.intextRutaDatos = wx.DirPickerCtrl(self.panelprincipal,message="Ruta de los datos para entrenamiento", style=wx.FLP_USE_TEXTCTRL)
        self.checkboxTensorboard = wx.CheckBox(self.panelprincipal, wx.ID_ANY, "Tensorboard")
        self.checkboxTensorboard.SetValue(True)
        self.checkboxCambiarPropiedades = wx.CheckBox(self.panelprincipal, wx.ID_ANY, "Cambiar propiedades")
        self.radioADAM = wx.RadioButton(self.panelprincipal, wx.ID_ANY, "ADAM")
        self.radioCGD = wx.RadioButton(self.panelprincipal, wx.ID_ANY, "SGD")
        self.checkboxLRP = wx.CheckBox(self.panelprincipal, wx.ID_ANY, "LR personalizado")
        self.intextLR = wx.TextCtrl(self.panelprincipal, wx.ID_ANY, "")
        self.buttonEntrenar = wx.Button(self.panelprincipal, wx.ID_ANY, "Entrenar")
        self.buttonCancelar = wx.Button(self.panelprincipal, wx.ID_ANY, "Cancelar")
        self.textConsola = Consola(self.panelprincipal, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        sys.stdout = self.textConsola #Redireccion de mensajes a GUI
        sys.stderr = self.textConsola #Redireccion de errores a GUI
        self.textRutaDatos = wx.StaticText(self.panelprincipal, wx.ID_ANY, "Carpeta de datos")
        self.__set_properties()
        self.__do_layout()

    #Configuracion de la ventana
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Entrenamiento")
        self.SetSize((600, 500))

        # end wxGlade

    #Acomodo de los widgets
    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.textConsola, 1, wx.EXPAND, 0)
        sizer_2.Add(self.checkboxContinuarEnt, 0, 0, 0)
        sizer_2.Add(self.intextRutaModelo, 1, 0, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_8.Add(self.textRutaDatos, 0, 0, 0)
        sizer_8.Add(self.intextRutaDatos, 1, 0, 0)
        sizer_9.Add(self.checkboxTensorboard, 1, 0, 0)
        sizer_9.Add(self.checkboxCambiarPropiedades, 1, 0, 0)
        sizer_4.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_6.Add(self.radioADAM, 1, 0, 0)
        sizer_6.Add(self.radioCGD, 1, 0, 0)
        sizer_4.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_5.Add(self.checkboxLRP, 0, 0, 0)
        sizer_5.Add(self.intextLR, 1, wx.LEFT, 4)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_7.Add(self.buttonEntrenar, 1, 0, 0)
        sizer_7.Add(self.buttonCancelar, 0, 0, 0)
        sizer_3.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)
        self.panelprincipal.SetSizer(sizer_1)
        self.Layout()
        self.SetSize((600, 500))
        self.checkboxCambiarPropiedades.Bind(wx.EVT_CHECKBOX, self.OnClickCheckBox)
        self.checkboxContinuarEnt.Bind(wx.EVT_CHECKBOX, self.OnClickCheckBox)
        self.checkboxLRP.Bind(wx.EVT_CHECKBOX, self.OnClickCheckBox)
        # end wxGlade

    #Funcion que lee los valores introducidos en los widgets
    def ObtenerValores(self):
        ruta_modelo = self.intextRutaModelo.GetPath()
        ruta_datos = self.intextRutaDatos.GetPath()
        tensorboard = self.checkboxTensorboard.GetValue()
        continuarentrenamiento=self.checkboxContinuarEnt.GetValue()
        lrperzonalizado = self.checkboxLRP.GetValue()
        optimizador = "adam" if self.radioADAM.GetValue() else "sgd"
        lr = self.intextLR.GetValue()
        cambiarpropiedades = self.checkboxCambiarPropiedades.GetValue()
        return (ruta_modelo, ruta_datos, tensorboard, continuarentrenamiento,
                lrperzonalizado, optimizador, lr, cambiarpropiedades)

    #Funcion que habilita o deshabilita los widgets dependiendo de las opciones seleccionadas
    def HabilitarWidgets(self, entrenando):
        self.buttonEntrenar.Enable(not entrenando)
        self.buttonCancelar.Enable(entrenando)
        self.checkboxCambiarPropiedades.Enable(not entrenando)
        self.checkboxContinuarEnt.Enable(not entrenando)
        self.checkboxLRP.Enable(self.checkboxCambiarPropiedades.GetValue() and not entrenando)
        self.checkboxTensorboard.Enable(not entrenando)
        self.intextLR.Enable(self.checkboxLRP.GetValue() and self.checkboxCambiarPropiedades.GetValue() and not entrenando)
        self.intextRutaDatos.Enable(not entrenando)
        self.intextRutaModelo.Enable(self.checkboxContinuarEnt.GetValue() and not entrenando)
        self.radioCGD.Enable(self.checkboxCambiarPropiedades.GetValue() and not entrenando)
        self.radioADAM.Enable(self.checkboxCambiarPropiedades.GetValue() and not entrenando)

    #Funcion callback relacionada a los checkbox de la ventana
    def OnClickCheckBox(self,evnt):
        self.HabilitarWidgets(entrenando = False)

class App(wx.App):
    def OnInit(self):
        self.ventana = Ventana(None)
        self.ventana.HabilitarWidgets(entrenando = False)
        self.ventana.Show()
        return True


#Funcion llamada por el boton "Entrenar"
def OnButtonEntrenar(evnt):
    #Creacion de hilo que evita que la GUI se bloquee en el proceso de entrenamiento
    thread = threading.Thread(target=entrenamiento.Entrenar, args=(app.ventana.ObtenerValores()))
    app.ventana.HabilitarWidgets(entrenando = True)
    try:
        thread.start()
        #entrenamiento.Entrenar(*app.ventana.ObtenerValores())
    except Exception as e:
        sys.stdout=sys.__stdout__ #Restauracion del canal de salida estandar
        sys.stderr=sys.__stderr__ #Restauracion del canal de errores estandar
        print (e)
    #app.ventana.HabilitarWidgets(entrenando = False)
    return


#Funcion llamada por el boton "Cancelar"
def OnButtonCancelar(evnt):
    app.ventana.HabilitarWidgets(entrenando = False)

if __name__ == "__main__":
    app = App(redirect=False)
    app.ventana.buttonEntrenar.Bind(wx.EVT_BUTTON, OnButtonEntrenar)
    app.ventana.buttonCancelar.Bind(wx.EVT_BUTTON, OnButtonCancelar)
    app.MainLoop()
