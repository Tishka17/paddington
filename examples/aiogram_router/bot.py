import asyncio
import logging
import os

from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery

from routers import UpdateSwitch
from dispatch import polling

router = UpdateSwitch()


@router.message.track(F.text == "/start")
async def process_message(event: Message, bot):
    await event.answer("Started")


@router.callback_query.track()
async def process_callback_query(event: CallbackQuery, bot):
    await event.answer("Click found")


subrouter = UpdateSwitch()
@subrouter.message.track()
async def process_message(event: Message, bot):
    await event.answer("Your text: " + event.text)

router.default_track.track(track=subrouter)


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    await polling(router, bot)


if __name__ == '__main__':
    asyncio.run(main())
