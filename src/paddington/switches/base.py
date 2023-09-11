from logging import getLogger
from typing import Any, Optional

from ..context import Context
from ..errors import ErrorEvent, RouteNotFound
from ..protocols import Track

logger = getLogger(__name__)


class OutputTrack:
    def __init__(self, track: Track):
        self.track = track

    def __call__(self, event: Any, context: Context):
        for tie in context.ties:
            tie(event, context)
        self.track(event, context)


class BaseSwitch:
    def __init__(self, error_switch: Optional[Track] = None) -> None:
        self.error_switch = error_switch

    def __call__(self, event: Any, context: Context):
        try:
            self._dispatch(event, context)
        except Exception as e:
            if not self.error_switch:
                raise
            error_event = ErrorEvent(e, event, self)
            try:
                self.error_switch(error_event, context)
            except RouteNotFound as rf:
                raise e

    def _wrap_output(self, switch: Track):
        if isinstance(switch, BaseSwitch):
            return switch
        return OutputTrack(switch)

    def _dispatch(self, event: Any, context: Context):
        raise NotImplementedError
