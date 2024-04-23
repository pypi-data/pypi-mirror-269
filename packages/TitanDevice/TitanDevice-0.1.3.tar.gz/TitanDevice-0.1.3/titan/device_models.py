from pydantic import BaseModel


class DeviceInfo(BaseModel):
    serial: str
    product: str
    model: str
    device: str

