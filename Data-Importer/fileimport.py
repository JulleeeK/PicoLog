import serial
import datetime
import time

def start():
    # Configure the serial connection
    port = "COM3"
    baudrate = 115200
    connect = True
    #wait for connection to work
    print('Waiting for connection to pico...')
    while connect:
        try:
            serial_connection = serial.Serial(port, baudrate)
            connect = False
            print("Connection Established")
        except:
            pass
    # Open a file on your computer to write the received data
    destination_file = str(datetime.datetime.now()).replace('.', '-').replace(':', '-').replace(' ', '') + ".csv"
    # wait for confirmation of connection from pico
    while True:
        if serial_connection.read() == b"S":
            print("Starting filetransfer now, do not disconnect device!")
            break
    # send message to start file transfer
    serial_connection.write(b"S\n")
    # skip next two symbols, since they are from the picos confirmation phrase (dirty fix, but should work for now)
    data = serial_connection.read()
    data = serial_connection.read()
    data = serial_connection.read()
    data = serial_connection.read()
    # Read and write data until the transfer is complete
    while True:
        data = serial_connection.read()
        # check for complete message
        if data == b"H":
            break
        print(data)
        with open(destination_file, "ab") as f:
            f.write(data)
    serial_connection.close()
    print("Finished transfer, you can disconnect the device now.")