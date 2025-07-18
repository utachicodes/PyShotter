"""This is part of the MSS Python's module.
Source: https://github.com/utachicodes/pyshotter.

2018-03-19.

Maximum screenshots in 1 second by computing BGRA raw values to RGB.


GNU/Linux
  pil_frombytes     139
  mss_rgb           119
  pil_frombytes_rgb 51
  numpy_flip        31
  numpy_slice       29

macOS
  pil_frombytes     209
  mss_rgb           174
  pil_frombytes_rgb 113
  numpy_flip        39
  numpy_slice       36

Windows
  pil_frombytes     81
  mss_rgb           66
  pil_frombytes_rgb 42
  numpy_flip        25
  numpy_slice       22
"""

import time

import numpy as np
from PIL import Image

import mss
from mss.screenshot import ScreenShot


def mss_rgb(im: ScreenShot) -> bytes:
    return im.rgb


def numpy_flip(im: ScreenShot) -> bytes:
    frame = np.array(im, dtype=np.uint8)
    return np.flip(frame[:, :, :3], 2).tobytes()


def numpy_slice(im: ScreenShot) -> bytes:
    return np.array(im, dtype=np.uint8)[..., [2, 1, 0]].tobytes()


def pil_frombytes_rgb(im: ScreenShot) -> bytes:
    return Image.frombytes("RGB", im.size, im.rgb).tobytes()


def pil_frombytes(im: ScreenShot) -> bytes:
    return Image.frombytes("RGB", im.size, im.bgra, "raw", "BGRX").tobytes()


def benchmark() -> None:
    with mss.mss() as sct:
        im = sct.grab(sct.monitors[0])
        for func in (
            pil_frombytes,
            mss_rgb,
            pil_frombytes_rgb,
            numpy_flip,
            numpy_slice,
        ):
            count = 0
            start = time.time()
            while (time.time() - start) <= 1:
                func(im)
                im._ScreenShot__rgb = None  # type: ignore[attr-defined]
                count += 1
            print(func.__name__.ljust(17), count)


benchmark()
