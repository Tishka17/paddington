from logging import getLogger
from typing import Protocol, Any, Callable, Optional

from ..errors import ErrorEvent, RouteNotFound
from .base import BaseSwitch
from ..protocols import Switch

logger = getLogger(__name__)


class MapSwitch(BaseSwitch):
    def __init__(
            self, getter: Callable, error_switch: Optional[Switch] = None,
    ) -> None:
        super().__init__(error_switch)
        self.routes: dict[Any, Callable] = {}
        self.getter = getter

    def add_route(self, value: Any, route: Optional[Callable] = None):
        if route:
            self.routes[value] = route
        else:
            def decorator(route: Callable):
                self.routes[value] = route

            return decorator

    def _dispatch(self, event: Any, context: Any):
        key = self.getter(event, context)
        logger.debug("MapSwitch key retrieved: %s", key)
        try:
            route = self.routes[key]
        except KeyError as e:
            raise RouteNotFound from e
        return route(event, context)


def get_event_type(event, context):
    return type(event)


def get_error_type(event, context):
    return type(event.exception)


class TypeSwitch(MapSwitch):
    def __init__(self, error_switch: Optional[Switch] = None) -> None:
        super().__init__(get_event_type, error_switch)


class ErrorTypeSwitch(MapSwitch):
    def __init__(self, error_switch: Optional[Switch] = None) -> None:
        super().__init__(get_error_type, error_switch)
