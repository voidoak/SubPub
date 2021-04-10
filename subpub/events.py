import weakref

from typing import Any, Callable
from collections import defaultdict

from .get_class import _getcls
from .exceptions import SubNameError, EventNotFound

class TrackRefs:
    """Metaclass to give subclasses the ability to track all instances.

    This allows for easy GC when the object is deleted or has no references left."""

    __refs__ = defaultdict(list)

    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        """generator method to yield instances of inputted class"""
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()  # create instance from weak reference
            if inst is not None:
                yield inst


class Events:
    """Subscribe/publish events system class.

    Subscribe a bound method by decorating with `Events.subscribe`.
    Publish an event by calling `Events.publish(event_name, *args, **kwargs)`.
    """

    _subscriptions: dict[str, Callable] = defaultdict(list)

    @staticmethod
    def subscribe() -> None:
        """Subscription decorator for bound method event listeners.

        Subscribed bound method's class must inherit from `TrackRefs` to allow for
        publishing to access all instances of the class. Overriding `__init__`
        will override this behaviour, so `super().__init__` should be called if
        this is done.

        Listener method names must be prefixed with `on_`, with the event name
        directly after; eg. `on_get_request`, which would be published to with
        `Events.publish("get_request", ... )`
        """

        def _sub_wrapper(func: Callable) -> Callable:
            event = func.__name__  # get name of event
            subs = Events._subscriptions

            if not (event.startswith("on_") and len(event) > 3):
                raise SubNameError(event)

            event = event[3:]                  # remove 'on_' prefix
            subs[event] = subs.get(event, [])  # get the event's subs, or []
            subs[event].append(func)           # add function to event's subs

            return func
        return _sub_wrapper

    @staticmethod
    def publish(event: str, *args: Any, **kwargs: Any) -> None:
        """Publish a given event `event` to listeners subscribed to the name of
        the event.
        """
        subs = Events._subscriptions.get(event, None)

        if subs is None:
            raise EventNotFound(event)

        for sub in subs:
            cls =_getcls(sub)                 # get the method's class
            for inst in cls.get_instances():  # cls must inherit from TrackRefs
                # get and call the instance's subscribed method
                subbed_mthd = getattr(inst, sub.__name__, None)
                subbed_mthd(*args, **kwargs)
