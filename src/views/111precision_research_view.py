import tkinter as tk
import threading
from tkinter import ttk

from time import sleep

from src.services.load_settings import Settings
from src.controllers.precision_research import precision_research
from src.services.data_collect import DataCollector


class PrecisionResearch():
    def __init__(self, master, connection, calibrator, device_poll, root):
        self.master = master
        self.connection = connection
        self.calibrator = calibrator
        self.device_poll = device_poll
        self.root = root

        self.add_main_frame()

    def add_main_frame(self):
        self.header_frame = tk.Frame(self.master)  # header
        self.header_frame.pack(fill="x")

        self.hello_label = ttk.Label(self.header_frame, text="Исследование точности")

        self.ao_chbtn_var = tk.BooleanVar(value=False)
        self.ao_chbtn = ttk.Checkbutton(self.header_frame, text="AO:", variable=self.ao_chbtn_var, command=self.set_ao)
        self.ao_chbtn.pack(side="left")

        self.selected_ao_mode = tk.StringVar(value="ESX")

        self.esx_rbtn = ttk.Radiobutton(self.header_frame, variable=self.selected_ao_mode, value="ESX", state="disable", command=self.add_spec_options_widgets)
        self.esx_rbtn.pack(side="left")
        self.esx_label = ttk.Label(self.header_frame, text="ESX")
        self.esx_label.pack(side="left")

        self.enmv_rbtn = ttk.Radiobutton(self.header_frame, variable=self.selected_ao_mode, value="ENMV", state="disable", command=self.add_spec_options_widgets)
        self.enmv_rbtn.pack(side="left")
        self.enmv_label = ttk.Label(self.header_frame, text="ENMV")
        self.enmv_label.pack(side="left")

        self.calib_parameterers = {"I, мА": "current", "U, В": "voltage", "R, Ом": "resistance"}
        self.calib_parameter_combobox = ttk.Combobox(self.header_frame, values=list(self.calib_parameterers.keys()), justify="center", state="readonly", width=5)
        self.calib_parameter_combobox.set("I, мА")
        self.calib_parameter_combobox.pack(side="left", expand=True)

        self.two_pass_chbtn_var = tk.BooleanVar(value=False)
        self.two_pass_chbtn = ttk.Checkbutton(self.header_frame, text="Второй проход", variable=self.two_pass_chbtn_var, command=self.second_pass)
        self.two_pass_chbtn.pack(side="left", expand=True)

        self.channel_scope_psinbox = ttk.Spinbox(self.header_frame, from_=1, to=16, increment=1, justify="center", width=3)
        self.channel_scope_psinbox.set(1)
        self.channel_scope_psinbox.pack(side="right")
        self.channel_scope_label = ttk.Label(self.header_frame, text="Канал")
        self.channel_scope_label.pack(side="right")

        self.settings_frame = tk.Frame(self.master) # main
        self.settings_frame.pack(fill="both")

        self.settings_frame.columnconfigure(index=0, weight=1, uniform='col')
        self.settings_frame.columnconfigure(index=1, weight=1, uniform='col')
        self.settings_frame.columnconfigure(index=2, weight=1, uniform='col')
        self.settings_frame.columnconfigure(index=3, weight=1, uniform='col')
        self.settings_frame.rowconfigure(index=0, weight=1)
        self.settings_frame.rowconfigure(index=1, weight=1)
        self.settings_frame.rowconfigure(index=2, weight=1)

        self.start_value_label = ttk.Label(self.settings_frame, text="Начальная точка")
        self.end_value_label = ttk.Label(self.settings_frame, text="Конечная точка")
        self.step_value_label = ttk.Label(self.settings_frame, text="Шаг")

        self.start_value_label.grid(column=0, row=0, sticky="nsew")
        self.end_value_label.grid(column=0, row=1, sticky="nsew")
        self.step_value_label.grid(column=0, row=2, sticky="nsew")

        self.start_value_spibox = ttk.Spinbox(self.settings_frame, from_=-100, to=100.0, increment=1, justify="center", width=8)
        self.end_value_spibox = ttk.Spinbox(self.settings_frame, from_=-100, to=100.0, increment=1, justify="center", width=8)
        self.step_value_spibox = ttk.Spinbox(self.settings_frame, from_=0.000001, to=100.0, increment=1, justify="center", width=8)

        self.start_value_spibox.set(Settings.get("POSITIVE_START"))
        self.end_value_spibox.set(Settings.get("POSITIVE_END"))
        self.step_value_spibox.set(Settings.get("POSITIVE_STEP"))

        self.start_value_spibox.grid(column=1, row=0)
        self.end_value_spibox.grid(column=1, row=1)
        self.step_value_spibox.grid(column=1, row=2)

        self.second_pass_start_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8, state="disable")
        self.second_pass_end_value_spibox = ttk.Spinbox(self.settings_frame, from_=0, to=100.0, increment=1, justify="center", width=8, state="disable")
        self.second_pass_step_value_spibox = ttk.Spinbox(self.settings_frame, from_=0.000001, to=100.0, increment=1, justify="center", width=8, state="disable")

        self.second_pass_start_value_spibox.set(Settings.get("NEGATIVE_START"))
        self.second_pass_end_value_spibox.set(Settings.get("NEGATIVE_END"))
        self.second_pass_step_value_spibox.set(Settings.get("NEGATIVE_STEP"))

        self.second_pass_start_value_spibox.grid(column=2, row=0)
        self.second_pass_end_value_spibox.grid(column=2, row=1)
        self.second_pass_step_value_spibox.grid(column=2, row=2)

        self.spec_options_frame = tk.Frame(self.settings_frame)
        self.spec_options_frame.grid(column=3, row=0, rowspan=3, sticky="nsew")
        self.add_spec_options_widgets()
        for widget in self.spec_options_frame.winfo_children():
            widget.config(state="disabled")

        self.spec_options_frame.columnconfigure(index=0, weight=1)
        self.spec_options_frame.columnconfigure(index=1, weight=1)
        self.spec_options_frame.columnconfigure(index=2, weight=1)
        self.spec_options_frame.rowconfigure(index=0, weight=1)
        self.spec_options_frame.rowconfigure(index=1, weight=1)

        self.footer_frame = tk.Frame(self.master) # footer
        self.footer_frame.pack(fill="x")

        self.start_btn = ttk.Button(self.footer_frame, text="Пуск", command=self.precision_research_start_thread)
        self.start_btn.pack(side="right")

        self.calib_disc_event = threading.Event()
        self.stop_btn = ttk.Button(self.footer_frame, text="Стоп", command=lambda: self.calibrator.connect_to_calib_thread(precision_research_flag=False, calib_disc_event = self.calib_disc_event))
        self.stop_btn.pack(side="right")

        self.progressbar_var = tk.IntVar(value=0)
        self.progressbar = ttk.Progressbar(self.footer_frame, orient="horizontal", variable=self.progressbar_var)
        self.progressbar.pack(expand=True, fill="x")

    def change_progress_bar_var(self, step = None, progress_bar_maximum = None):
        if progress_bar_maximum != None:
            self.progressbar.config(maximum=progress_bar_maximum+step)
        else:
            self.progressbar_var.set(self.progressbar_var.get()+step)

    def precision_research_start_thread(self):
        self.precision_research_thread = threading.Thread(target=self.precision_research_start, daemon=True)
        self.start_btn.config(state="disabled")
        self.precision_research_thread.start()

    def precision_research_start(self):
        self.device_connect_status = None
        try:
            self.save_settings()
            self.device_poll.save_poll_settings()

            self.writer = DataCollector()

            self.device = self.connection.get_device()
            if self.device != None:
                self.connection.disconnect()

            self.device_connect_status = self.connection.connect()

            if not self.device_connect_status:
                self.connection.disconnect_btn.config(state="enabled")
                self.connection.connect_btn.config(state="disabled")
                self.return_state()
                return
            self.connection.config_frame_var()
            self.device = self.connection.get_device()
            self.connection.connect_btn.config(state="disabled")
            self.connection.disconnect_btn.config(state="disabled")
            self.device_poll.send_btn.config(state="disabled")

            self.calib = self.calibrator.get_calib()
            self.calibrator.calib_status_chbtn.config(state="disabled")
            if not self.calib.client:
                self.calibrator.connect_to_calib_thread(precision_research_flag=True, callback = self.precision_research_callback, return_state = self.return_state)
            else:
                self.calibrator.connect_to_calib_thread(precision_research_flag=False, calib_disc_event = self.calib_disc_event)
                self.calib_disc_event.wait()
                self.calibrator.connect_to_calib_thread(precision_research_flag=True, callback=self.precision_research_callback, return_state=self.return_state)
        except Exception as e:
            print(f"pre res{e}")
            self.device_connect_status = False
            self.return_state()
            return

    def precision_research_callback(self):
        self.calib.parameter = self.calib_parameterers[self.calib_parameter_combobox.get()]
        # try:
        precision_research(self.device, self.calib, self.writer, self.change_progress_bar_var, self.change_polarity)
        # except Exception as e:
        #     print(11111111111)
        self.calibrator.connect_to_calib_thread(precision_research_flag=False, calib_disc_event = self.calib_disc_event)
        sleep(0.2)
        self.return_state()

    def change_polarity(self):
        tk.messagebox.showinfo(message="Меняй полярность!")

    def return_state(self, device_disconnect_flag = None):
        Settings.push("device", "AO_MODE", changed_setting="OFF")
        self.master.after(0, lambda: self.start_btn.config(state="enabled"))
        self.master.after(0, lambda: self.device_poll.send_btn.config(state="enabled"))
        self.master.after(0, lambda: self.calibrator.calib_status_chbtn.config(state="enabled"))
        if not self.device_connect_status:
            if device_disconnect_flag == None:
                self.master.after(0, lambda: self.connection.disconnect_btn.config(state="disabled"))
                self.master.after(0, lambda: self.connection.connect_btn.config(state="enabled"))
            else:
                self.master.after(0, lambda: self.connection.connect_btn.config(state="enabled"))
        else:
            self.master.after(0, lambda: self.connection.connect_btn.config(state="disabled"))
            self.master.after(0, lambda: self.connection.disconnect_btn.config(state="enabled"))
        self.progressbar_var.set(value=0)

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

        Settings.push("TWO_PASS", changed_setting=self.two_pass_chbtn_var.get())

        Settings.push("CHANEL_SCOPE", changed_setting=int(self.channel_scope_psinbox.get()))

        Settings.push("device", "MANUALLY_SEND", changed_setting=False)

        if self.ao_chbtn_var.get():
            Settings.push("device", "AO_MODE", changed_setting=self.selected_ao_mode.get())
            if self.selected_ao_mode.get() == "ESX":
                Settings.push("device", "AO_ESX_ID", changed_setting=int(self.esx_slave_id_spinbox.get()))
            else:
                Settings.push("device", "SLAVE_ID", changed_setting=int(self.enmv_slave_id_spinbox.get()))
                Settings.push("device", "AO_RANGE", changed_setting=self.ranges.index(self.enmv_range_combobox.get()))


    def set_ao(self):
        if self.ao_chbtn_var.get():
            self.esx_rbtn.config(state="enabled")
            self.enmv_rbtn.config(state="enabled")

            for widget in self.device_poll.command_const_frame.winfo_children():
                widget.config(state="disabled")
            for widget in self.device_poll.command_frame.winfo_children():
                widget.config(state="disabled")

            for widget in self.spec_options_frame.winfo_children():
                widget.config(state="enabled")

            self.two_pass_chbtn.config(state="disabled")
            self.channel_scope_psinbox.config(state="disabled")
        else:
            self.esx_rbtn.config(state="disabled")
            self.enmv_rbtn.config(state="disabled")

            for widget in self.device_poll.command_const_frame.winfo_children():
                widget.config(state="enabled")
            for widget in self.device_poll.command_frame.winfo_children():
                widget.config(state="enabled")
            self.device_poll.radiobuttons()

            for widget in self.spec_options_frame.winfo_children():
                widget.config(state="disabled")

            self.two_pass_chbtn.config(state="enabled")
            self.channel_scope_psinbox.config(state="enabled")

    def add_spec_options_widgets(self):
        for widget in self.spec_options_frame.winfo_children():
            widget.destroy()

        if self.selected_ao_mode.get() == "ESX":
            self.esx_slave_id_label = ttk.Label(self.spec_options_frame, text="Адрес опроса ESX:", anchor="center")
            self.esx_slave_id_label.grid(column=0, columnspan=2, row=0, sticky="nsew")

            self.esx_slave_id_spinbox = ttk.Spinbox(self.spec_options_frame, from_=0, to=255, increment=1, justify="center", width=4)
            self.esx_slave_id_spinbox.set(1)
            self.esx_slave_id_spinbox.grid(column=0, columnspan=2, row=1,rowspan=2)

        else:
            self.enmv_slave_id_label = ttk.Label(self.spec_options_frame, text="ЭНМВ ID:", anchor="center")
            self.enmv_slave_id_label.grid(column=0, row=0, sticky="nsew")
            self.enmv_slave_id_spinbox = ttk.Spinbox(self.spec_options_frame, from_=0, to=255, increment=1, justify="center", width=4)
            self.enmv_slave_id_spinbox.set(1)
            self.enmv_slave_id_spinbox.grid(column=1, row=0, sticky="nsew")
            self.enmv_range_label = ttk.Label(self.spec_options_frame, text="Диапазон:", anchor="center")
            self.enmv_range_label.grid(column=0, columnspan=2, row=1, sticky="nsew")
            self.ranges = ["-5...5 мА", "-20...20 мА", "-24...24 мА", "0...5 мА", "0...20 мА", "0...24 мА", "4...20 мА"]
            self.enmv_range_combobox = ttk.Combobox(self.spec_options_frame, values=self.ranges, justify="center", state="readonly")
            self.enmv_range_combobox.grid(column=0, columnspan=2, row=2, sticky="nsew")