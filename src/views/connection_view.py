import tkinter as tk
from tkinter import ttk

from src.services.load_settings import Settings
from src.models.device import Device


class Connection():
    def __init__(self, master):
        self.chosed_protocol = None
        self.device = None

        self.master = master
        ttk.Label(self.master, text=" Выберите протокол...", anchor="c").pack(fill="both", expand=True)

        self.protocol_buttons()
        self.config_frame = None
        self.add_status()

    def get_device(self):
        return self.device

    def connection_config(self, chosed_protocol):
        if  self.config_frame != None:
            self.config_frame.destroy()
        
        self.config_frame = tk.Frame(self.master, bg="green")
        self.config_frame.place(rely=1/4, relheight=2/4, relwidth=1)
        
        self.config_frame.columnconfigure(index=0, weight=1, uniform='col')
        self.config_frame.columnconfigure(index=1, weight=1, uniform='col')
        self.config_frame.rowconfigure(index=0, weight=1, uniform='row')
        self.config_frame.rowconfigure(index=1, weight=1, uniform='row')

        if self.chosed_protocol == self.rtu_btn:
            com_label = ttk.Label(self.config_frame, text="Порт:", anchor="c")
            baudrate_label = ttk.Label(self.config_frame, text="Cкорость передачи:", anchor="c")

            com_values = ["COM6", "COM7"]
            baudrate_values = ["19200", "115200"]

            self.com_combobox = ttk.Combobox(self.config_frame, textvariable=com_values, values=com_values, justify="center", state="readonly")
            self.baudrate_combobox = ttk.Combobox(self.config_frame, textvariable=baudrate_values, values=baudrate_values, justify="center", state="readonly")

            com_label.grid(row=0, column=0, sticky="nsew")
            baudrate_label.grid(row=1, column=0, sticky="nsew")
            self.com_combobox.grid(row=0, column=1, sticky="nsew")
            self.baudrate_combobox.grid(row=1, column=1, sticky="nsew")

        elif self.chosed_protocol == self.tcp_btn:
            ip_label = ttk.Label(self.config_frame, text="IP адрес:", anchor="c")
            port_label = ttk.Label(self.config_frame, text="Порт:", anchor="c")
            self.ip_entry = ttk.Entry(self.config_frame, justify="center")
            self.ip_entry.insert(0, "172.17.1.128")
            self.port_entry = ttk.Entry(self.config_frame, justify="center")
            self.port_entry.insert(0, 502)

            ip_label.grid(row=0, column=0, sticky="nsew")
            port_label.grid(row=1, column=0, sticky="nsew")
            self.ip_entry.grid(row=0, column=1, sticky="nsew")
            self.port_entry.grid(row=1, column=1, sticky="nsew")

        elif self.chosed_protocol == self.usb_btn:
            vid_label = ttk.Label(self.config_frame, text="VID:", anchor="c")
            pid_label = ttk.Label(self.config_frame, text="PID:", anchor="c")
            self.vid_entry = ttk.Entry(self.config_frame, justify="center")
            self.pid_entry = ttk.Entry(self.config_frame, justify="center")

            vid_label.grid(row=0, column=0, sticky="nsew")
            pid_label.grid(row=1, column=0, sticky="nsew")
            self.vid_entry.grid(row=0, column=1, sticky="nsew")
            self.pid_entry.grid(row=1, column=1, sticky="nsew")

    def protocol_buttons(self):
        self.protocol_frame = tk.Frame(self.master, bg="yellow")
        self.protocol_frame.place(relheight=1/4, relwidth=1)

        self.rtu_btn = ttk.Button(self.protocol_frame, text="RTU")
        self.tcp_btn = ttk.Button(self.protocol_frame, text="TCP")
        self.usb_btn = ttk.Button(self.protocol_frame, text="USB")

        self.previous_chosed_protocol = None

        def config_frame_var(event):
            self.connect_btn.config(state="enabled")
            self.chosed_protocol = event.widget
            if self.chosed_protocol == self.previous_chosed_protocol:
                return
            self.chosed_protocol["state"] = "disabled"

            if self.previous_chosed_protocol != None:
                self.previous_chosed_protocol["state"] = "enabled"

            self.previous_chosed_protocol = self.chosed_protocol

            self.connection_config(self.chosed_protocol)
            
        self.rtu_btn.bind('<ButtonPress-1>', config_frame_var)
        self.tcp_btn.bind('<ButtonPress-1>', config_frame_var)
        self.usb_btn.bind('<ButtonPress-1>', config_frame_var)

        self.rtu_btn.pack(side="left", fill="both", expand=True)
        self.tcp_btn.pack(side="left", fill="both", expand=True)
        self.usb_btn.pack(side="left", fill="both", expand=True)

    def add_status(self):
        self.status_frame = tk.Frame(self.master, bg="black")
        self.status_frame.place(rely=3 / 4, relheight=1 / 4, relwidth=1)
        self.status_label = ttk.Label(self.status_frame, text="Отключено", foreground="red", background="#FFCDD2", anchor="c")

        def connect():
            if self.chosed_protocol == self.rtu_btn:
                Settings.push("device", "PROTOCOL", changed_setting = self.rtu_btn["text"])
                Settings.push("device", "RTU_COM", changed_setting = self.com_combobox.get())
                Settings.push("device", "RTU_BAUDRATE", changed_setting = self.baudrate_combobox.get())
            elif self.chosed_protocol == self.tcp_btn:
                Settings.push("device", "PROTOCOL", changed_setting = self.tcp_btn["text"])
                Settings.push("device", "TCP_IP", changed_setting = self.ip_entry.get())
                Settings.push("device", "TCP_PORT", changed_setting = int(self.port_entry.get()))
            elif self.chosed_protocol == self.usb_btn:
                Settings.push("device", "PROTOCOL", changed_setting = self.usb_btn["text"])
                Settings.push("device", "VID", changed_setting = self.vid_entry.get())
                Settings.push("device", "PID", changed_setting = self.pid_entry.get())

            self.device = Device(**Settings.config["device"])
            self.device.connect()

            self.device.send("ping")
            ping_responce = self.device.recieve()
            print(ping_responce[0])
            if ping_responce[0] != b'':
               self.status_label.config(text="Подключено", foreground="green", background="#90feb5")
               self.connect_btn.config(state="disabled")
               self.disconnect_btn.config(state="enabled")

        def disconnect():
            self.device.disconnect()
            self.status_label.config(text="Отключено", foreground="red", background="#FFCDD2")
            self.device = None
            self.connect_btn.config(state="enabled")
            self.disconnect_btn.config(state="disabled")


        self.connect_btn = ttk.Button(self.status_frame, text="Подключить", command=connect, state="disabled")
        self.disconnect_btn = ttk.Button(self.status_frame, text="Отключить", command=disconnect, state="disabled")

        self.status_label.pack(side="left", fill="both", expand=True)
        self.disconnect_btn.pack(side="left", fill="both", expand=True)
        self.connect_btn.pack(side="left", fill="both", expand=True)


