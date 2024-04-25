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


class PackageInfo(BaseModel):
    package_name: str
    version_name: str
    version_code: int | None
    flags: list[str]
    first_install_time: int
    last_update_time: int
    path: str
    sub_apk_paths: list[str] | None


class RunningAppInfo(BaseModel):
    package: str
    activity: str
    pid: int = 0
