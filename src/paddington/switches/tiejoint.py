from typing import Any, Callable

from .base import BaseSwitch, wrap_output
from ..context import Context
from ..protocols import Track, Tie


class TieJoint(BaseSwitch):
    def __init__(self, track: Track, tie: Tie):
        super().__init__()
        self.track = wrap_output(track)
        self.tie = tie

    def _dispatch(self, event: Any, context: Context):
        context.ties.append(self.tie)
        try:
            return self.track(event, context)
        finally:
            context.ties.pop()


def make_tie(track: Track) -> Callable[[Tie], TieJoint]:
    def tie_decorator(tie: Tie) -> TieJoint:
        return TieJoint(track, tie)

    return tie_decorator
