from typing import overload

from titan._device_manager import _DeviceManager
from titan._device_models import DeviceInfo, FridaInfo

device_manager_list: list[_DeviceManager] = _DeviceManager.get_all_device_manager_list()


def get_all_devices() -> list[DeviceInfo]:
    return [device.get_info() for device in device_manager_list]


def get_frida_info(device_serial: str) -> FridaInfo:
    return next(
        filter(
            lambda device: device.get_info().serial == device_serial,
            device_manager_list
        )
    ).get_frida_info()
