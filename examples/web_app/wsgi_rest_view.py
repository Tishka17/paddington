import functools
import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, TypeVar, Generic, get_type_hints, get_args

from adaptix import Retort

from wsgi_app import WsgiContext
from paddington import WheelSet, Track

BodyT = TypeVar("BodyT")


@dataclass
class HttpResponse(Generic[BodyT]):
    body: BodyT
    status: HTTPStatus = HTTPStatus.OK


class RestTie(WheelSet):
    def __init__(self, track: Track):
        super().__init__(track, self.tie)
        self.retort = Retort()

    def _patch_track(self, track: Track):
        response_type = get_type_hints(track).get("return", HttpResponse[Any])
        body_type = get_args(response_type)[0]

        @functools.wraps(track)
        def patched_track(event: any, context: WsgiContext):
            response = track(event, context)
            response_headers = [('Content-type', 'application/json')]
            context.start_response(
                f"{response.status.value} {response.status.phrase}",
                response_headers,
            )
            body = self.retort.dump(response.body, body_type)
            return [
                json.dumps(body).encode("utf-8"),
            ]

        return patched_track
