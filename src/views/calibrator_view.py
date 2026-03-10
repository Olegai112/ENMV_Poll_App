import tkinter as tk
from tkinter import ttk

import threading

from time import sleep
from src.models.calibrator import Calibrator
from src.services.load_settings import Settings


class CalibView():
    calib = None
    def __init__(self, master):
        self.master = master

        self.calib_status()
        self.calib_settings_frame = None

    def calib_status(self):
        self.calib_status_frame = tk.Frame(self.master)
        self.calib_status_frame.pack(fill="x")

        self.calib_status_frame.columnconfigure(index=0, weight=1, uniform='col')
        self.calib_status_frame.columnconfigure(index=1, weight=1, uniform='col')
        self.calib_status_frame.rowconfigure(index=0, weight=1, uniform='row')
        self.calib_status_frame.rowconfigure(index=1, weight=1, uniform='row')


        self.calib_status_chbtn_var = tk.BooleanVar(value=False)

        self.calib_status_label = ttk.Label(self.calib_status_frame, text="Отключен", foreground="red", background="#FFCDD2", anchor="c")

        def calib_settings_status():
            if self.calib_status_chbtn_var.get():
                self.calib = Calibrator()

                def calib_connection():
                    while True:
                        try:
                            self.calib.connect()
                            if self.calib.send_response([166]*8)[0] != b'':
                                self.calib_status_label.config(text="Подключен", foreground="green", background="#90feb5")
                                return
                            sleep(1)
                        except Exception as e:
                            pass
                calib_connection_thread = threading.Thread(target=calib_connection, daemon=True)
                calib_connection_thread.start()
                while True:
                    if calib_connection_thread.is_alive():
                        print(123)
                        sleep(0.1)
                    else:
                        break
                self.calib_settings()
            else:
                self.calib.disconnect()
                self.calib = None
                self.calib_status_label.config(text="Отключен", foreground="red", background="#FFCDD2")

        calib_status_chbtn = ttk.Checkbutton(self.calib_status_frame, text="Калибратор", variable=self.calib_status_chbtn_var, command=calib_settings_status)

        self.calib_mode_combobox = ttk.Combobox(self.calib_status_frame, values=["Измерение", "Воспроизведение"], justify="center", state="readonly")
        self.calib_parameter_combobox = ttk.Combobox(self.calib_status_frame, values=["Ток", "Напряжение", "Сопротивление"], justify="center", state="readonly")

        self.calib_mode_combobox.bind('<<ComboboxSelected>>', self.calib_settings)
        self.calib_parameter_combobox.bind('<<ComboboxSelected>>', self.calib_settings)

        calib_status_chbtn.grid(row=0, column=0, sticky="nsew")
        self.calib_status_label.grid(row=0, column=1, sticky="e")
        self.calib_mode_combobox.grid(row=1, column=0, sticky="nsew")
        self.calib_parameter_combobox.grid(row=1, column=1, sticky="nsew")

    def calib_settings(self, event=None):
        if self.calib_settings_frame != None:
            self.calib_settings_frame.destroy()

        self.calib_settings_frame = tk.Frame(self.master)
        self.calib_settings_frame.pack(fill="both", expand=True)

        self.calib_settings_frame.columnconfigure(index=0, weight=1)
        self.calib_settings_frame.columnconfigure(index=1, weight=1)
        self.calib_settings_frame.columnconfigure(index=2, weight=1)
        self.calib_settings_frame.rowconfigure(index=0, weight=1, uniform='row')
        self.calib_settings_frame.rowconfigure(index=1, weight=1, uniform='row')

        if self.calib_mode_combobox.get() == "Измерение":
            measure_label = ttk.Label(self.calib_settings_frame, text="Измеренное значение:", relief="ridge", anchor="c", padding=3)
            measure_label.grid(row=0, column=0, rowspan=2, sticky="nsew")
            measure_unit_label = ttk.Label(self.calib_settings_frame, text="", relief="ridge", anchor="c", padding=3)
            measure_unit_label.grid(row=0, column=2, rowspan=2, sticky="nsew")
            measure_value_label = ttk.Label(self.calib_settings_frame, text="1.125846", relief="ridge", anchor="c", padding=3, background="black", foreground="white")
            measure_value_label.grid(row=0, column=1, rowspan=2, sticky="nsew")

            if self.calib_parameter_combobox.get() == "Ток":
                measure_unit_label["text"] = "мА"
                Settings.push("PARAMETER", changed_setting="current")
            elif self.calib_parameter_combobox.get() == "Напряжение":
                measure_unit_label["text"] = "В"
                Settings.push("PARAMETER", changed_setting="voltage")
            elif self.calib_parameter_combobox.get() == "Сопротивление":
                measure_unit_label["text"] = "Ом"
                Settings.push("PARAMETER", changed_setting="resistance")
            else:
                return

            if self.calib != None:
                self.calib.parameter = Settings.config["PARAMETER"]
                resp = self.calib.send_response(self.calib.measure_value(1))
                print(resp[1])
                measure_value_label["text"] = str(round(self.calib.send_response(self.calib.measure_value())[1], 6))

            # def calib_meausrement():
            #     while self.calib != None:
            #         measure_value_label["text"] = str(self.calib.send_response(self.calib.measure_value())[1])
            # # self.calib_connection_thread = threading.Thread(target=calib_meausrement, daemon=True)
            # # self.calib_connection_thread.start()

        elif self.calib_mode_combobox.get() == "Воспроизведение":
            return
        else:
            return





