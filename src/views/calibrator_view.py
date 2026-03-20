import tkinter as tk
from tkinter import ttk

from time import sleep
import threading

from src.models.calibrator import Calibrator

class CalibView():
    calib = Calibrator()
    def __init__(self, master):

        self.master = master
        self.add_calib_status_frame()

        ttk.Label(self.master, text="Подключите калибратор...", anchor="center").place(rely=1/5, relwidth=1, relheight=4/5)

    def get_calib(self):
        return self.calib

    def add_calib_status_frame(self):
        self.calib_status_frame = tk.Frame(self.master)
        self.calib_status_frame.pack(fill="x")

        self.calib_status_frame.columnconfigure(index=0, weight=1, uniform='col')
        self.calib_status_frame.columnconfigure(index=1, weight=1, uniform='col')

        self.calib_status_chbtn_var = tk.BooleanVar(value=False)

        self.calib_status_chbtn = ttk.Checkbutton(self.calib_status_frame, text="Калибратор", variable=self.calib_status_chbtn_var, command=self.connect_to_calib_thread)
        self.calib_status_label = ttk.Label(self.calib_status_frame, text="Отключен", foreground="red", background="#FFCDD2", anchor="center")

        self.calib_status_chbtn.grid(row=0, column=0, sticky="nsew")
        self.calib_status_label.grid(row=0, column=1, sticky="e")

        # self.connection_check_flag = False
        # self.connection_status = True


    def connect_to_calib_thread(self, precision_research_flag = None, callback = None):
        self.connect_to_calib_tread = threading.Thread(target=lambda: self.connect_to_calib(callback = callback), daemon=True)
        # self.connection_check_thread = threading.Thread(target=self.connection_check, daemon=True)
        if precision_research_flag != None:
            if precision_research_flag:
                self.calib_status = True
            else:
                self.calib_status = False

        else:
            self.calib_status = self.calib_status_chbtn_var.get()
        self.connect_to_calib_tread.start()

    def connect_to_calib(self, callback = None):
        if self.calib_status:
            while True:
                try:
                    if not self.calib.client:
                        self.calib.connect()
                    break
                except Exception as e:
                    print(f"connect{e}")
                    break

            # while True:
            #     try:
            #         resp = self.calib.send_response([166] * 8)[0][0]
            #     except Exception as e:
            #         print(e)
            #         sleep(1)
            #     if resp == 166:
            #         break

            while not self.calib.send_response([166]*8)[0][0] == 166:
                sleep(1)
                pass
        else:
            try:
                self.calib.disconnect()
                self.calib.client = None
            except Exception as e:
                print(f"disconnect{e}")

        if self.calib.client:
            self.master.after(0, self.calib_status_label.config(text="Подключен", foreground="green", background="#90feb5", anchor="center"))
            self.master.after(0, self.add_calib_work_frame())
            if callback != None:
                callback(self.calib)
            # self.connection_check_thread.start()
        else:
            self.master.after(0, self.calib_status_label.config(text="Отключен", foreground="red", background="#FFCDD2", anchor="center"))
            self.calib_work_frame.destroy()


    # def connection_check(self):
    #     while self.calib.client.is_open:
    #         sleep(10)
    #         self.connection_check_flag = True
    #         print(self.connection_status)
    #         if not self.connection_status:
    #             try:
    #                 self.calib.disconnect()
    #             except Exception as e:
    #                 print(e)
    #                 self.calib.client.is_open = False
    #             self.master.after(0, self.calib_status_label.config(text="Отключен", foreground="red", background="#FFCDD2", anchor="center"))


    def add_calib_work_frame(self):
        self.calib_work_frame = tk.Frame(self.master, bg="green")
        self.calib_work_frame.pack(fill="both", expand=True)

        self.calib_setting_frame = tk.Frame(self.calib_work_frame)
        self.calib_setting_frame.place(relheight=1/4, relwidth=1)

        # self.calib_work_frame.columnconfigure(index=0, weight=1, uniform='col')
        # self.calib_work_frame.columnconfigure(index=1, weight=1, uniform='col')
        # self.calib_work_frame.rowconfigure(index=0, weight=1)
        # self.calib_work_frame.rowconfigure(index=1, weight=1)

        self.calib_mode_frame = tk.Frame(self.calib_work_frame)

        self.calib_workin_thread = threading.Thread(target=self.calib_workin, daemon=True)

        self.calib_mode_combobox = ttk.Combobox(self.calib_setting_frame, values=["Измерение", "Воспроизведение"], justify="center", state="readonly")
        # self.calib_mode_combobox.set("Измерение")
        self.unit = ""
        # self.add_chosen_mode_vidgets()
        self.calib_parameter_combobox = ttk.Combobox(self.calib_setting_frame, values=["Ток", "Напряжение", "Сопротивление"], justify="center", state="disabled")
        # self.calib_parameter_combobox.set("Ток")
        # self.add_chosen_parameter_unit()


        self.calib_mode_frame.columnconfigure(index=0, weight=1, uniform='col')
        self.calib_mode_frame.columnconfigure(index=1, weight=1, uniform='col')
        self.calib_mode_frame.columnconfigure(index=2, weight=1, uniform='col')
        self.calib_mode_frame.columnconfigure(index=3, weight=1, uniform='col')
        self.calib_mode_frame.rowconfigure(index=0, weight=1, uniform='row')
        self.calib_mode_frame.rowconfigure(index=1, weight=1, uniform='row')

        self.calib_mode_combobox.bind('<<ComboboxSelected>>', self.add_chosen_mode_vidgets)
        self.calib_parameter_combobox.bind('<<ComboboxSelected>>', self.add_chosen_parameter_unit)

        # self.calib_mode_combobox.grid(row=0, column=0, sticky="nsew")
        # self.calib_parameter_combobox.grid(row=0, column=1, sticky="ew")
        # self.calib_mode_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.calib_mode_combobox.pack(side="left", fill="both", expand=True)
        self.calib_parameter_combobox.pack(side="left", fill="both", expand=True)
        self.calib_mode_frame.place(rely = 1/4, relheight=3/4, relwidth=1)

        # self.calib_workin_thread.start()


    def add_chosen_mode_vidgets(self, event=None):
        for widget in self.calib_mode_frame.winfo_children():
            widget.destroy()

        try:
            self.unit_label.config(text=self.unit)
        except:
            pass

        self.chosen_mode = self.calib_mode_combobox.get()
        if self.chosen_mode == "Измерение":
            self.add_measure_vidgets()
        elif self.chosen_mode == "Воспроизведение":
            self.add_set_vidgets()
        self.calib_parameter_combobox.config(state="readonly")

    def add_chosen_parameter_unit(self, event=None):
        self.chosen_parameter = self.calib_parameter_combobox.get()
        if self.chosen_parameter == "Ток":
            self.unit = "мА"
            self.calib.parameter = "current"
        elif self.chosen_parameter == "Напряжение":
            self.unit = "В"
            self.calib.parameter = "voltage"
        elif self.chosen_parameter == "Сопротивление":
            self.unit = "Ом"
            self.calib.parameter = "resistance"
        self.unit_label.config(text=self.unit)

        if not self.calib_workin_thread.is_alive():
            self.calib_workin_thread.start()

    def add_measure_vidgets(self):
        self.measure_label = ttk.Label(self.calib_mode_frame, text="Измеренное значение", relief="ridge", anchor="center", padding=3, width=1)
        self.measure_value_label = ttk.Label(self.calib_mode_frame, text="", relief="ridge", anchor="center", padding=3, background="black", foreground="white", width=1)
        self.unit_label = ttk.Label(self.calib_mode_frame, text=self.unit, relief="ridge", anchor="center", padding=3, width=1)

        self.measure_label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.measure_value_label.grid(row=0, column=2, sticky="nsew")
        self.unit_label.grid(row=0, column=3, sticky="nsew")

    def add_set_vidgets(self):
        self.set_label = ttk.Label(self.calib_mode_frame, text="Установленное значение", relief="ridge", anchor="center", padding=3, width=1)
        self.set_value_label = ttk.Label(self.calib_mode_frame, text="", relief="ridge", anchor="center", padding=3, background="black", foreground="white", width=1)
        self.unit_label = ttk.Label(self.calib_mode_frame, text=self.unit, relief="ridge", anchor="center", padding=3, width=1)
        self.to_set_value_label = ttk.Label(self.calib_mode_frame, text="Установить:", width=11)
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
        vcmd = self.calib_mode_frame.register(validate_spinbox)
        self.to_set_value_sb = ttk.Spinbox(self.calib_mode_frame, from_=-100.0, to=100.0, increment=0.000001, justify="center", validate="key", validatecommand=(vcmd, '%S', '%d', '%s', '%P'))
        self.to_set_value_btn = ttk.Button(self.calib_mode_frame, text="--->", command=self.to_set_value)

        self.to_set_value_btn_flag = False

        self.set_label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.set_value_label.grid(row=0, column=2, sticky="nsew")
        self.unit_label.grid(row=0, column=3, sticky="nsew")
        self.to_set_value_label.grid(row=1, column=1, sticky="e")
        self.to_set_value_sb.grid(row=1, column=2, sticky="ew")
        self.to_set_value_btn.grid(row=1, column=3, sticky="ew")

    def calib_workin(self):
        self.responce = ""
        calib_flag = True
        try:
            counter = 0
            while self.calib.client.is_open:
                if self.chosen_mode == "Измерение":
                    counter += 1
                    if counter % 10 == 0:
                        calib_flag = True
                    print(counter)
                    print(calib_flag)
                    if calib_flag:
                        command = self.calib.measure_value()
                        calib_flag = False
                    else:
                        command = self.calib.measure_value()
                    self.master.after(0, self.measure_value_label.config(text = self.responce))
                elif self.chosen_mode == "Воспроизведение":
                    if self.to_set_value_btn_flag:
                        self.calib_status_chbtn.config(state="disabled")
                        self.calib.send_response(self.calib.set_value(self.value_to_set))
                        self.to_set_value_btn_flag = False
                        self.calib_status_chbtn.config(state="enabled")
                    command = self.calib.read_value()
                    self.master.after(0, self.set_value_label.config(text = self.responce))
                self.responce = round(self.calib.send_response(command)[1], 6)
                sleep(1)
        except Exception as e:
            print(123123)
            print(e)

    def to_set_value(self):
        self.to_set_value_btn_flag = True
        self.value_to_set = float(self.to_set_value_sb.get())


