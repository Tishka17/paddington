import re
from typing import Callable, Any

from paddington import SequentialSwitch


def url(regex_str):
    regex = re.compile(regex_str)

    def url_match(environ, context):
        return regex.fullmatch(environ["PATH_INFO"])

    return url_match


def method(*methods):
    def method_match(environ, context):
        return environ["REQUEST_METHOD"] in methods

    return method_match


class WsgiSwitch(SequentialSwitch):
    def track(
            self, *predicates: Callable | str,
            methods: list[str] | None = None,
            track: Callable | None = None,
    ):
        if methods:
            predicates = predicates + (method(*methods),)
        return super().track(*predicates, track=track)

    def _prepare_predicate(self, predicate: Any) -> Callable:
        if isinstance(predicate, str):
            return url(predicate)
        return predicate
