import tkinter as tk


from src.views.connection_view import Connection
from src.views.calibrator_view import CalibView
from src.views.device_poll_view import DevicePoll
from src.views.console_view import Console
from src.views.graphs_view import Graphs



class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x600")

        self.frame_connection = tk.Frame(self.root, bg="red")
        self.connection = Connection(self.frame_connection)

        self.frame_device_poll = tk.Frame(self.root)
        self.device_poll = DevicePoll(self.frame_device_poll, self.connection)

        self.frame_calibrator = tk.Frame(self.root, bg="green")
        self.calibrator = CalibView(self.frame_calibrator)

        self.frame_precision_research = tk.Frame(self.root, bg="blue")
        #TODO

        self.frame_graphs = tk.Frame(self.root, bg="yellow")
        self.graphs = Graphs(self.frame_graphs)

        self.frame_console = tk.Frame(self.root, bg="gray")
        self.console = Console(self.frame_console)

        self.frame_connection.place(relheight=1/6, relwidth=1/3)
        self.frame_device_poll.place(rely=1/6, relheight=1/6, relwidth=1/3)
        self.frame_calibrator.place(rely=2/6, relheight=1/6, relwidth=1/3)
        self.frame_precision_research.place(rely=3/6, relheight=1/6, relwidth=1/3)
        self.frame_graphs.place(relx=1/3, relheight=4/6, relwidth=2/3)
        self.frame_console.place(relx=1/3, rely=4/6, relheight=2/6, relwidth=2/3)

        self.root.mainloop()