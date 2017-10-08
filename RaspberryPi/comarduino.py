#!/usr/bin/env python3
import serial, os


class Arduino():
    def __init__(self, velocidad=38400):
        if self.conectar(velocidad) is True:
            print("Conexion con Arduino exitosa")
        else:
            print("Conexion fallida")

    def conectar(self,velocidad):
        if "ttyACM0" in os.listdir("/dev"):
            self.puerto = serial.Serial("/dev/ttyACM0", baudrate=velocidad, timeout=0.5)
            return True
        else:
            print("Arduino no encontrado")
            return False

    def enviar_linea(self,mensaje):
        self.puerto.write(bytes(mensaje+"\n", encoding="utf-8"))

    def recibir_linea(self):
        linea_recibida=self.puerto.readline()
        linea_recibida= str(linea_recibida, errors="strict")
        linea_recibida = linea_recibida.strip("\n")
        return linea_recibida
    
    def borrar_entrada(self):
        self.puerto.reset_input_buffer()


