import threading
import tkinter as tk
from tkinter import ttk
from src.models.calibrator import Calibrator
import threading


class CalibView():
    calib = Calibrator()
    def __init__(self, master):
        self.master = master

        self.add_calib_status_frame()
        self.add_hello_label()

    def add_calib_status_frame(self):
        self.calib_status_frame = tk.Frame(self.master)
        self.calib_status_frame.pack(fill="x")

        self.calib_status_frame.columnconfigure(index=0, weight=1, uniform='col')
        self.calib_status_frame.columnconfigure(index=1, weight=1, uniform='col')

        self.calib_status_chbtn_var = tk.BooleanVar(value=False)

        self.calib_status_chbtn = ttk.Checkbutton(self.calib_status_frame, text="Калибратор", variable=self.calib_status_chbtn_var, command=lambda: self.set_calib_connection(self.calib_status_chbtn_var.get()))
        self.calib_status_label = ttk.Label(self.calib_status_frame, text="Отключен", foreground="red", background="#FFCDD2", anchor="center")

        self.calib_status_chbtn.grid(row=0, column=0, sticky="nsew")
        self.calib_status_label.grid(row=0, column=1, sticky="e")

    def set_calib_connection(self, connection_mode):
        def try_to_connect():
            self.calib.connection_waiting_flag = True
            self.calib.connect()
            # self.calib_status_label.config(text="Подключен", foreground="green", background="#90feb5", anchor="center")

        def stop_trying_to_connect():
            self.calib.connection_waiting_flag = False

        def to_disconnect():
            self.calib.disconnect()

        if self.calib.client:
            to_disconnect()
        else:
            if connection_mode:
                try_to_connect()
            else:
                stop_trying_to_connect()









    def add_hello_label(self):
        ttk.Label(self.master, text="Подключите калибратор...", anchor="center").place(rely=1 / 5, relwidth=1, relheight=4 / 5)