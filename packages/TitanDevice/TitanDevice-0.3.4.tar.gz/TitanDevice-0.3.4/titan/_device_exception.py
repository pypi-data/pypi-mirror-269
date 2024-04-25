class DeviceNoFoundException(Exception):
    def __init__(self, device_serial):
        super().__init__(f"Device with serial {device_serial} not found")


class DeviceMustBeRootedException(Exception):
    def __init__(self, device_serial):
        super().__init__(
            f'Device [{device_serial}] must be rooted to perform this operation'
        )


class FridaServerNotInstalled(Exception):
    def __init__(self, device_serial, frida_server_path):
        super().__init__(
            f'Frida server is not installed in {frida_server_path} on device with serial {device_serial}'
        )


class FridaServerNotRunning(Exception):
    def __init__(self, device_serial, frida_server_name):
        super().__init__(
            f'Frida server [{frida_server_name}] is not running on device with serial {device_serial}'
        )


class PackageNotInstalled(Exception):
    def __init__(self, device_serial, package_name):
        super().__init__(f'Package {package_name} is not installed in {device_serial}')


class InstallPackageMustUninstallFirst(Exception):
    def __init__(self, device_serial, package_name):
        super().__init__(
            f'Package {package_name} is already installed in {device_serial}'
        )
