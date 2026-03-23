from src.services.load_settings import Settings
import time


def precision_research(device, calibrator, writer):

    two_pass = Settings.get("TWO_PASS")
    negative_start = Settings.get("NEGATIVE_START") # TODO float
    negative_end = Settings.get("NEGATIVE_END")
    negative_step = Settings.get("NEGATIVE_STEP")
    positive_start = Settings.get("POSITIVE_START")
    positive_end = Settings.get("POSITIVE_END")
    positive_step = Settings.get("POSITIVE_STEP")
    num_of_points = Settings.get("NUM_OF_POINTS")
    delay = Settings.get("DELAY")
    parameter = Settings.get("PARAMETER")
    chanel_scope = Settings.get("CHANEL_SCOPE")

    units= {"current": "мА", "voltage": "В","resistance": "Ом"}


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


    points = positive_start, positive_end, positive_step

    if device.ao_mode != "OFF":
        print('Калибровка...')
        calibrator.send_response(calibrator.measure_value(1))
        for i in float_range(*points):
            print(f"Установка... {i} {units[parameter]}")
            device.send(i)
            print()
            counter = 0
            while counter != 5:
                current_value1 = calibrator.send_response(calibrator.measure_value())
                current_value2 = calibrator.send_response(calibrator.measure_value())
                print(f"{round(current_value2[1], 6)}...")
                counter +=1
                if abs(current_value2[1] - current_value1[1]) <= 0.00005:
                    break
            print(f"Установлено: {round(current_value2[1], 6)} {units[parameter]}")
            print(f"Запрос измерений...")

            next_time = time.perf_counter()

            for num_of_point in range(1, num_of_points+1):
                cur_time = time.perf_counter()
                if cur_time < next_time:
                    delay_correct = next_time - cur_time
                    time.sleep(delay_correct)

                cycle_end = time.perf_counter()
                cycle_duration = cycle_end - cur_time

                measured_value = calibrator.send_response(calibrator.measure_value())
                print(f"Точка №{num_of_point}: {measured_value[1]} {units[parameter]}, {cycle_duration * 1000:.1f} мс")
                writer.write_data(data = {"Reference": i, "Output_Value": measured_value[1]})

                next_time += delay


    else:
        while True:
            for i in float_range(*points):
                print(f"Установка... {float(i)} {units[parameter]}")
                calibrator.send_response(calibrator.set_value(i))
                while True:
                    current_value = calibrator.send_response(calibrator.read_value())
                    print(f"{round(current_value[1], 6)} {units[parameter]}...")
                    if abs(current_value[1] - i) <= 0.0001:
                        break
                print(f"Установлено: {round(current_value[1], 6)} {units[parameter]}")
                print(f"Запрос измерений...")

                next_time = time.perf_counter()

                for num_of_point in range(1, num_of_points+1):
                    cur_time = time.perf_counter()
                    if cur_time < next_time:
                        delay_correct = next_time - cur_time
                        time.sleep(delay_correct)

                    cycle_end = time.perf_counter()
                    cycle_duration = cycle_end - cur_time

                    device.send()
                    device_resp = device.recieve()
                    unpack_value = device.value_unpack_float(device_resp[1])

                    print(f"Точка №{num_of_point}: {unpack_value[list(unpack_value.keys())[chanel_scope-1]]} {units[parameter]}, {cycle_duration * 1000:.1f} мс")
                    writer.write_data(data = {**{"Calibrator":current_value[1]},**{list(unpack_value.keys())[chanel_scope-1]:unpack_value[list(unpack_value.keys())[chanel_scope-1]]}}) # **device.value_unpack_float(device_resp[1])

                    next_time += delay

            if not two_pass:
                break
            else:
                points = negative_start, negative_end, negative_step
                two_pass = False
                input("Меняй полярность!")

if __name__ == "__main__":
    precision_research()