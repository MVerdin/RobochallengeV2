#!/usr/bin/env python3
import tensorflow.contrib.keras as keras

#Funcion para generar el modelo keras de la red neuronal
def GenerarModelo(altoimg,anchoimg,canalesimg,clases):
    entradaImagen = keras.layers.Input(shape=(altoimg,anchoimg,canalesimg))

    conv1 = keras.layers.Conv2D(64, (3,3))(entradaImagen)
    pool1 = keras.layers.MaxPooling2D((2,2))(conv1)
    norm1 = keras.layers.BatchNormalization()(pool1)

    conv2 = keras.layers.Conv2D(64, (3,3))(norm1)
    pool2 = keras.layers.MaxPooling2D((2,2))(conv2)
    norm2 = keras.layers.BatchNormalization()(pool2)

    conv3 = keras.layers.Conv2D(64, (3,3))(norm2)
    pool3 = keras.layers.MaxPooling2D((2,2))(conv3)
    norm3 = keras.layers.BatchNormalization()(pool3)

    flat = keras.layers.Flatten()(norm3)

    dense1 = keras.layers.Dense(128, activation = "relu")(flat)
    dropout1 = keras.layers.Dropout(0.3)(dense1)
    dense2 = keras.layers.Dense(128, activation = "relu")(dropout1)

    out = keras.layers.Dense(clases, activation = "softmax")(dense2)

    modelo = keras.models.Model(inputs=entradaImagen, outputs = out)

    return modelo


if __name__ == "__main__":
    modelo = GenerarModelo(180,240,3,5)
    print(modelo.input_shape)
