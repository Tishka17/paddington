from typing import Protocol, Any

from .context import Context


class Switch(Protocol):
    def __call__(self, event: Any, context: Context):
        raise NotImplementedError
