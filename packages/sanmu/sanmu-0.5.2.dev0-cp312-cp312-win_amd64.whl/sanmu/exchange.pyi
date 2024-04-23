from .files import YamlFile as YamlFile
from _typeshed import Incomplete

logger: Incomplete

class Exchange:
    file: Incomplete
    def __init__(self, path: str = '', data: Incomplete | None = None, debug: bool = False) -> None: ...
    def extract(self, resp, var_name, attr, expr: str, index: int): ...
    def replace(self, data): ...
