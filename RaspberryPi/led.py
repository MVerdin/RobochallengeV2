import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

class LEDEstado():
    def __init__(self, pines_RGB, estado_inicial="apagado"):
        self.pines = pines_RGB
        GPIO.cleanup(self.pines)
        GPIO.setup(self.pines, GPIO.OUT)
        self.cambiar_estado(estado_inicial)

    def cambiar_estado(self, estado):
        if(estado=="apagado"):
            GPIO.output(self.pines, (1,0,0))
        elif(estado=="listo"):
            GPIO.output(self.pines, (0,0,1))
        elif(estado=="encendido"):
            GPIO.output(self.pines, (0,1,0))