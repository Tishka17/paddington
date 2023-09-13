from typing import Callable

from aiogram.dispatcher.event.handler import CallableMixin
from aiogram.types import Update

from paddington import Context, TieJoint, Track


class UnpackTie(TieJoint):
    def __init__(self, track: Track):
        super().__init__(track, self.tie)
        self.callable_cache = {}

    def tie(self, track: Callable, event: Update, context: Context):
        patched_track = self.callable_cache.get(track)
        if not patched_track:
            patched_track = CallableMixin(callback=track).call
            self.callable_cache[track] = patched_track
        return patched_track(event.event, **context.data)


async def polling(dispatcher, bot):
    offset = None
    dispatcher = UnpackTie(dispatcher)

    while True:
        updates = await bot.get_updates(
            timeout=10,
            allowed_updates=["message", "callback_query"],
            offset=offset
        )
        for event in updates:
            context = Context()
            context.data["bot"] = bot
            await dispatcher(event, context)
            offset = event.update_id + 1
