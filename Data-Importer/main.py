import datetime
import os
import tkinter as tk
from threading import Thread
from tkinter import ttk, filedialog as fd
from tkinter.messagebox import showinfo

import matplotlib.pyplot as plt
import numpy as np
from serial import Serial
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

directory = ""

class Import(Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        # Configure the serial connection
        port = "COM3"
        baudrate = 115200
        connect = True
        #wait for connection to work
        print('Waiting for connection to pico...')
        while connect:
            try:
                serial_connection = Serial(port, baudrate)
                connect = False
                print("Connection Established")
            except:
                pass
        # Open a file on your computer to write the received data
        destination_file = os.path.join(directory, (str(datetime.datetime.now()).replace('.', '-').replace(':', '-').replace(' ', '') + ".csv"))
        # wait for confirmation of connection from pico
        while True:
            if serial_connection.read() == b"S":
                print("Starting filetransfer now, do not disconnect device!")
                break
        # send message to start file transfer
        serial_connection.write(b"S\n")
        # skip next two symbols, since they are from the picos confirmation phrase (dirty fix, but should work)
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


class App (tk.Tk):
    def __init__(self):
        super().__init__()
        # put base GUI elements here
        self.title('Picologger')
        # self.geometry('2000x1000')
        self.style = ttk.Style(self)
        self.import_button = ttk.Button(self, text='Start Importing Logs')
        self.import_button['command'] = self.manage_import
        self.import_button.pack(ipadx=10, ipady=5)
        self.graph_button = ttk.Button(self, text='Show Graph')
        self.graph_button['command'] = self.show_graph
        self.graph_button.pack(ipadx=1, ipady=5)
        self.prog_bar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=280)

    def manage_import(self):
        global directory
        # disable button so no othe threads are started
        self.import_button['state'] = tk.DISABLED
        # ask for directory to save file in
        directory = fd.askdirectory()
        # start the thread
        import_thread = Import()
        import_thread.start()
        # make a progress bar
        self.prog_bar.pack(ipadx=1, ipady=6)
        self.prog_bar.start()
        self.monitor(import_thread)

    def monitor(self, thread):
        if thread.is_alive():
            # check the thread every 100ms
            self.after(100, lambda: self.monitor(thread))
        else:
            print('thread finished!')
            self.import_button['state'] = tk.NORMAL
            self.prog_bar.stop()
            self.prog_bar.destroy()
            self.prog_bar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=280)
            showinfo(title='Import Finished', message='The import has finnished! Press the \'Show Graph\' button to show a graph of your data.')

    def show_graph(self):
        # this might have to be changed for
        # generate values from csv file
        data = np.genfromtxt(fd.askopenfilename(), delimiter=', ', skip_footer=1, names=True, dtype=None)
        fig = plt.figure()
        figure_canvas = FigureCanvasTkAgg(fig, self)
        NavigationToolbar2Tk(figure_canvas, self)
        ax1 = fig.add_subplot(111)
        ax1.set_title("Temperature Log")
        # data.dtype.names gets an array of the names of the values. In the standard case, that is time at second
        # place and temp at 3rd. Still need to figure out how more than 24 will work, since time values might exist twice
        ax1.set_xlabel(data.dtype.names[1])
        ax1.set_ylabel(data.dtype.names[2])
        # make labels on x axis not overlap
        ax1.xaxis.set_major_locator(plt.AutoLocator())
        ax1.plot(data[data.dtype.names[1]], data[data.dtype.names[2]], color='r')
        # show the graph on the tkinter window
        figure_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
if __name__ == "__main__":
    app = App()
    app.mainloop()