import typing as T

from collections import defaultdict
from .get_class import _getcls


class EventNotFound(Exception):
    """Raised if event has not yet been subscribed by any bound methods"""

    def __init__(self, event: str) -> None:
        super().__init__()
        self.event = event

    def __str__(self) -> str:
        return f"Unsubscribed event of type '{self.event}' cannot be published to."


class SubNameError(Exception):
    """Raised if subscribed bound method does not follow proper naming format"""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.event = name

    def __str__(self) -> str:
        return "Subscribed method names must be prefixed with 'on_'; " \
        f"possible solution: 'on_{self.event}'"


class Events:
    """Subscribe/publish events system class.

    Subscribe a bound method by decorating with `Events.subscribe`.
    Publish an event by calling `Events.publish(event_name, *args, **kwargs)`.
    """

    _subscriptions: dict[str, T.Callable] = defaultdict(list)

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

        def _sub_wrapper(func: T.Callable) -> T.Callable:
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
    def publish(event: str, *args: T.Any, **kwargs: T.Any) -> None:
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
