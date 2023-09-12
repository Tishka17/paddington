from logging import getLogger
from typing import Any, Callable, Optional, List

from .base import BaseSwitch, wrap_output
from ..context import Context
from ..errors import RouteNotFound
from ..protocols import Track

logger = getLogger(__name__)


class SequentialSwitch(BaseSwitch):
    def __init__(self, error_track: Optional[Track] = None) -> None:
        super().__init__(error_track)
        self.routes: list[tuple[List[Callable], Callable]] = []

    def _prepare_predicate(self, predicate: Any) -> Callable:
        return predicate

    def track(self, *predicates: Callable, track: Optional[Callable] = None):
        predicates = [
            self._prepare_predicate(predicate)
            for predicate in predicates
            if predicate is not None
        ]
        if track:
            track = wrap_output(track)
            self.routes.append((predicates, track))
        else:
            def decorator(track: Callable):
                return self.track(*predicates, track=track)

            return decorator

    def _validate_predicates(
            self, predicates, event: Any, context: Context,
    ) -> bool:

        for predicate in predicates:
            if not predicate(event, context):
                return False
        return True

    def _dispatch(self, event: Any, context: Context):
        print(self.routes)
        for predicates, route in self.routes:
            logger.debug(
                "SequentialSwitch try predicates %s for route %s",
                predicates, route,
            )
            if not self._validate_predicates(predicates, event, context):
                continue
            try:
                return route(event, context)
            except RouteNotFound:
                pass
        raise RouteNotFound
