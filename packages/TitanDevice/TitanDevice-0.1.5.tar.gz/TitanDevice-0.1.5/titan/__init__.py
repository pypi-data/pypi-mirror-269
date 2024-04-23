from typing import overload

from titan._device_manager import _DeviceManager
from titan._device_models import DeviceInfo, FridaInfo

device_manager_list: list[_DeviceManager] = _DeviceManager.get_all_device_manager_list()


def get_all_devices() -> list[DeviceInfo]:
    return [device.get_info() for device in device_manager_list]


@overload
def get_frida_info(device_serial: str) -> FridaInfo:
    return next(
        filter(
            lambda device: device.get_info().serial == device_serial,
            device_manager_list
        )
    ).get_frida_info()


@overload
def get_frida_info(device_manager: _DeviceManager) -> FridaInfo:
    return device_manager.get_frida_info()


def get_frida_info(device: [str | _DeviceManager]) -> FridaInfo:
    if isinstance(device, str):
        return get_frida_info(device)
    elif isinstance(device, _DeviceManager):
        return get_frida_info(device)
    else:
        raise TypeError(f"Unsupported type: {type(device)}")
