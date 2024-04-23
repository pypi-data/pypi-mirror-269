from adbutils import adb

from titan._device_exception import DeviceNoFoundException
from titan._device_models import DeviceInfo, FridaInfo


class _DeviceManager(object):
    _device: adb.device
    _device_info: DeviceInfo = None
    _frida_info: FridaInfo = None

    def __init__(self, device_serial: str):
        if device_serial not in [device.serial for device in adb.device_list()]:
            raise DeviceNoFoundException(device_serial)
        self._device = adb.device(device_serial)

    @staticmethod
    def get_all_device_manager_list() -> list["_DeviceManager"]:
        return [
            _DeviceManager(device.serial)
            for device in adb.device_list()
        ]

    def get_info(self) -> DeviceInfo:
        if self._device_info is None:
            self._device_info = DeviceInfo(
                serial=self._device.serial,
                product=self._device.prop.name,
                model=self._device.prop.model,
                device=self._device.prop.device
            )
        return self._device_info

    def get_frida_info(self) -> FridaInfo:
        if self._frida_info is None:
            self._frida_info = FridaInfo(
                is_running=self.__is_frida_running(),
                is_installed=self.__is_frida_installed(),
                version=self.__get_frida_version()
            )
        return self._frida_info

    def __is_frida_running(self) -> bool:
        return self._device.shell("pgrep frida-server").strip() != ""

    def __is_frida_installed(self) -> bool:
        return self._device.shell("su -c ls /data/local/tmp/frida-server").strip() != ""

    def __get_frida_version(self) -> str:
        return self._device.shell(
            "su -c /data/local/tmp/frida-server --version"
        ).strip()
