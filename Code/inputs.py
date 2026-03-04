from load_settings import config
from device import Device
from calibrator import Calibrator

device = Device(**config.config["device"])
calibrator = Calibrator()
device.connect()
calibrator.connect()

parameter = config.get("PARAMETER")
two_pass = config.get("TWO_PASS")
negative_start = config.get("NEGATIVE_START")
negative_end = config.get("NEGATIVE_END")
negative_step = config.get("NEGATIVE_STEP")
positive_start = config.get("POSITIVE_START")
positive_end = config.get("POSITIVE_END")
positive_step = config.get("POSITIVE_STEP")

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

if parameter == "current":
    i = None
    set_value = calibrator.command_46()
    read_value = calibrator.command_49()
elif:
    set_value = calibrator.command_47(i)
    read_value = calibrator.command_50()
elif:
    set_value = calibrator.command_48(i)
    read_value = calibrator.command_51()
else:
    print("no command")

points = negative_start, negative_end, negative_step
while True:
    for i in float_range(*points):
        print(f"Установка... {i}")
        calibrator.send_response(set_value)
        while True:
            current_value = calibrator.send_response(read_value)
            if abs(current_value - i) <= 0.0001:
                break
        print(f"Установлено: {current_value}")
        print(f"Запрос измерений...")
        device.send()
        device_resp = device.recieve()
        print(f"Измерения: {device_resp}")

    if not two_pass:
        break
    else:
        points = positive_start, positive_end, positive_step
        two_pass = False

calibrator.disconnect()
device.disconnect()

