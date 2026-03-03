import time

from load_settings import config
from device import Device
from calibrator import Calibrator

device = Device(**config.config["device"])
calibrator = Calibrator()
device.connect()
# calibrator.connect()

parameter = config.get("PARAMETER")
two_pass = config.get("TWO_PASS")
negative_start = config.get("NEGATIVE_START") # TODO float
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
    i = 0
    set_value = calibrator.command_46(i)
    read_value = calibrator.command_49()
    measure_value = calibrator.command_40(1) # TODO калибровка
# elif parameter == "voltage":
#     set_value = calibrator.command_47(i)
#     read_value = calibrator.command_50()
#     measure_value = calibrator.command_40()
# elif parameter == "resistance":
#     set_value = calibrator.command_48(i)
#     read_value = calibrator.command_51()
#     measure_value = calibrator.command_40()
else:
    print("no command")

points = negative_start, negative_end, negative_step

print('Калибровка...')
# calibrator.send_response(measure_value)
for i in float_range(*points):
    print(f"Установка... {i}")
    device.send(i)
    while True:
        # current_value = calibrator.send_response(measure_value)
        # if abs(current_value - i) <= 0.0005:
        break
    print(f"Установлено: {i}")
    time.sleep(2)
    print(f"Запрос измерений...")
    # measured_value = calibrator.send_response(measure_value)
    # print(f"Измерения: {measured_value}")

# calibrator.disconnect()
device.disconnect()