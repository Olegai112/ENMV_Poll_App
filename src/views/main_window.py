import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('app')
root.geometry("800x600+70+200")
root.minsize(200,150)
root.maxsize(800,600)


def entered(event):
    btn.config(text="entered")

def left(event):
    btn.config(text="left")


btn = ttk.Button()
btn.place(height=100, width=200, x = 200, y = 200)

btn.bind("<Enter>", entered)
btn.bind("<Leave>", left)




root.mainloop()