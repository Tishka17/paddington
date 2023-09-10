from logging import getLogger
from typing import Any, Callable, Optional

from .base import BaseSwitch
from ..context import Context
from ..errors import RouteNotFound
from ..protocols import Switch

logger = getLogger(__name__)


class SequentialSwitch(BaseSwitch):
    def __init__(self, error_switch: Optional[Switch] = None) -> None:
        super().__init__(error_switch)
        self.routes: list[tuple[Callable, Callable]] = []

    def add_track(self, predicate: Callable, route: Optional[Callable] = None):
        if route:
            self.routes.append((predicate, route))
        else:
            def decorator(route: Callable):
                self.routes.append((predicate, route))

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
