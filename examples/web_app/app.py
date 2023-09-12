import json

from wsgi_app import App, WsgiContext
from wsgi_switch import WsgiSwitch

users = []
router = WsgiSwitch()


@router.track("/", methods=["GET"])
def index(environ, context: WsgiContext):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    context.start_response(status, response_headers)
    return [b"Hello world!\n"]


@router.track("/users", methods=["GET"])
def get_users(environ, context: WsgiContext):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'application/json')]
    context.start_response(status, response_headers)
    return [json.dumps(users).encode()]


@router.track("/users", methods=["POST"])
def add_user(environ, context: WsgiContext):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'application/json')]
    context.start_response(status, response_headers)
    users.append({"user": len(users)})
    return [b"{}"]


app = App(router)
