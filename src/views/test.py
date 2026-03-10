import tkinter as tk
from tkinter import ttk


class Connection():
    def __init__(self, master):
        self.master = master
        
        # Создаем Notebook (он займет всю доступную площадь)
        self.protocol_tabs = ttk.Notebook(self.master)
        self.protocol_tabs.pack(expand=True, fill='both')
        
        # Создаем фреймы для каждой вкладки
        self.rtu_tab = ttk.Frame(self.protocol_tabs)
        self.tcp_tab = ttk.Frame(self.protocol_tabs)
        self.usb_tab = ttk.Frame(self.protocol_tabs)
        
        # Добавляем содержимое в каждую вкладку
        self._create_rtu_content()
        self._create_tcp_content()
        self._create_usb_content()
        
        # Добавляем вкладки в Notebook
        self.protocol_tabs.add(self.rtu_tab, text="RTU")
        self.protocol_tabs.add(self.tcp_tab, text="TCP")
        self.protocol_tabs.add(self.usb_tab, text="USB")
    
    def _create_rtu_content(self):
        """Содержимое для RTU вкладки"""
        # Создаем рамку для параметров
        params_frame = ttk.LabelFrame(self.rtu_tab, text="Параметры RTU")
        params_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Параметры
        ttk.Label(params_frame, text="Порт:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        port_combo = ttk.Combobox(params_frame, values=["COM1", "COM2", "COM3", "COM4"])
        port_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(params_frame, text="Скорость:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        baud_combo = ttk.Combobox(params_frame, values=["9600", "19200", "38400", "115200"])
        baud_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопка подключения
        ttk.Button(self.rtu_tab, text="Подключиться RTU").pack(pady=10)
    
    def _create_tcp_content(self):
        """Содержимое для TCP вкладки"""
        params_frame = ttk.LabelFrame(self.tcp_tab, text="Параметры TCP/IP")
        params_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        ttk.Label(params_frame, text="IP адрес:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ip_entry = ttk.Entry(params_frame)
        ip_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(params_frame, text="Порт:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        port_entry = ttk.Entry(params_frame)
        port_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.tcp_tab, text="Подключиться TCP").pack(pady=10)
    
    def _create_usb_content(self):
        """Содержимое для USB вкладки"""
        params_frame = ttk.LabelFrame(self.usb_tab, text="Параметры USB")
        params_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        ttk.Label(params_frame, text="USB устройство:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        device_combo = ttk.Combobox(params_frame, values=["USB0", "USB1", "USB2"])
        device_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(self.usb_tab, text="Подключиться USB").pack(pady=10)


# Использование в главном окне
class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Главное окно")
        
        # Разделяем окно на зоны с помощью grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=3)
        self.root.grid_rowconfigure(2, weight=2)
        
        # Левая верхняя зона - Connection
        connection_frame = ttk.Frame(self.root)
        connection_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.connection = Connection(connection_frame)
        
        # Остальные зоны...
        precision_frame = tk.Frame(self.root, bg="blue")
        precision_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        manual_frame = tk.Frame(self.root, bg="green")
        manual_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        
        graphs_frame = tk.Frame(self.root, bg="yellow")
        graphs_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        console_frame = tk.Frame(self.root, bg="gray")
        console_frame.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
        
        self.root.mainloop()
