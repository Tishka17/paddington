import json
from datetime import datetime
from typing import List, Any

from adaptix import Retort, dumper, loader
from dataclass_rest import get
from dataclass_rest.client_protocol import FactoryProtocol
from dataclass_rest.http.requests import RequestsClient, RequestsMethod
from requests import Session, Response

from .types import Update, Message


class TgError(Exception):
    pass


class TgMethod(RequestsMethod):

    def _response_body(self, response: Response) -> Any:
        json_body = super()._response_body(response)
        if not (ok := json_body.get("ok")):
            raise TgError(
                (json_body.get("description"), json_body.get("error_code")),
            )
        return json_body.get("result")


class TgClient(RequestsClient):
    method_class = TgMethod

    def __init__(self, token):
        super().__init__(f"https://api.telegram.org/bot{token}/", Session())

    def _init_request_args_factory(self) -> Retort:
        return Retort(recipe=[
            dumper(List, json.dumps)
        ])

    def _init_response_body_factory(self) -> FactoryProtocol:
        return Retort(recipe=[
            loader(datetime, datetime.fromtimestamp),
        ])

    @get("getUpdates")
    def get_updates(
            self, offset: int, limit: int, timeout: int,
            allowed_updates: List[str],
    ) -> List[Update]:
        pass

    @get("sendMessage")
    def send_message(
            self, chat_id: int, text: str,
    ) -> Message:
        pass

    @get("answerCallbackQuery")
    def answer_callback(
            self, callback_query_id: str, text: str, show_alert: bool = False,
    ) -> bool:
        pass
