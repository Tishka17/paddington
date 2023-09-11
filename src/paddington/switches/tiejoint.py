from typing import Any, Callable

from .base import BaseSwitch
from ..context import Context
from ..protocols import Track


class TieJoint(BaseSwitch):
    def __init__(self, track: Track, tie: Callable):
        super().__init__()
        self.track = track
        self.tie = tie

    def _dispatch(self, event: Any, context: Context):
        context.ties.append(self.tie)
        try:
            self.track(event, context)
        finally:
            context.ties.pop()


def make_tie(track: Track):
    def tie_decorator(tie: Callable[[Track, Any, Context], Any]):
        return TieJoint(track, tie)

    return tie_decorator
