from logging import getLogger
from typing import Any, Callable, Optional

from .base import BaseSwitch, wrap_output
from ..context import Context
from ..errors import ErrorEvent, RouteNotFound
from ..protocols import Track

logger = getLogger(__name__)


class MapSwitch(BaseSwitch):
    def __init__(
            self,
            getter: Callable,
            default: Optional[Track] = None,
            error_track: Optional[Track] = None,
    ) -> None:
        super().__init__(error_track)
        self.routes: dict[Any, Callable] = {}
        self.default = default
        self.getter = getter

    def track(self, value: Any, track: Optional[Callable] = None):
        if track:
            track = wrap_output(track)
            self.routes[value] = track
        else:
            def decorator(track: Callable):
                self.track(value, track)

            return decorator

    def __getitem__(self, item) -> Track:
        return self.routes[item]

    def __setitem__(self, value: Any, track: Track):
        self.track(value, track)

    def _dispatch(self, event: Any, context: Context):
        key = self.getter(event, context)
        logger.debug("MapSwitch key retrieved: %s", key)
        try:
            route = self.routes[key]
        except KeyError as e:
            if self.default:
                return self.default(event, context)
            raise RouteNotFound from e
        else:
            try:
                return route(event, context)
            except RouteNotFound:
                if self.default:
                    return self.default(event, context)
                raise


def get_event_type(event, context: Context):
    return type(event)


def get_error_type(event: ErrorEvent, context: Context):
    return type(event.exception)


class TypeSwitch(MapSwitch):
    def __init__(
            self, error_track: Optional[Track] = None,
            default: Optional[Track] = None,
    ) -> None:
        super().__init__(
            get_error_type, error_track=error_track, default=default,
        )


class ErrorTypeSwitch(MapSwitch):
    def __init__(
            self, error_track: Optional[Track] = None,
            default: Optional[Track] = None,
    ) -> None:
        super().__init__(
            get_error_type, error_track=error_track, default=default,
        )
