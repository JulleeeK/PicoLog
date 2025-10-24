#ToDo:
#1. seperate all the important parts into different files, so that they can be switched out by PC program
#2. make file to log data. can be uploaded to server later?
#3. make PC program to set up Pico and copy file over to read and display in graph

from machine import ADC, I2C, Pin
from micropython_tmp117 import tmp117
import network
import ntptime
from time import sleep, localtime
from Pico_ePaper_29_D import EPD_2IN9_D

led = Pin("LED", Pin.OUT)

time = localtime()
#filename = "temp1-" + str(time[0]) + "-" + str(time[1]) + "-" + str(time[2]) + "-" + str(time[3]) + "-" + str(time[4]) +".txt"
#file = open(filename, "a+")

#setting sensor data

sda=Pin(6)
scl=Pin(7)
i2c=I2C(1,sda=sda, scl=scl, freq=400000)
tmp = tmp117.TMP117(i2c)

#setting Wifi information
#ToDo: make these values be read from config file
ssid = 'ssid'
password = 'password'

#initializing the screen
epd = EPD_2IN9_D()
epd.fill(0xff)
epd.text("Temperature: ", 1, 10, 0x00)
epd.text("Date: ", 1, 60, 0x00)
epd.text("Time: ", 1, 120, 0x00)
epd.display(epd.buffer)

def startformat():
    f = open('data.csv', 'a')
    f.write('\ndate, time, temperature')
    f.close()
    print('format written')
    
def write(values):
    f = open('data.csv', 'a')
    f.write('\n' + str(values[0]) + '.' + str(values[1]) + '.' + str(values[2]) + ', ' + str(values[3]) + ':' + str(values[4]) + ':' + str(values[5]) + ', ' + str(values[6]))
    f.close()
    print('values have been written to file')

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print('connection successful: ' + str(wlan.ifconfig()))
    epd.fill_rect(1, 200, 100, 10, 0xff)
    epd.text(wlan.ifconfig()[0], 1, 200, 0x00)
    epd.display_Partial(epd.buffer)

def writetodb(values):
    pass

def displaydata(values):
    epd.fill_rect(1, 20, 40, 10, 0xff)
    epd.text(str(values[6]), 1, 20, 0x00)
    epd.fill_rect(1, 70, 100, 10, 0xff)
    epd.text(str(values[0]) + "." + str(values[1]) + "." + str(values[2]), 1, 70, 0x00)
    epd.fill_rect(1, 130, 100, 10, 0xff)
    epd.text(str(values[3]) + ":" + str(values[4]) + ":" + str(values[5]), 1, 130, 0x00)
    epd.display_Partial(epd.buffer)

def readdata():
    temperature = tmp.temperature
    return round(temperature, 1)

def start():
    startformat()
    ts = 5
    num = 0
    #initiate database here
    connect()
    #update Time
    #ToDo: add timezones (currently just implemented with adding 2 to the time)
    try:
        ntptime.settime()
    except:
        raise Exception("npttime.settime() failed. No network connection.")
    while True:
        time_curr = localtime()
        led.toggle()
        num += 1
        value = readdata()
        # this will go to a screen later
        print(time_curr[0], time_curr[1], time_curr[2], (time_curr[3]+2), time_curr[4], time_curr[5], value)
        displaydata([time_curr[0], time_curr[1], time_curr[2], (time_curr[3]+2), time_curr[4], time_curr[5], value])
        write([time_curr[0], time_curr[1], time_curr[2], (time_curr[3]+2), time_curr[4], time_curr[5], value])
        #if num == 12:
        #    writetodb([time_curr[0], time_curr[1], time_curr[2], time_curr[3], time_curr[4], time_curr[5], value])
        #    num = 0
        sleep(ts)

