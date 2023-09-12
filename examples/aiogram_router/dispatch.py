from typing import Callable

from aiogram.types import Update

from paddington import Context, TieJoint


def unpack_event(track: Callable, event: Update, context: Context):
    return track(event.event, **context.data)


async def polling(dispatcher, bot):
    offset = None
    dispatcher = TieJoint(dispatcher, unpack_event)

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
