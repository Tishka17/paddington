class PaddingtonError(Exception):
    pass


class RouteNotFound(PaddingtonError):
    pass


class ErrorEvent:
    def __init__(self, exception, router, event):
        self.exception = exception
        self.router = router
        self.event = event

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({self.exception!r}, {self.router!r}, {self.event!r})"
        )
