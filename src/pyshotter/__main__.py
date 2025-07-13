"""This is part of the PyShotter Python's module.
Source: https://github.com/utachicodes/pyshotter.
"""

import os.path
import sys
from argparse import ArgumentParser

from pyshotter import __version__
from pyshotter.exception import ScreenShotError
from pyshotter.factory import pyshotter
from pyshotter.tools import to_png


def main(*args: str) -> int:
    """Main logic."""
    cli_args = ArgumentParser(prog="pyshotter")
    cli_args.add_argument(
        "-c",
        "--coordinates",
        default="",
        type=str,
        help="the part of the screen to capture: top, left, width, height",
    )
    cli_args.add_argument(
        "-l",
        "--level",
        default=6,
        type=int,
        choices=list(range(10)),
        help="the PNG compression level",
    )
    cli_args.add_argument("-m", "--monitor", default=0, type=int, help="the monitor to screenshot")
    cli_args.add_argument("-o", "--output", default="monitor-{mon}.png", help="the output file name")
    cli_args.add_argument("--with-cursor", default=False, action="store_true", help="include the cursor")
    cli_args.add_argument(
        "-q",
        "--quiet",
        default=False,
        action="store_true",
        help="do not print created files",
    )
    cli_args.add_argument("-v", "--version", action="version", version=__version__)

    options = cli_args.parse_args(args or None)
    kwargs = {"mon": options.monitor, "output": options.output}
    if options.coordinates:
        try:
            top, left, width, height = options.coordinates.split(",")
        except ValueError:
            print("Coordinates syntax: top, left, width, height")
            return 2

        kwargs["mon"] = {
            "top": int(top),
            "left": int(left),
            "width": int(width),
            "height": int(height),
        }
        if options.output == "monitor-{mon}.png":
            kwargs["output"] = "sct-{top}x{left}_{width}x{height}.png"

    try:
        with pyshotter(with_cursor=options.with_cursor) as sct:
            if options.coordinates:
                output = kwargs["output"].format(**kwargs["mon"])
                sct_img = sct.grab(kwargs["mon"])
                to_png(sct_img.rgb, sct_img.size, level=options.level, output=output)
                if not options.quiet:
                    print(os.path.realpath(output))
            else:
                for file_name in sct.save(**kwargs):
                    if not options.quiet:
                        print(os.path.realpath(file_name))
            return 0
    except ScreenShotError:
        if options.quiet:
            return 1
        raise


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
