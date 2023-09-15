import logging
from dataclasses import dataclass
from http import HTTPStatus

from paddington import (
    Joint, Track, ErrorEvent, ErrorTypeSwitch, RouteNotFound, SequentialSwitch,
)
from wsgi_app import App, WsgiContext
from wsgi_rest_view import RestTie, HttpResponse
from wsgi_switch import WsgiSwitch

error_router = ErrorTypeSwitch(default=SequentialSwitch())
router = WsgiSwitch(error_track=error_router)


@dataclass
class User:
    id: int
    name: str


@dataclass
class Error:
    error: str


class UserManager:
    def __init__(self):
        self.users = []


class ManagerJoint(Joint):
    def __init__(self, track: Track):
        super().__init__(track)
        self.user_manager = UserManager()

    def __call__(self, event, context: WsgiContext):
        context.data["user_manager"] = self.user_manager
        return self.track(event, context)


@router.track("/", methods=["GET"])
def index(environ, context: WsgiContext) -> HttpResponse[dict[str, str]]:
    return HttpResponse(
        body={"ok": "Index"}
    )


@router.track("/users", methods=["GET"])
def get_users(environ, context: WsgiContext) -> HttpResponse[list[User]]:
    user_manager: UserManager = context.data["user_manager"]
    return HttpResponse(body=user_manager.users)


@router.track("/users", methods=["POST"])
def add_user(environ, context: WsgiContext) -> HttpResponse[User]:
    user_manager: UserManager = context.data["user_manager"]

    user = User(
        id=len(user_manager.users),
        name=f"User {len(user_manager.users)}",
    )

    user_manager.users.append(user)
    return HttpResponse(body=user)


@error_router.track(RouteNotFound)
def handle_not_found_error(
        environ: ErrorEvent, context: WsgiContext,
) -> HttpResponse[Error]:
    logging.error(f"Resource {environ.event['PATH_INFO']} not found")
    return HttpResponse(
        status=HTTPStatus.NOT_FOUND,
        body=Error(error=f"Resource {environ.event['PATH_INFO']} not found"),
    )


@error_router.default.track()
def handle_any_error(
        environ: ErrorEvent, context: WsgiContext,
) -> HttpResponse[Error]:
    logging.error("Unhandled error in HTTP")
    return HttpResponse(
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
        body=Error(error=str(environ.exception)),
    )


router = ManagerJoint(router)
app = App(RestTie(router))
