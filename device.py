from serial import Serial
import socket, hid

class Device:
    def __init__(self, **kwargs):
        self.protocol = kwargs.get("PROTOCOL")

        self.com = kwargs.get("RTU_COM")
        self.baudrate = kwargs.get("RTU_BAUDRATE")
        self.rtu_timeout = kwargs.get("RTU_TIMEOUT")
        char_time = 11 / self.baudrate
        self.inter_char_timeout = char_time * 1.5

        self.ip = kwargs.get("TCP_IP")
        self.port = kwargs.get("TCP_PORT")
        self.tcp_timeout = kwargs.get("TCP_TIMEOUT")

        self.vid = kwargs.get("VID")
        self.pid = kwargs.get("PID")

        self.slave_id = kwargs.get("SLAVE_ID").to_bytes(1)
        self.function = int(kwargs.get("FUNCTION")).to_bytes(1)
        self.start_adress = kwargs.get("START_ADRESS").to_bytes(2)
        self.reg_count = kwargs.get("REG_COUNT").to_bytes(2)

        self.client = None

    def connect(self):
        if self.protocol == 'RTU':
            self.client = Serial(self.com, self.baudrate, timeout=self.rtu_timeout, inter_byte_timeout=self.inter_char_timeout)
            self.client.reset_input_buffer()
            self.client.reset_output_buffer()
        elif self.protocol == 'TCP':
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(self.tcp_timeout)
            self.client.connect((self.ip, self.port))
        elif self.protocol == 'USB':
            self.client = hid.device()
            self.client.open(int(self.vid, 16), int(self.pid, 16))

    def send(self):
        request_bytes = self.slave_id + self.function + self.start_adress + self.reg_count

        if self.protocol == 'RTU':
            request = request_bytes + self.calculate_crc(request_bytes)
            self.client.write(request)
        elif self.protocol == 'TCP':
            request = bytes([0, 1, 0, 0]) + len(request_bytes).to_bytes(2) + request_bytes
            self.client.sendall(request)
        elif self.protocol == 'USB':
            # _ = self.client.read(64, 100)
            no_header = request_bytes + self.calculate_crc(request_bytes)
            request = bytes([1, 0, len(no_header), 0]) + no_header
            hid_data = request.ljust(64, b'\x00')
            print(hid_data.hex())
            self.client.write(hid_data)

    def recieve(self):
        if self.protocol == 'RTU':
            response = self.client.read(69)     # TODO подогнать параметры приема
        elif self.protocol == 'TCP':
            response = self.client.recv(1024)
        elif self.protocol == 'USB':
            response = bytes(self.client.read(64, 1000))    # TODO принимать два пакета USB
        return response

    def disconnect(self):
        if self.protocol in ('RTU','TCP', 'USB'):
            self.client.close()

    @staticmethod
    def calculate_crc(data):
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc.to_bytes(2, 'little')


