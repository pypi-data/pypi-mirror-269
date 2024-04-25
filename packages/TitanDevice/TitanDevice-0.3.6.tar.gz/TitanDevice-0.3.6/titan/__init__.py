from titan._device_exception import *
from titan._device_manager import _DeviceManager
from titan._device_models import DeviceInfo, FridaInfo, PackageInfo, RunningAppInfo

device_manager_list: list[_DeviceManager] = _DeviceManager.get_all_device_manager_list()


def get_all_devices() -> list[DeviceInfo]:
    global device_manager_list
    device_manager_list = _DeviceManager.get_all_device_manager_list()
    return [device.get_device_info() for device in device_manager_list]


def get_frida_info(
        device_serial: str,
        frida_server_name='frida-server',
        frida_server_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.get_frida_info(frida_server_path, frida_server_name)
    raise DeviceNoFoundException(device_serial)


def install_frida(
        device_serial: str, frida_server_path: str,
        dist_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.install_frida(frida_server_path, dist_path)
    raise DeviceNoFoundException(device_serial)


def start_frida(
        device_serial: str, frida_server_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.start_frida(frida_server_path)
    raise DeviceNoFoundException(device_serial)


def stop_frida(
        device_serial: str, frida_server_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.stop_frida(frida_server_path)
    raise DeviceNoFoundException(device_serial)


def uninstall_frida(
        device_serial: str, frida_server_path='/data/local/tmp/frida-server'
) -> FridaInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.uninstall_frida(frida_server_path)
    raise DeviceNoFoundException(device_serial)


def get_installed_packages(device_serial: str) -> list[str]:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.get_installed_packages()
    raise DeviceNoFoundException(device_serial)


def get_package_info(device_serial: str, package_name: str) -> PackageInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.get_package_info(package_name)
    raise DeviceNoFoundException(device_serial)


def install_package(
        device_serial: str, package_path: str, uninstall=False, no_launch=True
) -> PackageInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.install_package(package_path, uninstall, no_launch)
    raise DeviceNoFoundException(device_serial)


def uninstall_package(device_serial: str, package_name: str) -> list[str]:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.uninstall_package(package_name)
    raise DeviceNoFoundException(device_serial)


def get_current_app(device_serial: str) -> RunningAppInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.get_current_app()
    raise DeviceNoFoundException(device_serial)


def start_package(
        device_serial: str, package_name: str, activity=None
) -> RunningAppInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.start_package(package_name, activity)
    raise DeviceNoFoundException(device_serial)


def stop_package(device_serial: str, package_name: str) -> RunningAppInfo:
    for device in device_manager_list:
        if device.get_device_info().serial == device_serial:
            return device.stop_package(package_name)
    raise DeviceNoFoundException(device_serial)
