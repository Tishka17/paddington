import functools
import json
from dataclasses import dataclass
from http import HTTPStatus
from operator import itemgetter
from typing import Any, TypeVar, Generic, get_type_hints

from adaptix import Retort, dumper, name_mapping, Chain

from paddington import WheelSet, Track
from .app import WsgiContext

BodyT = TypeVar("BodyT")


@dataclass
class HttpResponse(Generic[BodyT]):
    body: BodyT
    status: HTTPStatus = HTTPStatus.OK


class RestWheelSet(WheelSet):
    def __init__(self, track: Track):
        super().__init__(track, self.tie)
        self.retort = Retort(recipe=[
            name_mapping(HttpResponse, only=["body"]),
            dumper(HttpResponse, itemgetter("body"), chain=Chain.LAST)
        ])

    def _patch_track(self, track: Track):
        response_type = get_type_hints(track).get("return", HttpResponse[Any])

        @functools.wraps(track)
        def patched_track(event: any, context: WsgiContext):
            response = track(event, context)
            body = self.retort.dump(response, response_type)

            response_headers = [('Content-type', 'application/json')]
            context.start_response(
                f"{response.status.value} {response.status.phrase}",
                response_headers,
            )
            return [
                json.dumps(body).encode("utf-8"),
            ]

        return patched_track
