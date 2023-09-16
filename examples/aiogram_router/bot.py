import logging
import os

from magic_filter import F

from bot_object import TgClient
from dispatch import polling
from routers import UpdateSwitch
from tg_types import Message, CallbackQuery

router = UpdateSwitch()


@router.message(F.text == "/start")
def process_message(event: Message, bot: TgClient):
    bot.send_message(text="Started with bot", chat_id=event.chat.id)


@router.callback_query()
def process_callback_query(event: CallbackQuery, bot: TgClient):
    bot.answer_callback(callback_query_id=event.id, text="Click found")


subrouter = UpdateSwitch()


@subrouter.message()
def process_message(event: Message, bot: TgClient):
    bot.send_message(chat_id=event.chat.id, text="Your text: " + event.text)


router.include_router(subrouter)


def main():
    # real main
    logging.basicConfig(level=logging.DEBUG)
    bot = TgClient(token=os.getenv("BOT_TOKEN"))
    polling(router, bot)


if __name__ == '__main__':
    main()
