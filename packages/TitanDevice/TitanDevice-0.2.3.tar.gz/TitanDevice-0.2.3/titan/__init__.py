from titan._device_exception import *
from titan._device_manager import _DeviceManager
from titan._device_models import DeviceInfo, FridaInfo

device_manager_list: list[_DeviceManager] = _DeviceManager.get_all_device_manager_list()


def get_all_devices() -> list[DeviceInfo]:
    global device_manager_list
    device_manager_list = _DeviceManager.get_all_device_manager_list()
    return [device.get_info() for device in device_manager_list]


def get_frida_info(
        device_serial: str,
        frida_server_name='frida-server',
        frida_server_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_info().serial == device_serial:
            return device.get_frida_info(frida_server_path, frida_server_name)
    raise DeviceNoFoundException(device_serial)


def install_frida(
        device_serial: str, frida_server_path: str,
        dist_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_info().serial == device_serial:
            return device.install_frida(frida_server_path, dist_path)
    raise DeviceNoFoundException(device_serial)


def start_frida(
        device_serial: str, frida_server_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_info().serial == device_serial:
            return device.start_frida(frida_server_path)
    raise DeviceNoFoundException(device_serial)
