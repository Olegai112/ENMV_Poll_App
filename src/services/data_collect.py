import csv
from src.services.load_settings import config
from pathlib import Path
from datetime import datetime


class DataCollector:
    def __init__(self):
        self.path = Path(__file__).parents[2] / 'data'
        self.filename = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '_' + config.get("FILENAME") + '.csv'

    def write_data(self, data):
        if not Path(self.path / self.filename).exists():
            with open(self.path / self.filename, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ["Time"] + list(data.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({**{"Time":datetime.now().strftime("%H:%M:%S")}, **data})
        else:
            # TODO проверка заголовков
            with open(self.path / self.filename, 'a', newline='', encoding='utf-8') as file:
                fieldnames = ["Time"] + list(data.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow({**{"Time":datetime.now().strftime("%H:%M:%S")}, **data})







