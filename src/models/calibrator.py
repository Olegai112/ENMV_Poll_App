from time import sleep

import threading
from serial import Serial
from struct import pack, unpack


class Calibrator:
    client = None
    def __init__(self, parameter=None):
        self.parameter = parameter

        self.connection_waiting_flag = False

    def connect(self):
        def connect_thread():
            while self.connection_waiting_flag:
                try:
                    client = Serial(port="COM3", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=3, write_timeout=3)
                    client.write(b'\xa6')
                    if client.read(1) == b'\xa6':
                        self.connection_waiting_flag = False
                        self.client = client
                        print("Калибратор подключен.")
                        break
                except:
                    print("Ожидание подключения калибратора...")
                    sleep(1)

        threading.Thread(target=lambda: connect_thread(), daemon=True).start()

    def disconnect(self):
        self.client.close()
        self.client = None
        print("Калибратор отключен.")

    def send_response(self, command_data):
        self.pause_between_requests = False
        self.client.reset_input_buffer()
        self.client.reset_output_buffer()
        response = bytearray()
        for i in range(len(command_data)):
            self.client.write(bytes([command_data[i]]))
            response_byte = self.client.read(1)
            if response_byte == b'':
                print("no resp")
                return b''
            else:
                response.extend(response_byte)
        if len(command_data) >= 6:
            checksum = sum(response[-2:-6:-1]) % 256 == response[-1]
            float_value = unpack('>f', bytes(response)[-2:-6:-1])[0]
            return bytes(response), float_value, checksum
        # else:
        #     return bytes(response)

    def set_value(self, value = 0):
        command_data = None
        value_bytes = list(pack('<f', value))
        if self.parameter == "current":
            command_data = [46] + value_bytes + [46]
        elif self.parameter == "voltage":
            command_data = [47] + value_bytes + [47]
        elif self.parameter == "resistance":
            command_data = [48] + value_bytes + [48]
        # print(command_data)
        return command_data

    def read_value(self):
        command_data = None
        if self.parameter == "current":
            command_data = [49]*6
        elif self.parameter == "voltage":
            command_data = [50]*6
        elif self.parameter == "resistance":
            command_data = [51]*6
        return command_data

    def measure_value(self, calibrate = 0):
        command_data = None
        if self.parameter == "current":
            command_data = [40] + [calibrate] + [40]*5
        elif self.parameter == "voltage":
            command_data = [41] + [calibrate] + [41]*5
        elif self.parameter == "resistance":
            command_data = [42] + [calibrate] + [42]*5
        return command_data



