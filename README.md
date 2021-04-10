# SubPub
Subscribe/Publish style event system for Python 3.x

---
## Overview
This library uses a simple decorator system to subscribe bound methods to a given event, which can be published to with a given set of args or kwargs, which are then passed off to the methods subscribed to the given event. The only requirement for a class to be viable for method subscription, is for it to inherit and initialize attributes from `TrackRefs`. If you override `__init__`, you must call `super().__init__`, or call `TrackRefs.__init__`.

*Note: for dataclasses, one can always call `TrackRefs.__init__` in `__post_init__`*

Example: A bound method subscribes to a given event, determined by its name.
```python
class Adder(TrackRefs):
    @Events.subscribe()
    def on_nums_event(self, x: int, y: int, *, z: int) -> None:
        print("Adder:", x + y + z)

class Subtractor(TrackRefs):
    @Events.subscribe()
    def on_nums_event(self, x: int, y: int, *, z: int) -> None:
        print("Subtractor:", x - y - z)
```
The two given above subscribe to an event type `nums_event`. When `Events.publish` is called with the passed in `event` argument being a string equal to `"nums_event"`, it will call these methods from every instance of a class that has a subscribed method to that particular event.

Thus:
```python
>>> add = Adder()
>>> Events.publish("nums_event", 10, 20, z=30)
Adder: 60
>>> sub = Subtractor()
>>> Events.publish("nums_event", 40, 50, z=60)
Adder: 150
Subtractor: -70
```
----
### What can I use this for?
The main purpose of this library was for systematic calls to bound methods written with side effects in mind. This can be easily achieved with this library.
 ### Can subscribed methods be further decorated?
Absolutely. Be sure to leave `Events.subscribe` as the last decorator, and wrapping a subscribed method, eg. with `functools.cache`, works just fine.
```python
class C(TrackRefs):
    @functools.cache
    @Events.subscribe()
    def on_foo(self, spam):
        return self.bar + spam.egg
```
This example does conflict with the core concept of the library to provide support for side effect methods, but these methods can still be called, regardless of whether or not its event has been published to. Also, it is worth noting that decorators just as easily provide new behaviours to methods, besides manipulating its return value (eg. loggers).

###How can I contribute?
You can always contact me [on Discord](https://discord.gg/5d7BzA6pWa), or create an issue on the repository for something you think should be fixed or added.
