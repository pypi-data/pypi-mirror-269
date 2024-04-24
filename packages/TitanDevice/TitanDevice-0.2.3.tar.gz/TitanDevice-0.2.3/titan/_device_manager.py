import os.path
from typing import Optional

from adbutils import adb

from titan._device_exception import DeviceNoFoundException, DeviceMustBeRootedException, \
    FridaServerNotInstalled
from titan._device_models import DeviceInfo, FridaInfo


class _DeviceManager(object):
    _device: adb.device
    _serial: str
    _is_root: bool = False
    _device_info: Optional[DeviceInfo] = None
    _frida_info: Optional[FridaInfo] = None

    @staticmethod
    def check_is_root(func):
        def wrapper(self, *args, **kwargs):
            if not self._is_root:
                raise DeviceMustBeRootedException(self._serial)
            return func(self, *args, **kwargs)

        return wrapper

    def __init__(self, device_serial: str):
        if device_serial not in [device.serial for device in adb.device_list()]:
            raise DeviceNoFoundException(device_serial)
        self._serial = device_serial
        self._device = adb.device(device_serial)
        self._is_root = self.__is_root()

    @staticmethod
    def get_all_device_manager_list() -> list["_DeviceManager"]:
        return [
            _DeviceManager(device.serial)
            for device in adb.device_list()
        ]

    def __is_frida_running(self, frida_server_name) -> bool:
        return self._device.shell(f"pgrep {frida_server_name}").strip() != ""

    def __is_frida_installed(self, frida_server_path) -> bool:
        return self.__file_exists(frida_server_path)

    def __get_frida_version(self, frida_server_path) -> str | None:
        if not self.__is_frida_installed(frida_server_path):
            return None
        return self._device.shell(
            f"su -c {frida_server_path} --version"
        ).strip()

    def __file_exists(self, path: str) -> bool:
        return 'No such file or directory' not in self._device.shell(
            f"ls {path}"
        ).strip()

    def __is_root(self):
        return self.__file_exists("/system/xbin/su") or self.__file_exists(
            "/system/bin/su"
        )

    def get_info(self) -> DeviceInfo:
        if self._device_info is None:
            self._device_info = DeviceInfo(
                serial=self._device.serial,
                product=self._device.prop.name,
                model=self._device.prop.model,
                device=self._device.prop.device,
                is_root=self._is_root,
            )
        return self._device_info

    @check_is_root
    def install_frida(self, file_path, dist_path):
        self._device.push(file_path, dist_path)
        self._device.shell(f"su -c chmod 755 {dist_path}")
        self._device.shell(f"su -c {dist_path} &")
        self._frida_info = None
        return self.get_frida_info()

    @check_is_root
    def get_frida_info(self, frida_server_path, frida_server_name=None) -> FridaInfo:
        if self._frida_info is None:
            if frida_server_name is None:
                frida_server_name = os.path.basename(frida_server_path)
            self._frida_info = FridaInfo(
                is_running=self.__is_frida_running(frida_server_name),
                is_installed=self.__is_frida_installed(frida_server_path),
                version=self.__get_frida_version(frida_server_path)
            )
        return self._frida_info

    @check_is_root
    def start_frida(self, frida_server_path):
        if not self.__is_frida_installed(frida_server_path):
            raise FridaServerNotInstalled(self._serial, frida_server_path)
        self._device.shell(f"su -c {frida_server_path} &")
        self._frida_info = None
        return self.get_frida_info(frida_server_path)
