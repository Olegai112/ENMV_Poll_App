from load_settings import config
from device import Device
from calibrator import Calibrator
from data_collect import save_data


device = Device(**config.config["device"])
calibrator = Calibrator(config.get("PARAMETER"))
device.connect()
calibrator.connect()

two_pass = config.get("TWO_PASS")
negative_start = config.get("NEGATIVE_START") # TODO float
negative_end = config.get("NEGATIVE_END")
negative_step = config.get("NEGATIVE_STEP")
positive_start = config.get("POSITIVE_START")
positive_end = config.get("POSITIVE_END")
positive_step = config.get("POSITIVE_STEP")
num_of_points = config.get("NUM_OF_POINTS")


def float_range(start, stop, step):
    if start <= stop:
        value = start
        while value <= stop:
            yield round(value, 6)
            value += step
    else:
        step = -step
        value = start
        while value >= stop:
            yield round(value, 6)
            value += step


points = negative_start, negative_end, negative_step

if device.ao_mode != "OFF" :

    print('Калибровка...')
    calibrator.send_response(calibrator.measure_value(1))
    for i in float_range(*points):
        print(f"Установка... {i}")
        device.send(i)
        counter = 0
        while counter != 5:
            current_value1 = calibrator.send_response(calibrator.measure_value())
            current_value2 = calibrator.send_response(calibrator.measure_value())
            print(f"{round(current_value2[1], 6)}...")
            counter +=1
            if abs(current_value2[1] - current_value1[1]) <= 0.00001:
                break
        print(f"Установлено: {round(current_value2[1], 6)}")
        print(f"Запрос измерений...")

        for num_of_point in range(1, num_of_points+1):
            measured_value = calibrator.send_response(calibrator.measure_value())
            print(f"Точка №{num_of_point}: {measured_value[1]}")
            save_data(i, measured_value[1])

    calibrator.disconnect()
    device.disconnect()
else:
    while True:
        for i in float_range(*points):
            print(f"Установка... {float(i)}")
            calibrator.send_response(calibrator.set_value(i))
            while True:
                current_value = calibrator.send_response(calibrator.read_value())
                print(f"{round(current_value[1], 6)}...")
                if abs(current_value[1] - i) <= 0.0001:
                    break
            print(f"Установлено: {round(current_value[1], 6)}")
            print(f"Запрос измерений...")
            for num_of_point in range(1, num_of_points+1):
                device.send()
                device_resp = device.recieve()
                print(f"Точка №{num_of_point}: {round(device.value_unpack_float(device_resp[1])[0], 6)}")
                save_data(current_value[1], device.value_unpack_float(device_resp[1])[0])

        if not two_pass:
            break
        else:
            points = positive_start, positive_end, positive_step
            two_pass = False
            input("Меняй полярность!")

    calibrator.disconnect()
    device.disconnect()