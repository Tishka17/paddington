from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any, Optional, Callable

from ..context import Context
from ..errors import ErrorEvent, RouteNotFound
from ..protocols import Track

logger = getLogger(__name__)


class OutputTrack:
    def __init__(self, track: Track):
        self.track = track

    def __call__(self, event: Any, context: Context):
        track = self.track
        for tie in reversed(context.ties):
            track = make_joint(track)(tie)
        track(event, context)


class InternalTrack(ABC):
    @abstractmethod
    def __call__(self, event: Any, context: Context):
        raise NotImplementedError


class Joint(InternalTrack):
    def __init__(
            self, track: Track,
    ) -> None:
        super().__init__()
        self.track = track

    def __call__(self, event: Any, context: Context):
        self.track(event, context)


def make_joint(track: Track):
    def make_joint_decorator(handler: Callable[[Track, Any, Context], Any]):
        def joint_track(event: Any, context: Context):
            return handler(track, event, context)

        return Joint(joint_track)

    return make_joint_decorator


class BaseSwitch(InternalTrack):
    def __init__(self, error_track: Optional[Track] = None) -> None:
        self.error_track = error_track

    def __call__(self, event: Any, context: Context):
        if not self.error_track:
            return self._dispatch(event, context)

        try:
            self._dispatch(event, context)
        except Exception as e:
            error_event = ErrorEvent(e, event, self)
            try:
                self.error_track(error_event, context)
            except RouteNotFound as rf:
                raise e

    def _wrap_output(self, track: Track):
        if isinstance(track, InternalTrack):
            return track
        return OutputTrack(track)

    def _dispatch(self, event: Any, context: Context):
        raise NotImplementedError
