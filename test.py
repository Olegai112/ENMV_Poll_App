import tkinter as tk
import subprocess
import sys
import os


class TerminalEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Терминал в tkinter")

        # Создаем текстовое поле для вывода
        self.output = tk.Text(root, wrap=tk.WORD, bg='black', fg='white',
                              font=('Courier', 10), height=20, width=80)
        self.output.pack(fill=tk.BOTH, expand=True)

        # Создаем поле для ввода команд
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.prompt = tk.Label(self.input_frame, text=">>> ", font=('Courier', 10))
        self.prompt.pack(side=tk.LEFT)

        self.input = tk.Entry(self.input_frame, font=('Courier', 10), bg='lightgray')
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input.bind('<Return>', self.execute_command)
        self.input.focus()

        # Приветственное сообщение
        self.print_output("Простой терминал на Python. Введите 'exit' для выхода.\n")
        self.print_output(f"Текущая директория: {os.getcwd()}\n")

    def print_output(self, text):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def execute_command(self, event):
        command = self.input.get()
        self.input.delete(0, tk.END)

        self.print_output(f">>> {command}\n")

        if command.lower() == 'exit':
            self.root.quit()
        elif command.lower() == 'clear':
            self.output.delete(1.0, tk.END)
        else:
            try:
                # Выполняем команду
                result = subprocess.run(command, shell=True, capture_output=True,
                                        text=True, cwd=os.getcwd())

                if result.stdout:
                    self.print_output(result.stdout)
                if result.stderr:
                    self.print_output(f"Ошибка: {result.stderr}")

            except Exception as e:
                self.print_output(f"Ошибка выполнения: {str(e)}\n")


