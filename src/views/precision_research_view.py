import tkinter as tk
from tkinter import ttk

from time import sleep

from src.controllers.precision_research import precision_research

class PrecisionResearch():
    def __init__(self, master, connection, calibrator):
        self.master = master
        self.connection = connection
        self.calibrator = calibrator

        self.add_main_frame()

    def add_main_frame(self):
        self.start_btn = ttk.Button(self.master, text="Старт", command=self.precision_research_start)
        self.start_btn.pack()

    def precision_research_start(self):
        self.device = self.connection.get_device()


        if self.device == None:
            self.connection.connect()
            self.device = self.connection.get_device()

        self.calibrator.connect_to_calib_thread(precision_research_flag="precision_research_flag", callback = self.precision_research_callback)

    def precision_research_callback(self, calib):
        self.calib = calib
        # precision_research(self.device, self.calib)
        print(11111111)
        print(self.calib.client.is_open)
        sleep(3)
        self.calibrator.connect_to_calib_thread()

