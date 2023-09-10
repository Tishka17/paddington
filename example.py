import logging

from paddington import (
    Context, ErrorTypeSwitch, TypeSwitch, RouteNotFound, SequentialSwitch,
)

error_type_switch = ErrorTypeSwitch()


@error_type_switch.add_track(ValueError)
def handle_value_error(event, context):
    print("!!! handler_value_error", event, context)


suppress_route_not_found = ErrorTypeSwitch()


@suppress_route_not_found.add_track(RouteNotFound)
def handle_no_route(event, context):
    print("!!! handle_no_route", event, context)


event_type_switch = TypeSwitch(error_switch=error_type_switch)


@event_type_switch.add_track(int)
def handle_int(event, context):
    print(">>> handle_int", event, context)


@event_type_switch.add_track(str)
def handle_str(event, context):
    print(">>> handle_str", event, context)
    raise ValueError


root_switch = SequentialSwitch(error_switch=suppress_route_not_found)


@root_switch.add_track(lambda event, context: event == "test")
def handle_test(event, context):
    print(">>> handle_test", event, context)


root_switch.add_track(lambda event, context: True, event_type_switch)


def main():
    logging.basicConfig(level=logging.INFO)
    root_switch("test", Context())
    root_switch("hello_world", Context())
    root_switch(1, Context())
    root_switch(None, Context())


if __name__ == '__main__':
    main()
