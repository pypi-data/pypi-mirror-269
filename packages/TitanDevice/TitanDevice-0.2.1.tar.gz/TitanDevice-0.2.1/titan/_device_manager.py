from typing import Optional

from adbutils import adb

from titan._device_exception import DeviceNoFoundException, DeviceMustBeRootedException
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

    def __is_frida_running(self) -> bool:
        return self._device.shell("pgrep frida-server").strip() != ""

    def __is_frida_installed(self) -> bool:
        return self.__file_exists("/data/local/tmp/frida-server")

    def __get_frida_version(self) -> str | None:
        if not self.__is_frida_installed():
            return None
        return self._device.shell(
            "su -c /data/local/tmp/frida-server --version"
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
    def install_frida(self, frida_server_path, dist_path):
        self._device.push(frida_server_path, dist_path)
        self._device.shell(f"su -c chmod 755 {dist_path}")
        self._device.shell(f"su -c {dist_path} &")
        self._frida_info = None
        return self.get_frida_info()

    @check_is_root
    def get_frida_info(self) -> FridaInfo:
        if self._frida_info is None:
            self._frida_info = FridaInfo(
                is_running=self.__is_frida_running(),
                is_installed=self.__is_frida_installed(),
                version=self.__get_frida_version()
            )
        return self._frida_info
