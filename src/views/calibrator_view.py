import tkinter as tk
from tkinter import ttk

import threading

from time import sleep

from src.models.calibrator import Calibrator
from src.services.load_settings import Settings


class CalibView():
    calib = None

    def calib_read(self):
        while self.calib != None and self.calib_thread_flag:
            try:
                value = round(self.calib.send_response(self.calib.read_value())[1], 6)
                self.master.after(0, lambda: self.set_value_label.config(text=str(value)))
                if self.calib_read_stop_reading:
                    self.calib.send_response(self.calib.set_value(float(self.to_set_value_sb.get())))
                    self.calib_read_stop_reading = False
            except Exception as e:
                print(f"Ошибка в потоке: {e}")

    def __init__(self, master):
        self.master = master

        self.calib_status()
        self.calib_settings_frame = None
        self.calib_set_thread = threading.Thread(target=self.calib_read, daemon=True)

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
                    self.calib_connection_thread_flag = True
                    while self.calib_connection_thread_flag:
                        try:
                            self.calib.connect()
                            if self.calib.send_response([166]*8)[0] != b'':
                                self.calib_connection_thread_flag = False
                                self.master.after(0, self.calib_settings)
                                self.master.after(0, lambda:self.calib_status_label.config(text="Подключен", foreground="green", background="#90feb5"))
                            sleep(1)
                        except Exception as e:
                            self.calib_connection_thread_flag = False
                calib_connection_thread = threading.Thread(target=calib_connection, daemon=True)
                calib_connection_thread.start()
            else:
                self.calib.disconnect() # TODO с отключенным калибратором
                self.calib = None
                self.calib_status_label.config(text="Отключен", foreground="red", background="#FFCDD2")
                self.calib_settings()

        calib_status_chbtn = ttk.Checkbutton(self.calib_status_frame, text="Калибратор", variable=self.calib_status_chbtn_var, command=calib_settings_status)

        self.calib_mode_combobox = ttk.Combobox(self.calib_status_frame, values=["Измерение", "Воспроизведение"], justify="center", state="readonly")
        self.calib_parameter_combobox = ttk.Combobox(self.calib_status_frame, values=["Ток", "Напряжение", "Сопротивление"], justify="center", state="disabled")

        self.calib_mode_combobox.bind('<<ComboboxSelected>>', self.calib_settings)
        self.calib_parameter_combobox.bind('<<ComboboxSelected>>', self.calib_settings)

        calib_status_chbtn.grid(row=0, column=0, sticky="nsew")
        self.calib_status_label.grid(row=0, column=1, sticky="e")
        self.calib_mode_combobox.grid(row=1, column=0, sticky="nsew")
        self.calib_parameter_combobox.grid(row=1, column=1, sticky="nsew")

    def calib_settings(self, event=None):
        print(123)
        def parameter_changer():
            if self.calib_parameter_combobox.get() == "Ток":
                self.unit_label["text"] = "мА"
                Settings.push("PARAMETER", changed_setting="current")
            elif self.calib_parameter_combobox.get() == "Напряжение":
                self.unit_label["text"] = "В"
                Settings.push("PARAMETER", changed_setting="voltage")
            elif self.calib_parameter_combobox.get() == "Сопротивление":
                self.unit_label["text"] = "Ом"
                Settings.push("PARAMETER", changed_setting="resistance")
            else:
                return False

            if self.calib != None:
                self.calib_thread_flag = True
                self.calib.parameter = Settings.config["PARAMETER"]
                return True
            else:
                return False

        self.calib_parameter_combobox.config(state="readonly")
        self.calib_thread_flag = False
        print(456)

        if  self.calib_set_thread.is_alive():
            print("alive")
            self.calib_set_thread.join()
            print("done")

        if self.calib_settings_frame != None:
            self.calib_settings_frame.destroy()
        print(111111)
        self.calib_settings_frame = tk.Frame(self.master)
        self.calib_settings_frame.pack(fill="both", expand=True)
        self.unit_label = ttk.Label(self.calib_settings_frame, text="", relief="ridge", anchor="c", padding=3, width=1)

        self.calib_settings_frame.columnconfigure(index=0, weight=1, uniform='col')
        self.calib_settings_frame.columnconfigure(index=1, weight=1, uniform='col')
        self.calib_settings_frame.columnconfigure(index=2, weight=1, uniform='col')
        self.calib_settings_frame.columnconfigure(index=3, weight=1, uniform='col')
        self.calib_settings_frame.rowconfigure(index=0, weight=1, uniform='row')
        self.calib_settings_frame.rowconfigure(index=1, weight=1, uniform='row')


        if self.calib_mode_combobox.get() == "Измерение":
            measure_label = ttk.Label(self.calib_settings_frame, text="Измеренное значение", relief="ridge", anchor="c", padding=3, width=1)
            measure_label.grid(row=0, column=0, rowspan=2, columnspan= 2, sticky="nsew")
            self.unit_label.grid(row=0, column=3, rowspan=2, sticky="nsew")
            self.measure_value_label = ttk.Label(self.calib_settings_frame, text="", relief="ridge", anchor="c", padding=3, background="black", foreground="white", width=1)
            self.measure_value_label.grid(row=0, column=2, rowspan=2, sticky="nsew")

            if parameter_changer():
                self.calib_thread_flag = True
                def calib_measurement():
                    print(self.calib, self.calib_thread_flag)
                    self.calib.send_response(self.calib.measure_value(1))
                    while self.calib != None and self.calib_thread_flag:
                        try:
                            print(self.calib, self.calib_thread_flag)
                            self.master.after(0, lambda:self.measure_value_label.config(text = str(round(self.calib.send_response(self.calib.measure_value())[1], 6))))
                            sleep(0.5)
                        except Exception:
                            pass
                calib_measurement_thread = threading.Thread(target=calib_measurement, daemon=True)
                calib_measurement_thread.start()

        elif self.calib_mode_combobox.get() == "Воспроизведение":
            set_label = ttk.Label(self.calib_settings_frame, text="Установленное значение", relief="ridge", anchor="c", padding=3, width=1)
            set_label.grid(row=0, column=0, columnspan=2, sticky="nsew")
            self.unit_label.grid(row=0, column=3, sticky="nsew")
            self.set_value_label = ttk.Label(self.calib_settings_frame, text="", relief="ridge", anchor="c", padding=3, background="black", foreground="white", width=1)
            self.set_value_label.grid(row=0, column=2, sticky="nsew")
            to_set_value_label = ttk.Label(self.calib_settings_frame, text = "Установить:", width=11)
            to_set_value_label.grid(row=1, column=1, sticky="e")

            def validate_spinbox(char, action, current_text, new_text):
                """Разрешаем только цифры"""
                if action == '0':
                    return True
                if char.isdigit():
                    return True
                if char == '.':
                    if '.' in current_text:
                        return False
                    if current_text == "":
                        return False
                    return True
                return False
            vcmd = self.calib_settings_frame.register(validate_spinbox)
            self.to_set_value_sb = ttk.Spinbox(self.calib_settings_frame,from_=-100.0, to=100.0,  increment=0.000001, justify="center", validate="key", validatecommand=(vcmd, '%S', '%d', '%s', '%P'))
            self.to_set_value_sb.grid(row=1, column=2, sticky="ew")

            def stop_reading():
                self.calib_read_stop_reading = True
            self.to_set_value_btn = ttk.Button(self.calib_settings_frame, text="--->", command=stop_reading)
            self.to_set_value_btn.grid(row=1, column=3, sticky="ew")
            self.to_set_value_btn.config(state="disabled")

            if parameter_changer():
                self.calib.send_response(self.calib.set_value())
                self.to_set_value_btn.config(state="enabled")
                self.calib_thread_flag = True
                self.calib_read_stop_reading = False
                self.calib_set_thread.start()
        else:
            return





