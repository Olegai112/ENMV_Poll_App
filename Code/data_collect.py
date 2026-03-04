import csv, os
from datetime import datetime


def save_data(calib, channels):
    if type(channels) != type(list()):
        channels = list([channels])
    # Проверяем, существует ли файл
    file_exists = os.path.isfile('data.csv')

    with open('data.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        # Если файл новый - пишем заголовки
        if not file_exists:
            headers = ['Timestamp'] + ['Value'] + [f'Channel_{i + 1}' for i in range(len(channels))]
            writer.writerow(headers)
            print("Создан новый файл с заголовками")

        # Всегда пишем данные
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = [timestamp] + [calib] + channels
        writer.writerow(data)

    print(f"✅ Данные записаны: {data[0]}")