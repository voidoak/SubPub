import weakref
from collections import defaultdict
from dataclasses import dataclass


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
