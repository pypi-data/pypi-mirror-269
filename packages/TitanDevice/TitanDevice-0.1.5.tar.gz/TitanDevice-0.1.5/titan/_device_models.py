from pydantic import BaseModel


class DeviceInfo(BaseModel):
    serial: str
    product: str
    model: str
    device: str


class FridaInfo(BaseModel):
    is_running: bool
    is_installed: bool
    version: str
