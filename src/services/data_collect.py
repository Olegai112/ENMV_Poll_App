import csv
from src.services.load_settings import config
from pathlib import Path
from datetime import datetime


class DataCollector:
    def __init__(self):
        self.path = config.get("PATH")
        self.filename = config.get("FILENAME")
        if  self.filename == "":
            self.filename = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    def write_data(self, data):
        if not Path(self.path + self.filename + '.csv').exists():
            with open(self.path + self.filename + '.csv', 'w', newline='', encoding='utf-8') as file:
                fieldnames = ["Time"] + list(data.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({**{"Time":datetime.now().strftime("%H:%M:%S")}, **data})
        else:
            # TODO проверка заголовков
            with open(self.path + self.filename + '.csv', 'a', newline='', encoding='utf-8') as file:
                fieldnames = ["Time"] + list(data.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow({**{"Time":datetime.now().strftime("%H:%M:%S")}, **data})

writer = DataCollector()







