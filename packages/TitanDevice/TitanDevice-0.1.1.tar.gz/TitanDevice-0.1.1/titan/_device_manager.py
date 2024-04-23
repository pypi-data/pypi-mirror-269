from adbutils import adb

from titan._device_exception import DeviceNoFoundException


class _DeviceManager(object):
    def __init__(self, device_serial: str):
        if device_serial not in [device.serial for device in adb.device_list()]:
            raise DeviceNoFoundException(device_serial)
        self._device = adb.device(device_serial)

    @staticmethod
    def get_all_devices():
        return [device.info for device in adb.device_list()]
