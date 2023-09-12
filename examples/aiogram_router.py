import asyncio
import logging
import os
from typing import Callable

from aiogram import Bot
from aiogram.types import Update, Message, CallbackQuery
from paddington import MapSwitch, Context, TieJoint


def update_type(event: Update, context: Context) -> str:
    return event.event_type


router = MapSwitch(update_type)


@router.track("message")
async def process_message(event: Message, bot):
    print("message", event.text, bot)


@router.track("callback_query")
async def process_callback_query(event: CallbackQuery, bot):
    print("callback_query", event.data, bot)


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
