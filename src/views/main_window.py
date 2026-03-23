import tkinter as tk


from src.views.connection_view import Connection
from src.views.calibrator_view import CalibView
from src.views.device_poll_view import DevicePoll
from src.views.console_view import Console
# from src.views.graphs_view import Graphs
from src.views.precision_research_view import PrecisionResearch
from src.views.data_save_view import DataSave



class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x320")

        self.frame_connection = tk.Frame(self.root)
        self.connection = Connection(self.frame_connection)

        self.frame_device_poll = tk.Frame(self.root)
        self.device_poll = DevicePoll(self.frame_device_poll, self.connection)

        self.frame_calibrator = tk.Frame(self.root)
        self.calibrator = CalibView(self.frame_calibrator)

        self.frame_precision_research = tk.Frame(self.root)
        self.precision_research = PrecisionResearch(self.frame_precision_research, self.connection, self.calibrator, self.device_poll)

        self.frame_data_save = tk.Frame(self.root)
        self.data_save = DataSave(self.frame_data_save)

        # self.frame_graphs = tk.Frame(self.root, bg="yellow")
        # self.graphs = Graphs(self.frame_graphs)

        self.frame_console = tk.Frame(self.root)
        self.console = Console(self.frame_console)

        self.frame_connection.place(relheight=1/3, relwidth=1/3)
        self.frame_device_poll.place(rely=1/3, relheight=1/3, relwidth=1/3)
        self.frame_calibrator.place(rely=2/3, relheight=1/3, relwidth=1/3)
        self.frame_precision_research.place(relx=1/3, relheight=1/3, relwidth=5/12)
        self.frame_data_save.place(relx=9/12, relheight=1/3, relwidth=3/12)
        # self.frame_graphs.place(relx=1/3, relheight=4/6, relwidth=2/3)
        self.frame_console.place(relx=1/3, rely=1/3, relheight=2/3, relwidth=2/3)

        self.root.mainloop()