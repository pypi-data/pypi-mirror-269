from pydantic import BaseModel


class DeviceInfo(BaseModel):
    serial: str
    product: str
    model: str
    device: str
    is_root: bool


class FridaInfo(BaseModel):
    is_running: bool
    is_installed: bool
    version: str | None
