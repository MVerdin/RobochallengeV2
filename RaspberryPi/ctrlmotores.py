#!/usr/bin/env python3


class Motores():
    def __init__(self, arduino, tiempo_seguridad=0.5):
        self.arduino = arduino
        self.tiempo_seguridad = tiempo_seguridad
        self.caracteramensaje = {
                                "s": "Mdetenerse",
                                "f": "Mavanzar",
                                "b": "Mretroceder",
                                "r": "Mgirarderecha",
                                "l": "Mgirarizquierda"
                                }
        self.vectoramensaje =   {
                                (1, 0, 0, 0, 0): "Mdetenerse",
                                (0, 1, 0, 0, 0): "Mavanzar",
                                (0, 0, 1, 0, 0): "Mretroceder",
                                (0, 0, 0, 1, 0): "Mgirarderecha",
                                (0, 0, 0, 0, 1): "Mgirarizquierda"
                                }




    def test(self):
        self.arduino.enviar_linea("activar motores")
        print(self.arduino.recibir_linea())

    def leer_estado(self):
        self.arduino.borrar_entrada()
        if(not self.arduino.enviar_comando("Mestado")):
            return None
        estado = self.arduino.recibir_linea()
        return estado

    def detenerse(self):
        if(not self.arduino.enviar_comando("Mdetenerse")):
            print("Error al enviar comando")

    def avanzar(self):
        if(not self.arduino.enviar_comando("Mavanzar")):
            print("Error al enviar comando")

    def retroceder(self):
        if(not self.arduino.enviar_comando("Mretroceder")):
            print("Error al enviar comando")

    def girar_derecha(self):
        if(not self.arduino.enviar_comando("Mgirarderecha")):
            print("Error al enviar comando")

    def girar_izquierda(self):
        if(not self.arduino.enviar_comando("Mgirarizquierda")):
            print("Error al enviar comando")

    def procesar_comando(self, comando):
        if (type(comando) == str and comando in self.caracteramensaje):
            mensaje = self.caracteramensaje[comando]
        elif (type(comando) == tuple and comando in self.vectoramensaje):
            mensaje = self.vectoramensaje[comando]
        elif (type(comando) == list and tuple(comando) in self.vectoramensaje):
            mensaje = self.vectoramensaje[tuple(comando)]
        else:
            self.detenerse()
            print("Comando invalido")
            return False
        if(not self.arduino.enviar_comando(mensaje)):
            print("Error al enviar comando")
            return False
        return True


