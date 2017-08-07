#!/usr/bin/env python3

archivos_por_entrenamiento = 3

nombre_de_archivos = 'training_data-{0}.npy'
muestras_por_archivo = 100
resolucion_camara = (256,160)
escala_de_grises = False

#mapeo de comandos a vector one hot para el entrenamiento
cmd2onehot={
    "s":[1,0,0,0,0],
    "f":[0,1,0,0,0],
    "b":[0,0,1,0,0],
    "r":[0,0,0,1,0],
    "l":[0,0,0,0,1],
}

#Canales de salidas a motores
#(motorderA, motorderB, motorizqA, motorizqB)
canales_motores=(3,5,7,8)

#Salidas correspondientes a cada comando
#(motorderA, motorderB, motorizqA, motorizqB)
comandos_a_motores={
    "s":(0,0,0,0),
    "f":(1,0,1,0),
    "b":(0,1,0,1),
    "r":(1,0,0,1),
    "l":(0,1,1,0),
}


def ObtenerConfigEntrenamiento():
    return (nombre_de_archivos,
            archivos_por_entrenamiento)

def ObtenerConfigRecoleccion():
    return (nombre_de_archivos,
            muestras_por_archivo,
            resolucion_camara,
            escala_de_grises,
            cmd2onehot)

def ObtenerConfigMotores():
    return(canales_motores,
           comandos_a_motores)

def ObtenerConfigPelea():
    return(resolucion_camara,
           escala_de_grises,
           comandos_a_motores)
