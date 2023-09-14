from dataclasses import dataclass

from paddington import Joint, Track
from wsgi_app import App, WsgiContext
from wsgi_rest_view import RestTie, HttpResponse
from wsgi_switch import WsgiSwitch

router = WsgiSwitch()


@dataclass
class User:
    id: int
    name: str


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


router = ManagerJoint(router)
app = App(RestTie(router))
