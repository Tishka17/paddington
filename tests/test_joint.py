from typing import Any, Optional
from unittest.mock import Mock

import pytest

from paddington import Joint, Context, Track


class MyJoint(Joint):
    def __init__(
            self,
            track: Track,
            pre: Track,
            post: Track,
            error_switch: Optional[Track] = None,
    ) -> None:
        super().__init__(track, error_switch)
        self.pre = pre
        self.post = post

    def _dispatch(self, event: Any, context: Context):
        self.pre(event, context)
        super()._dispatch(event, context)
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


def test_joint_error():
    pre = Mock()
    handle = Mock(side_effect=ArithmeticError)
    post = Mock()
    error = Mock(side_effect=SyntaxError)
    joint = MyJoint(handle, pre, post, error)
    c = Context()
    with pytest.raises(SyntaxError):
        joint(1, c)
    pre.assert_called_once_with(1, c)
    handle.assert_called_once_with(1, c)
    post.assert_not_called()
    error.assert_called_once()
