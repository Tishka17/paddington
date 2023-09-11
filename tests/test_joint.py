from typing import Any
from unittest.mock import Mock

from paddington import Joint, Context, Track


class MyJoint(Joint):
    def __init__(
            self,
            track: Track,
            pre: Track,
            post: Track,
    ) -> None:
        super().__init__(track)
        self.pre = pre
        self.post = post

    def __call__(self, event: Any, context: Context):
        self.pre(event, context)
        super().__call__(event, context)
        self.post(event, context)


def test_joint():
    pre = Mock()
    handle = Mock()
    post = Mock()
    joint = MyJoint(handle, pre, post)
    c = Context()
    joint(1, c)
    pre.assert_called_once_with(1, c)
    handle.assert_called_once_with(1, c)
    post.assert_called_once_with(1, c)
