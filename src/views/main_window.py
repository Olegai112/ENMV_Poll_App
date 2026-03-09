import tkinter as tk
from src.views.connection_view import Connection


class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x600")

        self.frame_connection = tk.Frame(self.root, bg="red")
        self.device = Connection(self.frame_connection).device

        self.frame_precision_research = tk.Frame(self.root, bg="blue")
        self.frame_manual = tk.Frame(self.root, bg="green")
        self.frame_graphs = tk.Frame(self.root, bg="yellow")
        self.frame_console = tk.Frame(self.root, bg="gray")

        self.frame_connection.place(relheight=1/6, relwidth=1/3)
        self.frame_precision_research.place(rely=1/6, relheight=3/6, relwidth=1/3)
        self.frame_manual.place(rely=4/6, relheight=2/6, relwidth=1/3)
        self.frame_graphs.place(relx=1/3, relheight=4/6, relwidth=2/3)
        self.frame_console.place(relx=1/3, rely=4/6, relheight=2/6, relwidth=2/3)

        self.root.mainloop()