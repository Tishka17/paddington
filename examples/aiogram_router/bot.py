import asyncio
import logging
import os

from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery

from dispatch import polling
from routers import UpdateSwitch

router = UpdateSwitch()


@router.message(F.text == "/start")
async def process_message(event: Message, bot: Bot):
    await bot.send_message(text="Started with bot", chat_id=event.chat.id)


@router.callback_query()
async def process_callback_query(event: CallbackQuery):
    await event.answer("Click found")


subrouter = UpdateSwitch()


@subrouter.message()
async def process_message(event: Message):
    await event.answer("Your text: " + event.text)


router.include_router(subrouter)


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    await polling(router, bot)


if __name__ == '__main__':
    asyncio.run(main())
