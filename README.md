# RobochallengeV2
This repository has the scrips used to train and controll an autonomous competitor robot, using a Raspberry Pi 3 Model B with a camera module feeding images to a convolutional deep neural network and using it's output to control the two motors of the robot. The software is divided in three parts: the data collecting script, the training script, and the fighting script.

# Collecting data
The data collecting script (RaspberryPi/recolectardatos.py) creates a bluetooth conection to control the robot remotely, then takes photos with the camera and binds each photo with the command beign executed at the moment. Those photos are saved, in packets of a hundred, to a USB drive (if one is found during the start of the script) or to the Raspberry Pi's internal memory.

# Training the Neural Network
With enough training data saved

