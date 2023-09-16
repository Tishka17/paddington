import inspect
from typing import Dict, Any

from paddington import Context, Track, WheelSet
from .types import Update


class UnpackWheelSet(WheelSet):
    def __init__(self, track: Track):
        super().__init__(track, self.tie)

    def _prepare_kwargs(self, spec, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        if spec.varkw:
            return kwargs

        return {
            k: v for k, v in kwargs.items() if
            k in spec.args or k in spec.kwonlyargs
        }

    def _patch_track(self, track: Track):
        callback = inspect.unwrap(track)
        spec = inspect.getfullargspec(callback)

        def patched_track(event: Update, context: Context):
            kwargs = self._prepare_kwargs(spec, context.data)
            return callback(event.event, **kwargs)

        return patched_track


def polling(dispatcher, bot):
    offset = None
    dispatcher = UnpackWheelSet(dispatcher)

    while True:
        updates = bot.get_updates(
            offset=offset,
            limit=10,
            timeout=10,
            allowed_updates=["message", "callback_query"],
        )
        for event in updates:
            context = Context()
            context.data["bot"] = bot
            dispatcher(event, context)
            offset = event.update_id + 1
