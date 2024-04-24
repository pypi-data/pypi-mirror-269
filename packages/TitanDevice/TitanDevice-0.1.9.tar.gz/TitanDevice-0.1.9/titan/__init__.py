from titan._device_exception import DeviceNoFoundException
from titan._device_manager import _DeviceManager
from titan._device_models import DeviceInfo, FridaInfo

device_manager_list: list[_DeviceManager] = _DeviceManager.get_all_device_manager_list()


def get_all_devices() -> list[DeviceInfo]:
    global device_manager_list
    device_manager_list = _DeviceManager.get_all_device_manager_list()
    return [device.get_info() for device in device_manager_list]


def get_frida_info(device_serial: str) -> FridaInfo:
    for device in device_manager_list:
        if device.get_info().serial == device_serial:
            return device.get_frida_info()
    raise DeviceNoFoundException(device_serial)
