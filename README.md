# RobochallengeV2
This repository has the scrips used to train and control an autonomous competitor robot, using a Raspberry Pi 3 Model B with a camera module feeding images to a convolutional deep neural network and using its output to control the two motors of the robot. The software is divided into three parts: the data collecting script, the training script, and the fighting script.

# Collecting data
The data collecting script (RaspberryPi/recolectardatos.py) creates a Bluetooth connection to control the robot remotely, then takes photos with the camera and binds each photo with the command being executed at the moment. Those photos are saved, in packets of a hundred, to a USB drive (if one is found during the start of the script) or to the Raspberry Pi's internal memory.

# Training the Neural Network
With enough training data saved, it is transferred to a computer and using the training software (entrenamientoGUI.py) a new neural network model is generated and trained. The layers and connections of the neural network are defined in the "modelos.py" file.

# Fighting
When the model is trained and saved it is copied to the Raspberry Pi's internal memory. There, the model is loaded by the fighting script (RaspberryPi/pelear.py) and used to predict the best way to control the motors.

