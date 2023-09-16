Web app example
==================

This is an example of micro framework running directly over WSGI.

* `App` is a root class which creates Context and adapts wsgi call to more generic one
* `WsgiSwitch` is a vairant of `SequentialSwitch` with more simple filters for common web app cases
* `RestWheelSet` is an adapter, which converts result of a view function from dataclass to wsgi response
* `app.py` is a main file with view functions and default error handlers

start using `gunicorn app:app`