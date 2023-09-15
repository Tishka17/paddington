from aiogram.dispatcher.event.handler import CallableMixin
from aiogram.types import Update

from paddington import Context, Track, WheelSet


class UnpackWheelSet(WheelSet):
    def __init__(self, track: Track):
        super().__init__(track, self.tie)

    def _patch_track(self, track: Track):
        output_track = CallableMixin(callback=track).call

        def patched_track(event: Update, context: Context):
            return output_track(event.event, **context.data)

        return patched_track


async def polling(dispatcher, bot):
    offset = None
    dispatcher = UnpackWheelSet(dispatcher)

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
