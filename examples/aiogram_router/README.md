Aiogram routing example
===========================

* `FSwitch` is a variant of `SequentialSwitch` which allows to use `F`-filters as predicates
* `UpdateSwitch` is a variant of `MapSwitch` who filters event by their update type with aiogram-style registration
* `UnpackWheelSet` is an adapter to pass event and middleware arguments in aiogram style
* `polling` is a function which poll telegram for updates and call handlers
* `bot.py` is a main bot file with bot handlers