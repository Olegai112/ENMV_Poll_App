from serial import Serial
from struct import pack, unpack
import socket, hid

class Device:
    client = None

    def __init__(self, **kwargs):
        self.protocol = kwargs.get("PROTOCOL")

        self.com = kwargs.get("RTU_COM")
        self.baudrate = int(kwargs.get("RTU_BAUDRATE"))
        self.rtu_timeout = kwargs.get("RTU_TIMEOUT")
        char_time = 11 / self.baudrate
        self.inter_char_timeout = char_time * 1.5

        self.ip = kwargs.get("TCP_IP")
        self.port = kwargs.get("TCP_PORT")
        self.tcp_timeout = kwargs.get("TCP_TIMEOUT")

        self.vid = kwargs.get("VID")
        self.pid = kwargs.get("PID")

        self.manually_send = kwargs.get("MANUALLY_SEND")
        self.slave_id = kwargs.get("SLAVE_ID")
        self.function = kwargs.get("FUNCTION")
        self.start_adress = kwargs.get("START_ADRESS")
        self.reg_count = kwargs.get("REG_COUNT")

        self.ao_mode = kwargs.get("AO_MODE")
        self.ao_range = kwargs.get("AO_RANGE")
        self.ao_coefficients = kwargs.get("AO_COEFFICIENTS")
        self.ao_esx_id = kwargs.get("AO_ESX_ID")

    def connect(self):
        if self.protocol == 'RTU':
            self.client = Serial(self.com, self.baudrate, timeout=self.rtu_timeout, inter_byte_timeout=self.inter_char_timeout)
            self.client.reset_input_buffer()
            self.client.reset_output_buffer()
        elif self.protocol == 'TCP':
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(self.tcp_timeout)
            self.client.connect((self.ip, self.port))
            # self.client = "TCP client"
            # print('Имитация подключения...')
            # print(self.ip, self.port)
        elif self.protocol == 'USB':
            self.client = hid.device()
            self.client.open(int(self.vid, 16), int(self.pid, 16))

    def send(self, request_data = None):

        if request_data == "ping":
            request_data = b'\x00\x03\x00\x00\x00\x00E\xca'


        elif not self.manually_send:
            if self.ao_mode == 'OFF':
                request_data = int(self.slave_id).to_bytes(1) + bytes.fromhex(self.function) + int(self.start_adress).to_bytes(2) + int(self.reg_count).to_bytes(2)
            elif self.ao_mode == 'ENMV':
                request_data = self.slave_id + b'e\xa73\x00\x03\x06' +  self.ao_range.to_bytes(1) + self.ao_coefficients.to_bytes(1) + pack('<f', request_data)
            elif self.ao_mode == 'ESX':
                request_data = self.ao_esx_id.to_bytes(1) + b'\x03\x04' + pack('>f', request_data) # !возможно ошибка с big-endian!

        if self.protocol == 'RTU':
            request = request_data + self.calculate_crc(request_data)
            self.client.write(request)
        elif self.protocol == 'TCP':
            request = bytes([0, 1, 0, 0]) + len(request_data).to_bytes(2) + request_data
            self.client.sendall(request)
            # print('Имитация отправки данных')
            # print(request.hex())
        elif self.protocol == 'USB':
            # _ = self.client.read(64, 100)
            no_header = request_data + self.calculate_crc(request_data)
            request = bytes([1, 0, len(no_header), 0]) + no_header
            hid_data = request.ljust(64, b'\x00')
            self.client.write(hid_data)
        return request

    def recieve(self):
        raw_values = None
        if self.protocol == 'RTU':
            response = self.client.read(1024)     # TODO подогнать параметры приема
            if len(response) >= 7:
                raw_values = response[3:len(response)-2]
        elif self.protocol == 'TCP':
            response = self.client.recv(1024)
            if len(response) >= 7:
                raw_values = response[9:]
            # response = bytes.fromhex('00 01 00 00 00 23 01 03 20 41 bc 00 00 42 37 33 33 42 ca 99 9a 42 82 66 66 42 f6 e6 66 44 29 9a 40 40 49 0f db 40 2d f8 93')
            # raw_values = response[9:]
        elif self.protocol == 'USB':
            packet1 = bytes(self.client.read(64, 1024)).rstrip(b'\x00')
            packet2 = bytes(self.client.read(64, 1024)).rstrip(b'\x00')
            response = packet1 + packet2
            if len(response) >= 7:
                raw_values = packet1[7:]+packet2[2:]
                raw_values = raw_values[:len(raw_values) - 2]
        return response, raw_values

    def disconnect(self):
        if self.protocol in ('RTU', 'USB'):
            self.client.close()
        else:
            self.client.close()
            # print("Имитация отключения...")

    @staticmethod
    def value_unpack_float(raw_values):
        values = {}
        for i in range(0, len(raw_values), 4):
            bytes_value = raw_values[i:i + 4]
            byte_swap =  bytes([bytes_value[1]] + [bytes_value[0]] + [bytes_value[3]] + [bytes_value[2]]) # bytes_value
            unpack_value = unpack('<f', byte_swap)[0]
            values[f'Chanel_{len(values)+1}'] = unpack_value
        return values


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


