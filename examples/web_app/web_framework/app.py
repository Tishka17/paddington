from typing import Callable

from paddington import Track, Context


class WsgiContext(Context):
    def __init__(self, start_response: Callable):
        super().__init__()
        self.start_response = start_response


class App:
    def __init__(self, switch: Track):
        self.switch = switch

    def __call__(self, environ, start_response):
        context = WsgiContext(start_response)
        return self.switch(environ, context)
