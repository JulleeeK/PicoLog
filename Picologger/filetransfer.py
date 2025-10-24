import sys
import machine
from machine import I2C, Pin
import time
import uos
import os

def startimport():
    # set connection parameters
    uart = machine.UART(0, baudrate=115200)
    uart.init(115200, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))
    uos.dupterm(uart)
    time.sleep(1)
    print("S")
    time.sleep(1)
    while True:
        v = sys.stdin.readline().strip()
        if v == "S":
            break
    time.sleep(1)
    # send over filecontent
    with open('data.csv') as f:
        print(f.read())
    # Give signal to end the transfer with unused letter
    print('H')
    # delete file since it is now on PC
    os.remove('data.csv')
