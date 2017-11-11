#!/usr/bin/env python3
import time
import multiprocessing
import queue
import numpy as np


class Guardador():
    def __init__(self):
        self.fila = multiprocessing.Queue()
        self.evento_encendido = multiprocessing.Event()
        self.evento_encendido.set()
        self.proceso = multiprocessing.Process(
            target=self.funcion_guardado, args=(self.fila, self.evento_encendido))
        self.proceso.start()

    def funcion_guardado(self, fila, encendido):
        while encendido.is_set() is True:
            try:
                datos = fila.get(block=False)
            except queue.Empty:
                time.sleep(0.05)
            else:
                archivo = datos[0]
                ruta = datos[1]
                np.save(ruta, archivo)
                print("Archivo {} guardado con {} imagenes".format(
                    ruta, len(archivo)))

    def guardar(self, ruta, archivo):
        print("Archivo {} recibido con {} imagenes".format(ruta, len(archivo)))
        self.fila.put([archivo, ruta])

    def apagar(self):
        self.evento_encendido.clear()
        self.proceso.join()