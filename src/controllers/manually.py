from src.models.device import Device
from src.services.load_settings import config
from src.services.data_collect import writer


request_bytes = bytes.fromhex("01 03 0000 0010")
# 01 65 a733 0003 06 0200 0000 4040
device.send(request_bytes)

device_resp = device.recieve()

values = device.value_unpack_float(device_resp[1])
print(values)
writer.write_data(values)



device.disconnect()