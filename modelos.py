#!/usr/bin/env python3
import tensorflow.contrib.keras as keras
#import keras

#Funcion para generar el modelo keras de la red neuronal
def GenerarModelo(altoimg,anchoimg,canalesimg,clases):
    entradaImagen = keras.layers.Input(shape=(altoimg,anchoimg,canalesimg))

    conv1 = keras.layers.Conv2D(32, (3,3))(entradaImagen)
    pool1 = keras.layers.MaxPooling2D((2,2))(conv1)
    norm1 = keras.layers.BatchNormalization()(pool1)

    conv2 = keras.layers.Conv2D(32, (3,3))(norm1)
    pool2 = keras.layers.MaxPooling2D((2,2))(conv2)
    norm2 = keras.layers.BatchNormalization()(pool2)

    conv3 = keras.layers.Conv2D(32, (3,3))(norm2)
    pool3 = keras.layers.MaxPooling2D((2,2))(conv3)
    norm3 = keras.layers.BatchNormalization()(pool3)

    conv4 = keras.layers.Conv2D(32, (3,3))(norm3)
    pool4 = keras.layers.MaxPooling2D((2,2))(conv4)
    norm4 = keras.layers.BatchNormalization()(pool4)

    conv5 = keras.layers.Conv2D(32, (3,3))(norm4)
    pool5 = keras.layers.MaxPooling2D((2,2))(conv5)

    flat = keras.layers.Flatten()(pool5)

    dense1 = keras.layers.Dense(128, activation = "relu")(flat)
    dropout1 = keras.layers.Dropout(0.3)(dense1)
    dense2 = keras.layers.Dense(128, activation = "relu")(dropout1)
    dropout2 = keras.layers.Dropout(0.3)(dense2)
    dense3 = keras.layers.Dense(128, activation = "relu")(dropout2)
    #dropout3 = keras.layers.Dropout(0.3)(dense3)
    #dense4 = keras.layers.Dense(128, activation = "relu")(dropout3)
    

    out = keras.layers.Dense(clases, activation = "softmax")(dense3)

    modelo = keras.models.Model(inputs=entradaImagen, outputs = out)

    modelo.compile(optimizer="adam",loss="categorical_crossentropy",metrics=['accuracy'])
    return modelo


if __name__ == "__main__":
    pass
