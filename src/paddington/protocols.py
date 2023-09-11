from typing import Protocol, Any

from .context import Context


class Track(Protocol):
    def __call__(self, event: Any, context: Context):
        raise NotImplementedError
