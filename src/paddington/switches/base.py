from logging import getLogger
from typing import Any, Optional

from ..errors import ErrorEvent, RouteNotFound
from ..protocols import Switch
from ..context import Context

logger = getLogger(__name__)


class BaseSwitch:
    def __init__(self, error_switch: Optional[Switch] = None) -> None:
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

    def _dispatch(self, event: Any, context: Context):
        raise NotImplementedError


