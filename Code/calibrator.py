from serial import Serial
from struct import pack

class Calibrator:
    def __init__(self, **kwargs):
        self.positive_start = kwargs.get("POSITIVE_START"),
        self.positive_end = kwargs.get("POSITIVE_END"),
        self.positive_step = kwargs.get("POSITIVE_STEP"),
        self.negative_start = kwargs.get("NEGATIVE_START"),
        self.negative_end = kwargs.get("NEGATIVE_END"),
        self.negative_step = kwargs.get("NEGATIVE_STEP")

    def connect(self):
        self.client = Serial(port="COM3", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=3)

    def send_response(self, command):
        self.client.reset_input_buffer()
        self.client.reset_output_buffer()
        response = bytearray()
        for i in range(len(command)):
            self.client.write(bytes([command[i]]))
            response.extend(self.client.read(1))
        checksum = sum(response[-2:-6:-1]) % 256 == response[-1]
        return bytes(response)

    def disconnect(self):
        self.client.close()

# КОМАНДЫ КАЛИБРАТОРА
    # Команды измерения физических величин
    @staticmethod
    def command_40(calibrate = 0):
        # Команда №40 – Измерение силы тока (диапазон -22 … 22 мА)
        command = [40] + [calibrate] + [40]*5
        return command



    # Команды воспроизведения физических величин
    @ staticmethod
    def command_46(value = 0):
        # Команда №46 – Установка целевого значения для режима воспроизведения силы тока
        command = [46] + list(pack('<f', value)) + [46]
        return command

    @staticmethod
    def command_49():
        #  Команда №49 – Уточнение воспроизводимого значения силы тока
        command = [49]*6
        return command

    @staticmethod
    def command_49():
        #  Команда №49 – Уточнение воспроизводимого значения силы тока
        command = [49] * 6
        return command

