from typing import Any, Callable

from .base import BaseSwitch, wrap_output, OutputTrack
from ..context import Context
from ..protocols import Track, Tie


class WheelSet(BaseSwitch):
    def __init__(self, track: Track, flag: Any = None):
        super().__init__()
        self.flag = flag or self.__class__
        self.track = wrap_output(track)

    def _patch_track(self, track: Track):
        return track

    def tie(self, track: Callable, event: Any, context: Context):
        output = context.output
        if self.flag not in output.flags:
            output.track = self._patch_track(output.track)
            output.flags[self.flag] = True
        return track(event, context)

    def _dispatch(self, event: Any, context: Context):
        context.ties.append(self.tie)
        try:
            return self.track(event, context)
        finally:
            context.ties.pop()
