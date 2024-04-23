class DeviceNoFoundException(Exception):
    def __init__(self, device_serial):
        super().__init__(f"Device with serial {device_serial} not found")
