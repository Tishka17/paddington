import asyncio
import logging
import os
from typing import Callable, Optional

from aiogram import Bot, MagicFilter, F
from aiogram.types import Update, Message, CallbackQuery

from paddington import MapSwitch, Context, TieJoint, SequentialSwitch


def update_type(event: Update, context: Context) -> str:
    return event.event_type


class FSwitch(SequentialSwitch):
    def track(self, predicate: Callable | MagicFilter | None = None,
              track: Optional[Callable] = None):
        if predicate is None:
            def real_predicate(event, context):
                return True
        elif isinstance(predicate, MagicFilter):
            def real_predicate(event, context):
                return predicate.resolve(event.event)
        else:
            real_predicate = predicate
        return super().track(real_predicate, track)


router = MapSwitch(update_type)
message_router = FSwitch()
router.track("message", message_router)
callback_router = FSwitch()
router.track("callback_query", callback_router)


@message_router.track(F.text == "/start")
async def process_message(event: Message, bot):
    await event.answer("Started")


@message_router.track()
async def process_message(event: Message, bot):
    await event.answer("Your text: " + event.text)


@callback_router.track()
async def process_callback_query(event: CallbackQuery, bot):
    await event.answer("Click found")


def unpack_event(track: Callable, event: Update, context: Context):
    return track(event.event, **context.data)


dispatcher = TieJoint(router, unpack_event)


async def polling(bot):
    offset = None
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


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    await polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
