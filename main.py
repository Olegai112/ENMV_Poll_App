from load_settings import config
from device_init import Device
from calibrator import Calibrator

# device = Device(**config.config["device"])
# device.connect()

calibrator = Calibrator(**config.config["passage_values"])
calibrator.connect()

command = calibrator.command_select(40)
calib_resp = calibrator.send_response(command)
print(calib_resp.hex())


# device.send()
# device_resp = device.recieve()
# print(device_resp.hex())


# device.disconnect()

