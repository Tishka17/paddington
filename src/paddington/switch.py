from logging import getLogger
from typing import Protocol, Any, Callable, Optional

from .errors import ErrorEvent, RouteNotFound

logger = getLogger(__name__)


class Switch(Protocol):
    def __call__(self, event: Any, context: Any):
        raise NotImplementedError


class BaseSwitch:
    def __init__(self, error_switch: Optional[Switch] = None) -> None:
        self.error_switch = error_switch

    def __call__(self, event: Any, context: Any):
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

    def _dispatch(self, event: Any, context: Any):
        raise NotImplementedError


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


class SequentialSwitch(BaseSwitch):
    def __init__(self, error_switch: Optional[Switch] = None) -> None:
        super().__init__(error_switch)
        self.routes: list[tuple[Callable, Callable]] = []

    def add_route(self, predicate: Callable, route: Optional[Callable] = None):
        if route:
            self.routes.append((predicate, route))
        else:
            def decorator(route: Callable):
                self.routes.append((predicate, route))

            return decorator

    def _dispatch(self, event: Any, context: Any):
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
