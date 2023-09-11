from typing import Protocol, Any

from .context import Context


class Track(Protocol):
    def __call__(self, event: Any, context: Context):
        raise NotImplementedError


class Tie(Protocol):
    def __call__(self, track: Track, event: Any, context: Context):
        raise NotImplementedError
