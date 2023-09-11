import functools
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any, Optional, Callable

from ..context import Context
from ..errors import ErrorEvent, RouteNotFound
from ..protocols import Track, Tie

logger = getLogger(__name__)


class InternalTrack(ABC):
    @abstractmethod
    def __call__(self, event: Any, context: Context):
        raise NotImplementedError


class OutputTrack(InternalTrack):
    def __init__(self, track: Track):
        self.track = track

    def __call__(self, event: Any, context: Context):
        track = self.track
        for tie in reversed(context.ties):
            track = make_internal_joint(track, tie)
        track(event, context)


def wrap_output(track: Track) -> InternalTrack:
    if isinstance(track, InternalTrack):
        return track
    return OutputTrack(track)


class InternalJoint(InternalTrack):
    def __init__(
            self, track: Track,
    ) -> None:
        super().__init__()
        self.track = track

    def __call__(self, event: Any, context: Context):
        self.track(event, context)


def make_internal_joint(
        track: Track, handler: Tie,
) -> InternalJoint:
    def joint_track(event: Any, context: Context):
        return handler(track, event, context)

    return InternalJoint(joint_track)


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
            except RouteNotFound:
                raise e

    def _dispatch(self, event: Any, context: Context):
        raise NotImplementedError
