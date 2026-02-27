from serial import Serial

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
        return bytes(response)

    def disconnect(self):
        self.client.close()

    def command_select(self, choice):
        if choice == 40:
            command = [40, 0, 40, 40, 40, 40, 40]
        return command