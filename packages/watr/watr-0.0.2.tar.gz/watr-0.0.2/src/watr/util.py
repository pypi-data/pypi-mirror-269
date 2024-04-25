from typing import Any, Callable, Iterable, TypeVar

_T = TypeVar("_T")


def first_or_none(lst: Iterable[_T], predicate: Callable[[_T], Any]) -> _T | None:
    """Return the first occurrence or `None` of an iterable, given a predicate."""
    filter_iter = filter(predicate, lst)
    return next(filter_iter, None)
