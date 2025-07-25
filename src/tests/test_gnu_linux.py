"""This is part of the MSS Python's module.
Source: https://github.com/utachicodes/pyshotter.
"""

import platform
from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest

import mss
import mss.linux
from mss.base import MSSBase
from mss.exception import ScreenShotError

pyvirtualdisplay = pytest.importorskip("pyvirtualdisplay")

PYPY = platform.python_implementation() == "PyPy"

WIDTH = 200
HEIGHT = 200
DEPTH = 24


@pytest.fixture
def display() -> Generator:
    with pyvirtualdisplay.Display(size=(WIDTH, HEIGHT), color_depth=DEPTH) as vdisplay:
        yield vdisplay.new_display_var


@pytest.mark.skipif(PYPY, reason="Failure on PyPy")
def test_factory_systems(monkeypatch: pytest.MonkeyPatch) -> None:
    """Here, we are testing all systems.

    Too hard to maintain the test for all platforms,
    so test only on GNU/Linux.
    """
    # GNU/Linux
    monkeypatch.setattr(platform, "system", lambda: "LINUX")
    with mss.mss() as sct:
        assert isinstance(sct, MSSBase)
    monkeypatch.undo()

    # macOS
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    # ValueError on macOS Big Sur
    with pytest.raises((ScreenShotError, ValueError)), mss.mss():
        pass
    monkeypatch.undo()

    # Windows
    monkeypatch.setattr(platform, "system", lambda: "wInDoWs")
    with pytest.raises(ImportError, match="cannot import name 'WINFUNCTYPE'"), mss.mss():
        pass


def test_arg_display(display: str, monkeypatch: pytest.MonkeyPatch) -> None:
    # Good value
    with mss.mss(display=display):
        pass

    # Bad `display` (missing ":" in front of the number)
    with pytest.raises(ScreenShotError), mss.mss(display="0"):
        pass

    # Invalid `display` that is not trivially distinguishable.
    with pytest.raises(ScreenShotError), mss.mss(display=":INVALID"):
        pass

    # No `DISPLAY` in envars
    monkeypatch.delenv("DISPLAY")
    with pytest.raises(ScreenShotError), mss.mss():
        pass


@pytest.mark.skipif(PYPY, reason="Failure on PyPy")
def test_bad_display_structure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mss.linux, "Display", lambda: None)
    with pytest.raises(TypeError), mss.mss():
        pass


@patch("mss.linux._X11", new=None)
def test_no_xlib_library() -> None:
    with pytest.raises(ScreenShotError), mss.mss():
        pass


@patch("mss.linux._XRANDR", new=None)
def test_no_xrandr_extension() -> None:
    with pytest.raises(ScreenShotError), mss.mss():
        pass


@patch("mss.linux.MSS._is_extension_enabled", new=Mock(return_value=False))
def test_xrandr_extension_exists_but_is_not_enabled(display: str) -> None:
    with pytest.raises(ScreenShotError), mss.mss(display=display):
        pass


def test_unsupported_depth() -> None:
    with (
        pyvirtualdisplay.Display(size=(WIDTH, HEIGHT), color_depth=8) as vdisplay,
        pytest.raises(ScreenShotError),
        mss.mss(display=vdisplay.new_display_var) as sct,
    ):
        sct.grab(sct.monitors[1])


def test_region_out_of_monitor_bounds(display: str) -> None:
    monitor = {"left": -30, "top": 0, "width": WIDTH, "height": HEIGHT}

    assert not mss.linux._ERROR

    with mss.mss(display=display) as sct:
        with pytest.raises(ScreenShotError) as exc:
            sct.grab(monitor)

        assert str(exc.value)

        details = exc.value.details
        assert details
        assert isinstance(details, dict)
        assert isinstance(details["error"], str)
        assert not mss.linux._ERROR

    assert not mss.linux._ERROR


def test__is_extension_enabled_unknown_name(display: str) -> None:
    with mss.mss(display=display) as sct:
        assert isinstance(sct, mss.linux.MSS)  # For Mypy
        assert not sct._is_extension_enabled("NOEXT")


def test_missing_fast_function_for_monitor_details_retrieval(display: str) -> None:
    with mss.mss(display=display) as sct:
        assert isinstance(sct, mss.linux.MSS)  # For Mypy
        assert hasattr(sct.xrandr, "XRRGetScreenResourcesCurrent")
        screenshot_with_fast_fn = sct.grab(sct.monitors[1])

    assert set(screenshot_with_fast_fn.rgb) == {0}

    with mss.mss(display=display) as sct:
        assert isinstance(sct, mss.linux.MSS)  # For Mypy
        assert hasattr(sct.xrandr, "XRRGetScreenResourcesCurrent")
        del sct.xrandr.XRRGetScreenResourcesCurrent
        screenshot_with_slow_fn = sct.grab(sct.monitors[1])

    assert set(screenshot_with_slow_fn.rgb) == {0}


def test_with_cursor(display: str) -> None:
    with mss.mss(display=display) as sct:
        assert not hasattr(sct, "xfixes")
        assert not sct.with_cursor
        screenshot_without_cursor = sct.grab(sct.monitors[1])

    # 1 color: black
    assert set(screenshot_without_cursor.rgb) == {0}

    with mss.mss(display=display, with_cursor=True) as sct:
        assert hasattr(sct, "xfixes")
        assert sct.with_cursor
        screenshot_with_cursor = sct.grab(sct.monitors[1])

    # 2 colors: black & white (default cursor is a white cross)
    assert set(screenshot_with_cursor.rgb) == {0, 255}


@patch("mss.linux._XFIXES", new=None)
def test_with_cursor_but_not_xfixes_extension_found(display: str) -> None:
    with mss.mss(display=display, with_cursor=True) as sct:
        assert not hasattr(sct, "xfixes")
        assert not sct.with_cursor


def test_with_cursor_failure(display: str) -> None:
    with mss.mss(display=display, with_cursor=True) as sct:
        assert isinstance(sct, mss.linux.MSS)  # For Mypy
        with (
            patch.object(sct.xfixes, "XFixesGetCursorImage", return_value=None),
            pytest.raises(ScreenShotError),
        ):
            sct.grab(sct.monitors[1])
