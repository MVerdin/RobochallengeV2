#!/usr/bin/env python3
'''Programa de entrenamiento'''

import wx
import wx.lib.plot as plot
import gettext
import entrenamiento
import modelos
import configuracion
import os, sys, threading

class Consola(wx.TextCtrl):
    def __init__(self, *args, **kwds):
        wx.TextCtrl.__init__(self, *args, **kwds)
    #Metodo necesario para recibir los mensajes y mandarlos a la ventana
    def write(self, message):
        wx.CallAfter(self.WriteText, message)
    def flush(self):
        pass


class EntEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, Entrenando=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._Entrenando = Entrenando

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event
        """
        return self._Entrenando

#Clase generada en wxGlade para la creacion de la ventana
class Ventana(wx.Frame):
    #Creacion de componentes de la ventana
    def __init__(self,redireccionar_consola=False, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = (wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
                         wx.RESIZE_BORDER | wx.SYSTEM_MENU |
                         wx.CAPTION | wx.CLOSE_BOX |
                         wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)
        wx.Frame.__init__(self, *args, **kwds)
        self.panelprincipal = wx.Panel(self)
        self.notebook = wx.Notebook(self.panelprincipal)
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
        self.selectorEpochs = wx.SpinCtrlDouble(self.panelprincipal,wx.ID_ANY,initial=1)
        self.selectorNumeroArchivos = wx.SpinCtrlDouble(self.panelprincipal,wx.ID_ANY,initial=configuracion.ARCHIVOS_POR_ENTRENAMIENTO)
        self.buttonEntrenar = wx.Button(self.panelprincipal, wx.ID_ANY, "Entrenar")
        self.buttonCancelar = wx.Button(self.panelprincipal, wx.ID_ANY, "Cancelar")
        self.textConsola = Consola(self.notebook, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.etiquetaRutaDatos = wx.StaticText(self.panelprincipal, wx.ID_ANY, "Carpeta de datos")
        self.etiquetaNumeroEpochs = wx.StaticText(self.panelprincipal, wx.ID_ANY, "Numero de epochs")
        self.etiquetaNumeroArchivos = wx.StaticText(self.panelprincipal, wx.ID_ANY, "Archivos por entrenamiento")
        
        self.__set_properties()
        self.__do_layout()
        self.__do_binding()

        self.sizerGrafica = wx.BoxSizer(wx.VERTICAL)
        self.panelGrafica = wx.Panel(self.notebook)
        self.panelGrafica.SetSizer(self.sizerGrafica)
        self.grafica = plot.PlotCanvas(self.panelprincipal)
        self.sizerGrafica.Add(self.grafica)
        self.notebook.AddPage(self.textConsola, "Consola")
        self.notebook.AddPage(self.panelGrafica, "Grafica")
        
        if redireccionar_consola:
            sys.stdout = self.textConsola #Redireccion de mensajes a GUI
            sys.stderr = self.textConsola #Redireccion de errores a GUI

    #Configuracion de la ventana
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Entrenamiento")
        self.SetSize((600, 500))
        self.SetMinSize(wx.Size(420,400))
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
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)

        sizer_1.Add(self.notebook, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 0, wx.EXPAND | wx.LEFT, 8)

        sizer_2.Add(sizer_8, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 8)
        sizer_2.Add(sizer_10, 1, wx.EXPAND, 0)

        sizer_8.Add(self.checkboxContinuarEnt, 1, wx.EXPAND, 0)
        sizer_8.Add(self.etiquetaRutaDatos, 1, wx.EXPAND, 0)
        sizer_8.Add(self.etiquetaNumeroEpochs, 1, wx.EXPAND, 0)
        sizer_8.Add(self.etiquetaNumeroArchivos, 1, wx.EXPAND, 0)

        sizer_10.Add(self.intextRutaModelo, 1, wx.EXPAND, 0)
        sizer_10.Add(self.intextRutaDatos, 1, wx.EXPAND, 0)
        sizer_10.Add(self.selectorEpochs, 1, wx.EXPAND, 0)
        sizer_10.Add(self.selectorNumeroArchivos, 1, wx.EXPAND, 0)

        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_7, 0, wx.EXPAND, 0)

        sizer_4.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)

        sizer_7.Add(self.buttonEntrenar, 1, 0, 0)
        sizer_7.Add(self.buttonCancelar, 0, 0, 0)

        sizer_9.Add(self.checkboxTensorboard, 1, 0, 0)
        sizer_9.Add(self.checkboxCambiarPropiedades, 1, 0, 0)

        sizer_6.Add(self.radioADAM, 1, 0, 0)
        sizer_6.Add(self.radioCGD, 1, 0, 0)

        sizer_5.Add(self.checkboxLRP, 0, 0, 0)
        sizer_5.Add(self.intextLR, 1, wx.LEFT, 4)


        self.panelprincipal.SetSizer(sizer_1)
        self.panelprincipal.Layout()
        #self.SetSize((600, 500))

        # end wxGlade


    def __do_binding(self):
        self.checkboxCambiarPropiedades.Bind(wx.EVT_CHECKBOX, self.OnClickCheckBox)
        self.checkboxContinuarEnt.Bind(wx.EVT_CHECKBOX, self.OnClickCheckBox)
        self.checkboxLRP.Bind(wx.EVT_CHECKBOX, self.OnClickCheckBox)
        self.buttonEntrenar.Bind(wx.EVT_BUTTON, self.OnButtonEntrenar)
        self.buttonCancelar.Bind(wx.EVT_BUTTON, self.OnButtonCancelar)
        self.Bind(entrenamiento.EVT_ENTRENAMIENTO, self.OnEntrenamiento)
        self.Bind(entrenamiento.EVT_ACTUALIZAR_GRAFICAS, self.ActualizarGraficas)

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
        epochs = self.selectorEpochs.GetValue()
        archivos_por_entrenamiento = self.selectorNumeroArchivos.GetValue()
        return (ruta_modelo, ruta_datos, tensorboard, continuarentrenamiento,
                lrperzonalizado, optimizador, lr, cambiarpropiedades, int(epochs), 
                int(archivos_por_entrenamiento))

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


    def OnEntrenamiento(self,evnt):
        self.HabilitarWidgets(entrenando = evnt.GetValue())
        #print("Evento recibido")
        #print(evnt)

    #Funcion llamada por el boton "Entrenar"
    def OnButtonEntrenar(self,evnt):
        entrenamiento.seguirEntrenamiento.set()
        try:
            #Creacion de hilo que evita que la GUI se bloquee en el proceso de entrenamiento
            threadEnt = threading.Thread(target=entrenamiento.Entrenar, args=(*self.ObtenerValores(), self))
            threadEnt.start()
        except Exception as e:
            sys.stdout=sys.__stdout__ #Restauracion del canal de salida estandar
            sys.stderr=sys.__stderr__ #Restauracion del canal de errores estandar
            print (e)

    #Funcion llamada por el boton "Cancelar"
    def OnButtonCancelar(self,evnt):
        print("\nCancelando")
        entrenamiento.seguirEntrenamiento.clear()

    def ActualizarGraficas(self, evnt):
        print("evento recibido")
        linea_perdidas = plot.PolyLine(evnt.recolector.perdidas, legend="Perdidas")
        linea_perdidas_promedio = plot.PolyLine(evnt.recolector.perdidas_promedio, legend="Perdidas promedio")
        linea_precisiones = plot.PolyLine(evnt.recolector.precisiones, legend="Precisiones")
        linea_precisiones_promedio = plot.PolyLine(evnt.recolector.precisiones_promedio, legend="Precisiones promedio")
        graficos = plot.PlotGraphics([linea_perdidas,linea_perdidas_promedio,linea_precisiones,linea_precisiones_promedio])
        self.grafica.Draw(graficos)
        #print(evnt.recolector.perdidas,
        #        evnt.recolector.precisiones,
        #        evnt.recolector.precisiones_promedio,
        #        evnt.recolector.precisiones_promedio)
        

class App(wx.App):
    def OnInit(self):
        self.ventana = Ventana(True,None)
        self.ventana.HabilitarWidgets(entrenando = False)
        self.ventana.Show()
        self.ventana.Refresh()
        return True

if __name__ == "__main__":
    app = App()
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
