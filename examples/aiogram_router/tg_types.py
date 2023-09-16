from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


@dataclass
class Chat:
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None


@dataclass
class MessageEntity:
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None


@dataclass
class Message:
    message_id: int
    date: datetime
    chat: Chat
    message_thread_id: Optional[int] = None
    from_: Optional[User] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None


@dataclass
class CallbackQuery:
    id: str
    from_: User
    chat_instance: str
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None


@dataclass
class Update:
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None

    @property
    def event_type(self):
        attr_names = (
            key
            for key, value in self.__dict__.items()
            if key != "update_id" and value is not None
        )
        return next(attr_names, None)

    @property
    def event(self):
        attr_values = (
            value
            for key, value in self.__dict__.items()
            if key != "update_id" and value is not None
        )
        return next(attr_values, None)
