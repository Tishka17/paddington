import json

from wsgi_app import App, WsgiContext
from wsgi_switch import WsgiSwitch
from http import HTTPStatus

users = []
router = WsgiSwitch()


def status(http_status: HTTPStatus):
    return f"{http_status.value} {http_status.phrase}"


@router.track("/", methods=["GET"])
def index(environ, context: WsgiContext):
    response_headers = [('Content-type', 'text/plain')]
    context.start_response(status(HTTPStatus.OK), response_headers)
    return [b"Hello world!\n"]


@router.track("/users", methods=["GET"])
def get_users(environ, context: WsgiContext):
    response_headers = [('Content-type', 'application/json')]
    context.start_response(status(HTTPStatus.OK), response_headers)
    return [json.dumps(users).encode()]


@router.track("/users", methods=["POST"])
def add_user(environ, context: WsgiContext):
    response_headers = [('Content-type', 'application/json')]
    context.start_response(status(HTTPStatus.OK), response_headers)
    users.append({"user": len(users)})
    return [b"{}"]


app = App(router)
