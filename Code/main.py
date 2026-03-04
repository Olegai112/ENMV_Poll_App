from load_settings import config
from device import Device
from calibrator import Calibrator

device = Device(**config.get("device"))
# calibrator = Calibrator(config.get("PARAMETER"))


device.connect()
device.send()

device_resp = device.recieve()
print(device_resp[0].hex())

values = device.value_unpack_float(device_resp[1])
print(values)


# calibrator.connect()
# calib_resp = calibrator.send_response(calibrator.read_value())
# print(calib_resp[1])
#

# calibrator.disconnect()
device.disconnect()



