import httpx
import pytest
from _typeshed import Incomplete
from collections.abc import Generator
from pytest_xlsx.file import XlsxItem as XlsxItem
from pytest_yaml.file import YamlItem as YamlItem
from sanmu import settings as settings
from sanmu.assertion import Assertion as Assertion
from sanmu.exchange import Exchange as Exchange
from sanmu.runner import SanmuRunner as SanmuRunner

logger: Incomplete
http_logger: Incomplete
exchanger: Incomplete

class HTTPClient(httpx.Client):
    def __init__(self, **kwargs) -> None: ...
    @staticmethod
    def log_request(request: httpx.Request): ...
    @staticmethod
    def log_response(response: httpx.Response): ...

client: Incomplete

def pytest_yaml_run_step(item: YamlItem, request: pytest.FixtureRequest): ...
def pytest_xlsx_run_step(item: XlsxItem, request: pytest.FixtureRequest): ...
def pytest_collection_modifyitems(session, config, items) -> None: ...
def pytest_unconfigure() -> None: ...
def chrome() -> Generator[Incomplete, None, None]: ...
def new_chrome() -> Generator[Incomplete, None, None]: ...
