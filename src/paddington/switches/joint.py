from logging import getLogger
from typing import Any, Callable, Optional

from .base import BaseSwitch
from ..context import Context
from ..protocols import Track

logger = getLogger(__name__)


class Joint(BaseSwitch):
    def __init__(
            self, track: Track, error_switch: Optional[Track] = None,
    ) -> None:
        super().__init__(error_switch)
        self.track = track
        self.routes: list[tuple[Callable, Callable]] = []

    def _dispatch(self, event: Any, context: Context):
        self.track(event, context)
