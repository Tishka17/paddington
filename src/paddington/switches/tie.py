from typing import Any, Callable

from .base import BaseSwitch
from ..context import Context


class Tie(BaseSwitch):
    def __init__(self, switch: Callable, handler: Callable):
        super().__init__()
        self.switch = switch
        self.handler = handler

    def _dispatch(self, event: Any, context: Context):
        context.ties.append(self.handler)
        try:
            self.switch(event, context)
        finally:
            context.ties.pop()
