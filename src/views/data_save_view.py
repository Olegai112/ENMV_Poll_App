import tkinter as tk
from tkinter import  ttk
from tkinter.messagebox import showinfo

from src.services.load_settings import Settings


class DataSave:
    def __init__(self, master, device_poll, precision_research = None):
        self.master = master
        self.device_poll = device_poll
        self.precision_research = precision_research

        self.add_main_frame()

    def add_main_frame(self):
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill="both")

        self.file_name_label = ttk.Label(self.main_frame, text="Имя файла:")
        self.file_name_label.pack()

        self.file_name_entry = ttk.Entry(self.main_frame, justify="center")
        self.file_name_entry.insert(0, Settings.get("FILENAME"))
        self.file_name_entry.pack()

        self.save_device_poll_flag_chbtn_var = tk.BooleanVar(value=Settings.get("SAVE_MODBUS_POLL_FLAG"))
        self.save_device_poll_flag_chbtn = ttk.Checkbutton(self.main_frame, text="Сохранять Modbus-опрос", variable=self.save_device_poll_flag_chbtn_var)
        self.save_device_poll_flag_chbtn.pack()

        self.save_button = ttk.Button(self.main_frame, text="Сохранить", command=self.save_settings)
        self.save_button.pack()

    def save_settings(self):
        print("\nСохранено:")

        self.file_name_to_save = self.file_name_entry.get()
        if Settings.get("FILENAME") != self.file_name_to_save:
            Settings.push("FILENAME", changed_setting=self.file_name_to_save)
            print(f"Имя файла: {self.file_name_to_save}")

        self.save_device_poll_flag_to_save = self.save_device_poll_flag_chbtn_var.get()
        if Settings.get("SAVE_MODBUS_POLL_FLAG") != self.save_device_poll_flag_to_save:
            Settings.push("SAVE_MODBUS_POLL_FLAG", changed_setting=self.save_device_poll_flag_to_save)
            print(f"Сохранять Modbus-опрос: {self.save_device_poll_flag_to_save}")



