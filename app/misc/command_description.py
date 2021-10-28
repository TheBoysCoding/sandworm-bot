from dataclasses import dataclass
from collections.abc import Callable

@dataclass
class CommandDescription:
    command: str
    description: str
    func: Callable = None
