#!/usr/bin/env python3
import serial, os, time


class Arduino():
    def __init__(self, velocidad=38400):
        if self.conectar(velocidad) is True:
            print("Conexion con Arduino exitosa")
        else:
            print("Conexion fallida")

    def conectar(self,velocidad):
        if "ttyACM0" in os.listdir("/dev"):
            self.puerto = serial.Serial("/dev/ttyACM0", baudrate=velocidad)
            return True
        else:
            print("Arduino no encontrado")
            return False

    def enviar_linea(self,mensaje):
        self.puerto.write(bytes(mensaje+"\n", encoding="utf-8"))

    def recibir_linea(self):
        linea_recibida=self.puerto.readline()
        linea_recibida= str(linea_recibida, errors="strict")
        linea_recibida = linea_recibida.strip("\n\r")
        return linea_recibida

    def enviar_comando(self, comando):
        self.borrar_entrada()
        self.enviar_linea(comando)
        return self.recibir_linea() == comando
    
    def borrar_entrada(self):
        self.puerto.reset_input_buffer()

    def ping(self):
        self.borrar_entrada()
        self.enviar_linea("ping")
        t1 = time.time()
        recibido = self.recibir_linea()
        if recibido == "ping":
            t2 = time.time()
            print(t2-t1, "segundos")
        else:
            print(recibido)
            return recibido



