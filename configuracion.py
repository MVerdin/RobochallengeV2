#!/usr/bin/env python3

ARCHIVOS_POR_ENTRENAMIENTO = 30

NOMBRE_DE_ARCHIVOS = 'training_data-{0}.npy'
MUESTRAS_POR_ARCHIVO = 100
RESOLUCION_CAMARA = (256, 160)
ESCALA_DE_GRISES = False

IMAGENES_POR_DECISION = 1
# mapeo de comandos a vector one hot para el entrenamiento
CMD2ONEHOT = {

    "s": (1, 0, 0, 0, 0),
    "f": (0, 1, 0, 0, 0),
    "b": (0, 0, 1, 0, 0),
    "r": (0, 0, 0, 1, 0),
    "l": (0, 0, 0, 0, 1),
}

# Canales de salidas a motores
#(motorderA, motorderB, motorizqA, motorizqB)
CANALES_MOTORES = (31, 33, 35, 37)

# Salidas correspondientes a cada comando
#(motorderA, motorderB, motorizqA, motorizqB)
COMANDOS_A_MOTORES = {
    (1, 0, 0, 0, 0): (0, 0, 0, 0),
    (0, 1, 0, 0, 0): (1, 0, 1, 0),
    (0, 0, 1, 0, 0): (0, 1, 0, 1),
    (0, 0, 0, 1, 0): (1, 0, 0, 1),
    (0, 0, 0, 0, 1): (0, 1, 1, 0),
}

PIN_INTERRUPTOR = 32
CANALES_LED_RGB = (36, 38, 40)


def ConectarLEDEstado():
    led = LEDEstado(CANALES_LED_RGB)
    return led

def ObtenerConfigEntrenamiento():
    return (NOMBRE_DE_ARCHIVOS,
            ARCHIVOS_POR_ENTRENAMIENTO)


def ObtenerConfigRecoleccion():
    return (NOMBRE_DE_ARCHIVOS,
            MUESTRAS_POR_ARCHIVO,
            RESOLUCION_CAMARA,
            ESCALA_DE_GRISES,
            CMD2ONEHOT,
            PIN_INTERRUPTOR,
            CANALES_LED_RGB)


def ObtenerConfigMotores():
    return(CANALES_MOTORES,
           COMANDOS_A_MOTORES,
           CMD2ONEHOT)


def ObtenerConfigPelea():
    return(RESOLUCION_CAMARA,
           ESCALA_DE_GRISES,
           COMANDOS_A_MOTORES,
           CANALES_MOTORES,
           IMAGENES_POR_DECISION,
           PIN_INTERRUPTOR,
           CANALES_LED_RGB)
