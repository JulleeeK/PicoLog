# THIS IS A WORK IN PROGRESS
# PicoLog
An expandable framework for data logging on Raspberry Picos, designed for flexibility in scientific environments.

# What?
The Goal of this project is to make a cheap and easy to use, expandable framework for logging diverse data in scientific environments. The main parts of it are the logging and copying files to PC, as well as the actual sensor. While currently only one sensor is supported, the aim is to make this compatible with as many sensors as possible.

# Why?
Scientific equipment is expensive. By making this open source and based on cheap hardware, it may increase accessibility. It will not replace expensive, specialized lab equipment, but rather provide a cheap alternative. 
The reason I started this project is a slightly broken climate chamber, which may still be usefull if the exact temperature is logged throughout experiments.

# Features I am working on
-> An easy way to add drivers for new sensors. I want to make it as easy as possible to contribute.\
-> 3D printable / easy to DIY enclosures optimized for different environments.\
-> Lora Wan module for transferring data over wide range in remote locations\
-> Database module for fixed local installations\
-> Integrations into other systems (e.G. Home Assistant)\
-> Settings menu, module importer and updater in Data Importer Software\

# Hardware
Here are some links to the hardware I used:\
Display:\
https://www.waveshare.com/wiki/Pico-ePaper-2.9-D \
Temperature Sensor:\
https://www.adafruit.com/product/4821?srsltid=AfmBOop-LRcEVgQHUQiO-RTHF9dfsrg5beyn9RiG7nexVIOL9lnbpCLe \
Rpi Pico w\

# Installation
The setup is rather easy. After setting up the rpi pico according to this guide:
https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2
Change your Wifi Information in the pico-log file. This will be set in the Data Importer in the future.
Copy over the files in Picologger to the pico.
Install the tmp117 driver using Thonny: https://pypi.org/project/micropython-tmp117/ 
When connecting it only to power, it will start logging and show the output on the screen. 
As soon as its connected to a PC, it will enter data transfer mode. Run the software in the Data-Importer folder, press start import, choose a destination folder, then connect the rpi in order to import the data from the pico.
