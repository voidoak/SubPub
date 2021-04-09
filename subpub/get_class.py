import typing as T
import inspect, functools


def _getcls(mthd: T.Callable):
    """Get class to which a given method belongs to"""

    if isinstance(mthd, functools.partial):
        return _getcls(mthd.func)  # find the base class for the original method

    if inspect.ismethod(mthd) or (
        inspect.isbuiltin(mthd)
        and getattr(mthd, "__self__", None) is not None
        and getattr(mthd.__self__, "__class__", None)):

        for cls in inspect.getmro(mthd.__self__.__class__):
            if mthd.__name__ in cls.__dict__:
                return cls

        mthd = getattr(mthd, "__func__", mthd)

    if inspect.isfunction(mthd):
        cls = getattr(
            inspect.getmodule(mthd),
            mthd.__qualname__.split(".<locals>.", 1)[0].rsplit(".", 1)[0],
            None
        )

        if isinstance(cls, type):
            return cls

    return getattr(mthd, "__objclass__", None)  # special descriptor objects
