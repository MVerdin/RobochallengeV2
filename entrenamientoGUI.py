#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade not found on Wed Jul 19 16:06:23 2017
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.checkboxContinuarEnt = wx.CheckBox(self, wx.ID_ANY, "Continuar entrenamiento")
        self.intextRutaModelo = wx.TextCtrl(self, wx.ID_ANY, "Ruta del modelo")
        self.intextRutaDatos = wx.TextCtrl(self, wx.ID_ANY, "Ruta de datos para entrenamiento")
        self.checkboxTensorboard = wx.CheckBox(self, wx.ID_ANY, "Tensorboard")
        self.radioADAM = wx.RadioButton(self, wx.ID_ANY, "ADAM")
        self.radioCGD = wx.RadioButton(self, wx.ID_ANY, "CGD")
        self.checkboxLRP = wx.CheckBox(self, wx.ID_ANY, "LR personalizado")
        self.intextLR = wx.TextCtrl(self, wx.ID_ANY, "")
        self.buttonEntrenar = wx.Button(self, wx.ID_ANY, "Entrenar")
        self.buttonCancelar = wx.Button(self, wx.ID_ANY, "Cancelar")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Entrenamiento")
        self.SetSize((600, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        textConsola = wx.StaticText(self, wx.ID_ANY, "")
        sizer_1.Add(textConsola, 1, wx.EXPAND, 0)
        sizer_2.Add(self.checkboxContinuarEnt, 0, 0, 0)
        sizer_2.Add(self.intextRutaModelo, 1, 0, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_1.Add(self.intextRutaDatos, 0, wx.EXPAND, 0)
        sizer_4.Add(self.checkboxTensorboard, 0, wx.EXPAND, 0)
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
        self.SetSizer(sizer_1)
        self.Layout()
        self.SetSize((600, 500))
        # end wxGlade


class MyApp(wx.App):
    def OnInit(self):
        #self.res = xrc.XmlResource(GUI_FILENAME)
        self.frame = MyFrame(None)#self.res.LoadFrame(None, GUI_MAINFRAME_NAME)
        self.frame.Show()
        return True

# end of class MyFrame
app = MyApp()
#ventana = MyFrame()
#ventana.show()
app.MainLoop()


