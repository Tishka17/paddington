from typing import Any

from magic_filter import MagicFilter

from paddington import SequentialSwitch, MapSwitch, Context, Track
from tg_types import Update


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
        self.message = self.track("message", FSwitch()).track
        self.callback_query = self.track("callback_query", FSwitch()).track

    def include_router(self, track: Track):
        self.default.track(track=track)
