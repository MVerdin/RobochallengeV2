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
        self.arduino.enviar_linea("Mestado")
        estado = self.arduino.recibir_linea().strip("M")
        return estado

    def detenerse(self):
        self.arduino.enviar_linea("Mdetenerse")

    def avanzar(self):
        self.arduino.enviar_linea("Mavanzar")

    def retroceder(self):
        self.arduino.enviar_linea("Mretroceder")

    def girar_derecha(self):
        self.arduino.enviar_linea("Mgirarderecha")

    def girar_izquierda(self):
        self.arduino.enviar_linea("Mgirarizquierda")
