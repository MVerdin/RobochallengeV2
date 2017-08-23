#!/bin/bash

sudo raspi-config
sudo apt update
sudo apt purge wolfram-engine
sudo apt upgrade
sudo apt install git
sudo apt install python3-dev
sudo apt install pi-bluetooth
sudo apt install bluetooth bluez
sudo apt install python3-pip
sudo apt install libbluetooth-dev
sudo apt install libhdf5-dev
sudo pip3 install h5py
sudo pip3 install pybluez
sudo pip3 install numpy
sudo pip3 install RPi.GPIO
sudo pip3 install picamera

sudo apt install build-essential cmake pkg-config
sudo apt install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install libxvidcore-dev libx264-dev
sudo apt install libgtk2.0-dev
sudo apt install libatlas-base-dev gfortran

#sudo apt install build-essential
#sudo apt install cmake libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
#sudo apt install libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

cd ~

git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D INSTALL_PYTHON_EXAMPLES=ON \
  -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
  -D BUILD_EXAMPLES=ON ..

make -j4

sudo make install
sudo ldconfig
