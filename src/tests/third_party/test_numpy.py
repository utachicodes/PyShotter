"""This is part of the PyShotter Python's module.
Source: https://github.com/utachicodes/pyshotter.
"""

import os

import numpy
import pytest

from pyshotter import pyshotter


def test_numpy():
    """Test that numpy can handle our images."""
    with pyshotter(display=os.getenv("DISPLAY")) as sct:
        sct_img = sct.grab(sct.monitors[0])
        arr = numpy.array(sct_img)
        assert arr.shape == (sct_img.height, sct_img.width, 3)
