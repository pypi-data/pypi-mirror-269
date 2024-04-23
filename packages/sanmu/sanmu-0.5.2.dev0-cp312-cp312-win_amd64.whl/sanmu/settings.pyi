from _typeshed import Incomplete
from enum import StrEnum
from pathlib import Path
from pydantic import EmailStr as EmailStr, FilePath as FilePath, HttpUrl as HttpUrl
from pydantic_settings import BaseSettings
from typing import Optional, Union

logger: Incomplete

class AllurePathEnum(StrEnum):
    allure: str

class NotSetEnum(StrEnum):
    no: str

class DriverEnum(StrEnum):
    chrome: str

class EmailEncrypEnum(StrEnum):
    tls: str
    ssl: str
    none: str

class Settings(BaseSettings):
    vars_file: Optional[Path]
    vars_save: bool
    allure_path: Union[FilePath, AllurePathEnum]
    allure_report: Path
    allure_show: bool
    allure_url: HttpUrl
    allure_local_port: int
    email_server: str
    email_port: int
    email_account: Union[EmailStr, NotSetEnum]
    email_password: str
    email_to: Union[EmailStr, NotSetEnum]
    email_encryption: EmailEncrypEnum
    qywx_url: Union[HttpUrl, NotSetEnum]
    dingding_url: Union[HttpUrl, NotSetEnum]
    dingding_secret: str
    driver_type: DriverEnum
    driver_option: str
    selenium_grid: Union[HttpUrl, NotSetEnum]
    wait_poll: float
    wait_max: float
    touch_css: str
    force_click: bool
    screenshot_step: bool
    screenshot_error: bool
    screenshot_playback: bool
    base_url: str

class ProxySettings:
    section: Incomplete
    proxy_cls: Incomplete
    def __init__(self, section, proxy_cls) -> None: ...
    def __getattr__(self, item): ...
    def __setattr__(self, key, value) -> None: ...
    def reload_settings(self) -> None: ...

sanmu: Settings
sanmu_ui: Settings
sanmu_api: Settings
