import functools
from typing import Any, Callable

from .base import InternalJoint, wrap_output
from ..context import Context
from ..protocols import Track, Tie


class Joint(InternalJoint):
    def __init__(
            self, track: Track,
    ) -> None:
        super().__init__(wrap_output(track))


def make_joint(track: Track) -> Callable[[Tie], Joint]:
    def make_joint_decorator(handler: Tie) -> Joint:
        @functools.wraps(handler)
        def joint_track(event: Any, context: Context):
            return handler(track, event, context)

        return Joint(joint_track)

    return make_joint_decorator
