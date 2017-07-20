import tensorflow.contrib.keras as keras

def GenerarModelo(anchoimg,altoimg,clases):
    entradaImagen = keras.layers.Input(shape=(altoimg,anchoimg))

    conv1 = keras.layers.Conv2D(64, (3,3))(entradaImagen)
    pool1 = keras.layers.MaxPooling2D((2,2))(conv1)
    norm1 = keras.layers.normalization.BatchNormalization()(pool1)

    conv2 = keras.layers.Conv2D(64, (3,3))(norm1)
    pool2 = keras.layers.MaxPooling2D((2,2))(conv2)
    norm2 = keras.layers.normalization.BatchNormalization()(pool2)

    conv3 = keras.layers.Conv2D(64, (3,3))(norm2)
    pool3 = keras.layers.MaxPooling2D((2,2))(conv3)
    norm3 = keras.layers.normalization.BatchNormalization()(pool3)

    flat = keras.layers.core.Flatten()(norm3)

    dense1 = keras.layers.core.Dense(128, activation = "relu")(flat)
    dropout1 = keras.ayers.core.Dropout(0.3)(dense1)
    dense2 = keras.layers.core.Dense(128, activation = "relu")(dropout1)

    out = keras.layers.core.Dense(clases, activation = "softmax")(dense2)

    modelo = Model(inputs=entradaImagen, outputs = out)

    return modelo
