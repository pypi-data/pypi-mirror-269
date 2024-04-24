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
