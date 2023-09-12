from dataclasses import dataclass
from typing import Any, Callable

from paddington import Context, TypeSwitch, TieJoint


@dataclass
class CommandOne:
    value: str


class CommandOneHandler:
    def __init__(self, dependency: str):
        self.dependency = dependency

    def __call__(self, command: CommandOne):
        print(self.dependency, command)


def inject(track: Callable, event: Any, context: Context):
    return track(context.data["dependency"])(event)


mediator = TypeSwitch()
mediator.track(CommandOne, CommandOneHandler)

root = TieJoint(mediator, inject)

context = Context()
context.data["dependency"] = "dependency_value"
root(CommandOne("value"), context)
