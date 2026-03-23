import tkinter as tk
from tkinter import  ttk
from src.services.load_settings import Settings


class DataSave:
    def __init__(self, master):
        self.master = master

        self.file_name_label = ttk.Label(self.master, text="Имя файла:")
        self.file_name_label.pack()
        self.file_name_entry = ttk.Entry(self.master)
        self.file_name_entry.pack()

        Settings.push("FILENAME", changed_setting=self.file_name_entry.get())

