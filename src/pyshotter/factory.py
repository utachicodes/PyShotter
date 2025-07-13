"""This is part of the PyShotter Python's module.
Source: https://github.com/utachicodes/pyshotter.
"""

import platform
from typing import Any

from pyshotter.base import MSSBase
from pyshotter.exception import ScreenShotError


def pyshotter(**kwargs: Any) -> MSSBase:
    """Factory returning a proper PyShotter class instance.

    It detects the platform we are running on
    and chooses the most adapted pyshotter_class to take
    screenshots.

    It then proxies its arguments to the class for
    instantiation.
    """
    os_ = platform.system().lower()

    if os_ == "darwin":
        from pyshotter import darwin

        return darwin.MSS(**kwargs)

    if os_ == "linux":
        from pyshotter import linux

        return linux.MSS(**kwargs)

    if os_ == "windows":
        from pyshotter import windows

        return windows.MSS(**kwargs)

    msg = f"System {os_!r} not (yet?) implemented."
    raise ScreenShotError(msg)
