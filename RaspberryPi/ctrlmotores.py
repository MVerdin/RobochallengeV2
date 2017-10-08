import time


class Motores():
    def __init__(self, arduino, tiempo_seguridad=0.5):
        self.arduino = arduino
        self.tiempo_seguridad = tiempo_seguridad

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
