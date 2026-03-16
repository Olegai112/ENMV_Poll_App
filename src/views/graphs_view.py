import tkinter as tk
from tkinter import ttk
import matplotlib

matplotlib.use('TkAgg')  # Указываем бэкенд для Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class Graphs:
    def __init__(self, parent):
        self.parent = parent

        # Создаем фигуру и оси
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Создаем холст для отображения графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Панель управления
        self.control_frame = ttk.Frame(parent)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(self.control_frame, text="Обновить",
                   command=self.update_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Очистить",
                   command=self.clear_graph).pack(side=tk.LEFT, padx=5)

        # Данные по умолчанию
        self.x_data = np.linspace(0, 10, 100)
        self.y_data = np.sin(self.x_data)
        self.plot()

    def plot(self):
        """Построение графика"""
        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, 'b-', linewidth=2, label='sin(x)')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('График синуса')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def update_graph(self):
        """Обновление графика"""
        # Генерируем новые данные
        self.y_data = np.cos(self.x_data)  # меняем на косинус
        self.plot()

    def clear_graph(self):
        """Очистка графика"""
        self.ax.clear()
        self.canvas.draw()

    def plot_data(self, x, y, title="График", xlabel="X", ylabel="Y"):
        """Построение произвольных данных"""
        self.ax.clear()
        self.ax.plot(x, y, 'r-', linewidth=2)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        self.ax.grid(True)
        self.canvas.draw()