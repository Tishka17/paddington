import logging

from paddington import Context, MapSwitch, SequentialSwitch

type_switch = MapSwitch(getter=lambda event, context: type(event))


@type_switch.add_route(int)
def handle_int(event, context):
    print(">>> handle_int", event, context)


@type_switch.add_route(str)
def handle_str(event, context):
    print(">>> handle_str", event, context)


root_switch = SequentialSwitch()


@root_switch.add_route(lambda event, context: event == "test")
def handle_test(event, context):
    print(">>> handle_test", event, context)


root_switch.add_route(lambda event, context: True, type_switch)


def main():
    logging.basicConfig(level=logging.DEBUG)
    root_switch("test", Context())
    root_switch("hello_world", None)
    root_switch(1, None)
    root_switch(None, None)


if __name__ == '__main__':
    main()
