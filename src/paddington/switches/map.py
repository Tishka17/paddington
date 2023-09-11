from logging import getLogger
from typing import Any, Callable, Optional

from .base import BaseSwitch
from ..context import Context
from ..errors import ErrorEvent, RouteNotFound
from ..protocols import Track

logger = getLogger(__name__)


class MapSwitch(BaseSwitch):
    def __init__(
            self, getter: Callable, error_track: Optional[Track] = None,
    ) -> None:
        super().__init__(error_track)
        self.routes: dict[Any, Callable] = {}
        self.getter = getter

    def add_track(self, value: Any, track: Optional[Callable] = None):
        if track:
            track = self._wrap_output(track)
            self.routes[value] = track
        else:
            def decorator(track: Callable):
                self.add_track(value, track)

            return decorator

    def _dispatch(self, event: Any, context: Context):
        key = self.getter(event, context)
        logger.debug("MapSwitch key retrieved: %s", key)
        try:
            route = self.routes[key]
        except KeyError as e:
            raise RouteNotFound from e
        return route(event, context)


def get_event_type(event, context: Context):
    return type(event)


def get_error_type(event: ErrorEvent, context: Context):
    return type(event.exception)


class TypeSwitch(MapSwitch):
    def __init__(self, error_track: Optional[Track] = None) -> None:
        super().__init__(get_event_type, error_track)


class ErrorTypeSwitch(MapSwitch):
    def __init__(self, error_track: Optional[Track] = None) -> None:
        super().__init__(get_error_type, error_track)
