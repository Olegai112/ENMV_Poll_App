import tkinter as tk
from tkinter import scrolledtext
import sys


class Console:
    def __init__(self, master):
        self.master = master

        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=('Courier', 11), bg='black', fg='white', state='normal')
        self.text_area.pack(expand=True, fill="both")

        # sys.stdout = self

    def write(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.text_area.update_idletasks()

    def flush(self):
        pass

    def clear(self):
        self.text_area.delete(1.0, tk.END)