from device import Device
from load_settings import config


device = Device(**config.config["device"])
device.connect()

request_bytes = bytes.fromhex("01 65 a733 0003 06 0100 0000 0000")
# 01 65 a733 0003 06 0200 0000 4040
device.send(request_bytes)

device_resp = device.recieve()
print(device_resp[6:].hex())
device.disconnect()