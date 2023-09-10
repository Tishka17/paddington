from typing import Protocol, Any


class Switch(Protocol):
    def __call__(self, event: Any, context: Any):
        raise NotImplementedError
