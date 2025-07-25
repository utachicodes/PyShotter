"""This is part of the PyShotter Python's module.
Source: https://github.com/utachicodes/pyshotter.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mss.exception import ScreenShotError
from mss.models import Monitor, Pixel, Pixels, Pos, Size

if TYPE_CHECKING:  # pragma: nocover
    from collections.abc import Iterator


class ScreenShot:
    """Screenshot object.

    .. note::

        A better name would have  been *Image*, but to prevent collisions
        with PIL.Image, it has been decided to use *ScreenShot*.
    """

    __slots__ = {"__pixels", "__rgb", "pos", "raw", "size"}

    def __init__(self, data: bytearray, monitor: Monitor, /, *, size: Size | None = None) -> None:
        self.__pixels: Pixels | None = None
        self.__rgb: bytes | None = None

        #: Bytearray of the raw BGRA pixels retrieved by ctypes
        #: OS independent implementations.
        self.raw = data

        #: NamedTuple of the screenshot coordinates.
        self.pos = Pos(monitor["left"], monitor["top"])

        #: NamedTuple of the screenshot size.
        self.size = Size(monitor["width"], monitor["height"]) if size is None else size

    def __repr__(self) -> str:
        return f"<{type(self).__name__} pos={self.left},{self.top} size={self.width}x{self.height}>"

    @property
    def __array_interface__(self) -> dict[str, Any]:
        """Numpy array interface support.
        It uses raw data in BGRA form.

        See https://docs.scipy.org/doc/numpy/reference/arrays.interface.html
        """
        return {
            "version": 3,
            "shape": (self.height, self.width, 4),
            "typestr": "|u1",
            "data": self.raw,
        }

    @classmethod
    def from_size(cls: type[ScreenShot], data: bytearray, width: int, height: int, /) -> ScreenShot:
        """Instantiate a new class given only screenshot's data and size."""
        monitor = {"left": 0, "top": 0, "width": width, "height": height}
        return cls(data, monitor)

    @property
    def bgra(self) -> bytes:
        """BGRA values from the BGRA raw pixels."""
        return bytes(self.raw)

    @property
    def height(self) -> int:
        """Convenient accessor to the height size."""
        return self.size.height

    @property
    def left(self) -> int:
        """Convenient accessor to the left position."""
        return self.pos.left

    @property
    def pixels(self) -> Pixels:
        """:return list: RGB tuples."""
        if not self.__pixels:
            rgb_tuples: Iterator[Pixel] = zip(self.raw[2::4], self.raw[1::4], self.raw[::4])
            self.__pixels = list(zip(*[iter(rgb_tuples)] * self.width))

        return self.__pixels

    @property
    def rgb(self) -> bytes:
        """Compute RGB values from the BGRA raw pixels.

        :return bytes: RGB pixels.
        """
        if not self.__rgb:
            rgb = bytearray(self.height * self.width * 3)
            raw = self.raw
            rgb[::3] = raw[2::4]
            rgb[1::3] = raw[1::4]
            rgb[2::3] = raw[::4]
            self.__rgb = bytes(rgb)

        return self.__rgb

    @property
    def top(self) -> int:
        """Convenient accessor to the top position."""
        return self.pos.top

    @property
    def width(self) -> int:
        """Convenient accessor to the width size."""
        return self.size.width

    def pixel(self, coord_x: int, coord_y: int) -> Pixel:
        """Returns the pixel value at a given position.

        :param int coord_x: The x coordinate.
        :param int coord_y: The y coordinate.
        :return tuple: The pixel value as (R, G, B).
        """
        try:
            return self.pixels[coord_y][coord_x]
        except IndexError as exc:
            msg = f"Pixel location ({coord_x}, {coord_y}) is out of range."
            raise ScreenShotError(msg) from exc
