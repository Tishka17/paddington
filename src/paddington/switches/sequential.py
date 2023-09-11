from logging import getLogger
from typing import Any, Callable, Optional

from .base import BaseSwitch, wrap_output
from ..context import Context
from ..errors import RouteNotFound
from ..protocols import Track

logger = getLogger(__name__)


class SequentialSwitch(BaseSwitch):
    def __init__(self, error_track: Optional[Track] = None) -> None:
        super().__init__(error_track)
        self.routes: list[tuple[Callable, Callable]] = []

    def add_track(self, predicate: Callable, track: Optional[Callable] = None):
        if track:
            track = wrap_output(track)
            self.routes.append((predicate, track))
        else:
            def decorator(track: Callable):
                self.add_track(predicate, track)

            return decorator

    def _dispatch(self, event: Any, context: Context):
        for predicate, route in self.routes:
            logger.debug(
                "SequentialSwitch try predicate %s for route %s",
                predicate, route,
            )
            if predicate(event, context):
                try:
                    return route(event, context)
                except RouteNotFound:
                    pass
        raise RouteNotFound
