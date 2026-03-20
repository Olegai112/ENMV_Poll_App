import tkinter as tk
from logging import disable
from tkinter import ttk

from time import sleep

from src.services.load_settings import Settings
from src.controllers.precision_research import precision_research

class PrecisionResearch():
    def __init__(self, master, connection, calibrator):
        self.master = master
        self.connection = connection
        self.calibrator = calibrator

        self.add_main_frame()

    def add_main_frame(self):
        self.header_frame = tk.Frame(self.master)  # header
        self.header_frame.pack(fill="x")

        self.hello_label = ttk.Label(self.header_frame, text="Исследование точности")

        self.ao_chbtn_var = tk.BooleanVar(value=False)
        self.ao_chbtn = ttk.Checkbutton(self.header_frame, text="AO:", variable=self.ao_chbtn_var, command=self.set_ao)
        self.ao_chbtn.pack(side="left")

        self.selected_ao_mode = tk.StringVar(value="ESX")

        self.esx_rbtn = ttk.Radiobutton(self.header_frame, variable=self.selected_ao_mode, value="ESX", state="disable")
        self.esx_rbtn.pack(side="left")
        self.esx_label = ttk.Label(self.header_frame, text="ESX")
        self.esx_label.pack(side="left")

        self.enmv_rbtn = ttk.Radiobutton(self.header_frame, variable=self.selected_ao_mode, value="ENMV", state="disable")
        self.enmv_rbtn.pack(side="left")
        self.enmv_label = ttk.Label(self.header_frame, text="ENMV")
        self.enmv_label.pack(side="left")

        self.two_pass_chbtn_var = tk.BooleanVar(value=False)
        self.two_pass_chbtn = ttk.Checkbutton(self.header_frame, text="Второй проход", variable=self.two_pass_chbtn_var, command=self.second_pass)
        self.two_pass_chbtn.pack(side="right")

        self.settings_frame = tk.Frame(self.master, bg="green") # main
        self.settings_frame.pack(fill="both", expand=True)

        self.settings_frame.columnconfigure(index=0, weight=0)
        self.settings_frame.columnconfigure(index=1, weight=1)
        self.settings_frame.columnconfigure(index=2, weight=1)
        self.settings_frame.columnconfigure(index=3, weight=1)
        self.settings_frame.rowconfigure(index=0, weight=1)
        self.settings_frame.rowconfigure(index=1, weight=1)
        self.settings_frame.rowconfigure(index=2, weight=1)

        self.start_value_label = ttk.Label(self.settings_frame, text="Начальная точка")
        self.end_value_label = ttk.Label(self.settings_frame, text="Конечная точка")
        self.step_value_label = ttk.Label(self.settings_frame, text="Шаг")

        self.start_value_label.grid(column=0, row=0, sticky="nsew")
        self.end_value_label.grid(column=0, row=1, sticky="nsew")
        self.step_value_label.grid(column=0, row=2, sticky="nsew")

        self.start_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8)
        self.end_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8)
        self.step_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8)

        self.start_value_spibox.set(Settings.get("POSITIVE_START"))
        self.end_value_spibox.set(Settings.get("POSITIVE_END"))
        self.step_value_spibox.set(Settings.get("POSITIVE_STEP"))

        self.start_value_spibox.grid(column=1, row=0)
        self.end_value_spibox.grid(column=1, row=1)
        self.step_value_spibox.grid(column=1, row=2)

        self.second_pass_start_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8, state="disable")
        self.second_pass_end_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8, state="disable")
        self.second_pass_step_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8, state="disable")

        self.second_pass_start_value_spibox.set(Settings.get("NEGATIVE_START"))
        self.second_pass_end_value_spibox.set(Settings.get("NEGATIVE_END"))
        self.second_pass_step_value_spibox.set(Settings.get("NEGATIVE_STEP"))

        self.second_pass_start_value_spibox.grid(column=3, row=0)
        self.second_pass_end_value_spibox.grid(column=3, row=1)
        self.second_pass_step_value_spibox.grid(column=3, row=2)

        self.footer_frame = tk.Frame(self.master) # footer
        self.footer_frame.pack(fill="x")

        self.start_btn = ttk.Button(self.footer_frame, text="Старт", command=self.precision_research_start)
        self.start_btn.pack(side="right")
        self.pause_btn = ttk.Button(self.footer_frame, text="Пауза")
        self.pause_btn.pack(side="right")
        self.stop_btn = ttk.Button(self.footer_frame, text="Стоп")
        self.stop_btn.pack(side="right")
        self.progressbar = ttk.Progressbar(self.footer_frame, orient="horizontal")
        self.progressbar.pack(expand=True, fill="x")

    def precision_research_start(self):
        self.save_settings()

        self.device = self.connection.get_device()
        if self.device == None:
            self.connection.connect()
            self.connection.config_frame_var()
            self.device = self.connection.get_device()

        self.calib = self.calibrator.get_calib()
        if not self.calib.client:
            self.calibrator.connect_to_calib_thread(precision_research_flag=True, callback = self.precision_research_callback)
        else:
            self.precision_research_callback(self.calib)

    def precision_research_callback(self, calib):
        self.calib = calib
        self.calib.parameter = "current"
        precision_research(self.device, self.calib)
        self.calibrator.connect_to_calib_thread(precision_research_flag=False)
        self.connection.disconnect()

    def second_pass(self):
        second_pass = self.two_pass_chbtn_var.get()
        Settings.push("TWO_PASS", changed_setting=second_pass)
        if second_pass:
            self.second_pass_start_value_spibox.config(state="enable")
            self.second_pass_end_value_spibox.config(state="enable")
            self.second_pass_step_value_spibox.config(state="enable")
        else:
            self.second_pass_start_value_spibox.config(state="disable")
            self.second_pass_end_value_spibox.config(state="disable")
            self.second_pass_step_value_spibox.config(state="disable")

    def save_settings(self):
        Settings.push("POSITIVE_START", changed_setting=float(self.start_value_spibox.get()))
        Settings.push("POSITIVE_END", changed_setting=float(self.end_value_spibox.get()))
        Settings.push("POSITIVE_STEP", changed_setting=float(self.step_value_spibox.get()))

        Settings.push("NEGATIVE_START", changed_setting=float(self.second_pass_start_value_spibox.get()))
        Settings.push("NEGATIVE_END", changed_setting=float(self.second_pass_end_value_spibox.get()))
        Settings.push("NEGATIVE_STEP", changed_setting=float(self.second_pass_step_value_spibox.get()))

        if self.ao_chbtn_var.get():
            Settings.push("device", "AO_MODE", changed_setting=self.selected_ao_mode.get())
        else:
            Settings.push("device", "AO_MODE", changed_setting="OFF")

    def set_ao(self):
        if self.ao_chbtn_var.get():
            self.esx_rbtn.config(state="enable")
            self.enmv_rbtn.config(state="enable")
        else:
            self.esx_rbtn.config(state="disable")
            self.enmv_rbtn.config(state="disable")