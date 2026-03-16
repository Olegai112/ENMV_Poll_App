import tkinter as tk
from http.client import responses
from tkinter import ttk

from src.services.load_settings import Settings


class DevicePoll():
    def __init__(self, master, connection):
        self.connection = connection
        self.device = None

        self.master = master

        self.selected_send_mode = tk.BooleanVar(value=False)

        self.add_command_frame()

    def add_command_frame(self):
        self.command_frame = tk.Frame(self.master) # первый
        self.command_frame.pack(fill="x", expand=True)

        self.command_label = ttk.Label(self.command_frame, text="Modbus command")
        self.command_entry = ttk.Entry(self.command_frame)
        self.command_rbtn = ttk.Radiobutton(self.command_frame, variable=self.selected_send_mode, value=True, command=self.radiobuttons)

        self.command_label.pack(side="left",)
        self.command_entry.pack(side="left", expand=True,fill="x")
        self.command_rbtn.pack(side="left")


        self.command_const_frame = tk.Frame(self.master) # второй
        self.command_const_frame.pack(fill="x", expand=True)

        self.slave_id_label = ttk.Label(self.command_const_frame, text="Slave ID")
        self.slave_id_entry = ttk.Entry(self.command_const_frame, width=4)
        self.slave_id_entry.insert(0, Settings.get("device")["SLAVE_ID"])
        self.fuction_label = ttk.Label(self.command_const_frame, text="Fuction")
        self.fuction_entry = ttk.Entry(self.command_const_frame, width=4)
        self.fuction_entry.insert(0, Settings.get("device")["FUNCTION"])
        self.start_addr_label = ttk.Label(self.command_const_frame, text="Address")
        self.start_addr_entry = ttk.Entry(self.command_const_frame, width=4)
        self.start_addr_entry.insert(0, Settings.get("device")["START_ADRESS"])
        self.reg_count_label = ttk.Label(self.command_const_frame, text="Quantity")
        self.reg_count_entry = ttk.Entry(self.command_const_frame, width=4)
        self.reg_count_entry.insert(0, Settings.get("device")["REG_COUNT"])
        self.command_const_rbtn = ttk.Radiobutton(self.command_const_frame, variable=self.selected_send_mode, value=False, command=self.radiobuttons)


        self.slave_id_label.pack(side="left", expand=True)
        self.slave_id_entry.pack(side="left", expand=True)
        self.fuction_label.pack(side="left", expand=True)
        self.fuction_entry.pack(side="left", expand=True)
        self.start_addr_label.pack(side="left", expand=True)
        self.start_addr_entry.pack(side="left", expand=True)
        self.reg_count_label.pack(side="left", expand=True)
        self.reg_count_entry.pack(side="left", expand=True)
        self.command_const_rbtn.pack(side="left")


        self.send_frame = tk.Frame(self.master) # третий
        self.send_frame.pack(fill="x", expand=True)

        self.delay_chbtn = ttk.Checkbutton(self.send_frame)
        self.delay_label = ttk.Label(self.send_frame, text="Delay")
        self.delay_entry = ttk.Entry(self.send_frame, width=4)
        self.points_chbtn = ttk.Checkbutton(self.send_frame)
        self.points_label = ttk.Label(self.send_frame, text="Points")
        self.points_entry = ttk.Entry(self.send_frame, width=4)
        self.send_btn = ttk.Button(self.send_frame, command = self.modbus_request_mode, text="--->")

        self.delay_chbtn.pack(side="left")
        self.delay_label.pack(side="left")
        self.delay_entry.pack(side="left")
        self.points_chbtn.pack(side="left")
        self.points_label.pack(side="left")
        self.points_entry.pack(side="left")
        self.send_btn.pack(side="right")

        self.radiobuttons()

    def modbus_request_mode(self):
        self.device = self.connection.get_device()

        selected = self.selected_send_mode.get()
        Settings.push("device", "MANUALLY_SEND", changed_setting=selected)
        self.device.manually_send = Settings.get("device")["MANUALLY_SEND"]

        if selected:
            self.device.send(bytes.fromhex(self.command_entry.get()))
        else:
            self.send_modbus_request()

        # resp = self.device.value_unpack_float(self.device.recieve()[1])
        # for i in resp.keys():
        #     print(i, resp[i])
        print(self.device.recieve()[1].hex())


    def send_modbus_request(self):
        Settings.push("device", "SLAVE_ID", changed_setting=self.slave_id_entry.get())
        Settings.push("device", "FUNCTION", changed_setting=self.fuction_entry.get())
        Settings.push("device", "START_ADRESS", changed_setting=self.start_addr_entry.get())
        Settings.push("device", "REG_COUNT", changed_setting=self.reg_count_entry.get())

        self.device.slave_id = self.slave_id_entry.get()
        self.device.function = self.fuction_entry.get()
        self.device.start_adress = self.start_addr_entry.get()
        self.device.reg_count = self.reg_count_entry.get()

        self.device.send()

    def radiobuttons(self):
        if self.selected_send_mode.get():
            self.command_entry.config(state="enabled")
            for widget in self.command_const_frame.winfo_children():
                if not widget == self.command_const_rbtn:
                    widget.config(state="disabled")
        else:
            self.command_entry.config(state="disabled")
            for widget in self.command_const_frame.winfo_children():
                if not widget == self.command_const_rbtn:
                    widget.config(state="enabled")




