"""This is part of the PyShotter Python's module.
Source: https://github.com/utachicodes/pyshotter.
"""

from typing import Any, NamedTuple

Monitor = dict[str, int]
Monitors = list[Monitor]

Pixel = tuple[int, int, int]
Pixels = list[tuple[Pixel, ...]]

CFunctions = dict[str, tuple[str, list[Any], Any]]


class Pos(NamedTuple):
    left: int
    top: int


class Size(NamedTuple):
    width: int
    height: int
