from typing import Any

from aiogram import MagicFilter
from aiogram.types import Update

from paddington import SequentialSwitch, MapSwitch, Context


class FSwitch(SequentialSwitch):

    def _prepare_predicate(self, predicate: Any):
        if isinstance(predicate, MagicFilter):
            def real_predicate(event, context):
                return predicate.resolve(event.event)

            return real_predicate
        return predicate


def update_type(event: Update, context: Context) -> str:
    return event.event_type


class UpdateSwitch(MapSwitch):
    default: FSwitch

    def __init__(self):
        super().__init__(update_type, FSwitch())
        self.message = self["message"] = FSwitch()
        self.callback_query = self["callback_query"] = FSwitch()
