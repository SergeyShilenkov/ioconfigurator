from typing import Callable

from parsers.parser import model


__all__ = ['checks']


def checks() -> tuple[Callable[[model.ParsedLine], None], ...]:
    return tuple()
