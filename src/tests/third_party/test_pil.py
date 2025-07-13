"""This is part of the PyShotter Python's module.
Source: https://github.com/utachicodes/pyshotter.
"""

import os
import sys

import PIL.Image
import pytest

from pyshotter import pyshotter


def test_pil():
    """Test that PIL can open our PNGs."""
    with pyshotter(display=os.getenv("DISPLAY")) as sct:
        # PIL can open our PNGs
        sct_img = sct.grab(sct.monitors[0])
        img = PIL.Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        assert img.size == sct_img.size
        assert img.mode == "RGB"

        # PIL can open our PNGs with cursor
        sct_img = sct.grab(sct.monitors[0])
        img = PIL.Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        assert img.size == sct_img.size
        assert img.mode == "RGB"

        # PIL can open our PNGs with cursor
        sct_img = sct.grab(sct.monitors[0])
        img = PIL.Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        assert img.size == sct_img.size
        assert img.mode == "RGB"
