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
        return "Subscribed method names must be prefixed with 'on_'; possible solution: 'on_{self.event}'"
