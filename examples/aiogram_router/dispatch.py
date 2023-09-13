from typing import Callable, Any

from aiogram.dispatcher.event.handler import CallableMixin
from aiogram.types import Update

from paddington import Context, TieJoint, Track
from paddington.switches.base import OutputTrack


class UnpackTie(TieJoint):
    def __init__(self, track: Track):
        super().__init__(track, self.tie)

    def _patch_output(self, output: OutputTrack, flag: Any):
        if flag in output.flags:
            return
        output_track = CallableMixin(callback=output.track).call

        def patched_track(event: Update, context: Context):
            return output_track(event.event, **context.data)

        output.track = patched_track
        output.flags[UnpackTie] = True

    def tie(self, track: Callable, event: Update, context: Context):
        self._patch_output(context.output, self.__class__)
        return track(event, context)


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
