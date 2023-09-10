from logging import getLogger
from typing import Protocol, Any, Callable, Optional

logger = getLogger(__name__)


class PaddingtonError(RuntimeError):
    pass


class RouteNotFound(PaddingtonError, ValueError):
    pass


class Switch(Protocol):
    def __call__(self, event: Any, context: Any):
        raise NotImplementedError


class MapSwitch:
    def __init__(self, getter: Callable):
        self.routes: dict[Any, Callable] = {}
        self.getter = getter

    def add_route(self, value: Any, route: Optional[Callable] = None):
        if route:
            self.routes[value] = route
        else:
            def decorator(route: Callable):
                self.routes[value] = route

            return decorator

    def __call__(self, event: Any, context: Any):
        key = self.getter(event, context)
        logger.debug("MapSwitch key retrieved: %s", key)
        try:
            route = self.routes[key]
        except KeyError as e:
            raise RouteNotFound from e
        return route(event, context)


class SequentialSwitch:
    def __init__(self):
        self.routes: list[tuple[Callable, Callable]] = []

    def add_route(self, predicate: Callable, route: Optional[Callable] = None):
        if route:
            self.routes.append((predicate, route))
        else:
            def decorator(route: Callable):
                self.routes.append((predicate, route))

            return decorator

    def __call__(self, event: Any, context: Any):
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
