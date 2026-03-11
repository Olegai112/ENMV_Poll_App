import serial
import time

# Настройки порта
port = 'COM2'  # Замените на ваш порт
baudrate = 9600  # Скорость

try:
    # Открываем порт
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Прослушиваю порт {port}...")

    # Бесконечное чтение
    counter = 0
    while True:
        if ser.in_waiting > 0:  # Если есть данные
            data = ser.read()  # Читаем строку
            # if counter%5 == 0:
            #     print(1111111111111)
            print(int.from_bytes(data))
            counter +=1
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"Ошибка: {e}")
except KeyboardInterrupt:
    print("\nОстановлено пользователем")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Порт закрыт")