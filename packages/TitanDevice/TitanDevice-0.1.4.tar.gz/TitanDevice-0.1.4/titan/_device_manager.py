from adbutils import adb

from titan._device_exception import DeviceNoFoundException
from titan.device_models import DeviceInfo


class _DeviceManager(object):
    _device: adb.device
    _device_info: DeviceInfo = None

    def __init__(self, device_serial: str):
        if device_serial not in [device.serial for device in adb.device_list()]:
            raise DeviceNoFoundException(device_serial)
        self._device = adb.device(device_serial)

    def get_info(self) -> DeviceInfo:
        if self._device_info is None:
            self._device_info = DeviceInfo(
                serial=self._device.serial,
                product=self._device.prop.name,
                model=self._device.prop.model,
                device=self._device.prop.device
            )
        return self._device_info

    @staticmethod
    def get_all_devices():
        device_manager_list = [
            _DeviceManager(device.serial)
            for device in adb.device_list()
        ]
        return [device_manager.get_info() for device_manager in device_manager_list]
