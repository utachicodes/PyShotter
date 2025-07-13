"""This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss.
"""

import platform
import tarfile
from subprocess import STDOUT, check_call, check_output
from zipfile import ZipFile

import pytest

from pyshotter import __version__

if platform.system().lower() != "linux":
    pytestmark = pytest.mark.skip

pytest.importorskip("build")
pytest.importorskip("twine")

SDIST = "python -m build --sdist".split()
WHEEL = "python -m build --wheel".split()
CHECK = "twine check --strict".split()


def test_sdist() -> None:
    output = check_output(SDIST, stderr=STDOUT, text=True)
    file = f"pyshotter-{__version__}.tar.gz"
    assert f"Successfully built {file}" in output
    assert "warning" not in output.lower()

    check_call([*CHECK, f"dist/{file}"])

    with tarfile.open(f"dist/{file}", mode="r:gz") as fh:
        files = sorted(fh.getnames())

    assert files == [
        f"pyshotter-{__version__}/.gitignore",
        f"pyshotter-{__version__}/CHANGELOG.md",
        f"pyshotter-{__version__}/CHANGES.md",
        f"pyshotter-{__version__}/CONTRIBUTORS.md",
        f"pyshotter-{__version__}/LICENSE.txt",
        f"pyshotter-{__version__}/PKG-INFO",
        f"pyshotter-{__version__}/README.md",
        f"pyshotter-{__version__}/docs/source/api.rst",
        f"pyshotter-{__version__}/docs/source/conf.py",
        f"pyshotter-{__version__}/docs/source/developers.rst",
        f"pyshotter-{__version__}/docs/source/examples.rst",
        f"pyshotter-{__version__}/docs/source/examples/callback.py",
        f"pyshotter-{__version__}/docs/source/examples/custom_cls_image.py",
        f"pyshotter-{__version__}/docs/source/examples/fps.py",
        f"pyshotter-{__version__}/docs/source/examples/fps_multiprocessing.py",
        f"pyshotter-{__version__}/docs/source/examples/from_pil_tuple.py",
        f"pyshotter-{__version__}/docs/source/examples/linux_display_keyword.py",
        f"pyshotter-{__version__}/docs/source/examples/opencv_numpy.py",
        f"pyshotter-{__version__}/docs/source/examples/part_of_screen.py",
        f"pyshotter-{__version__}/docs/source/examples/part_of_screen_monitor_2.py",
        f"pyshotter-{__version__}/docs/source/examples/pil.py",
        f"pyshotter-{__version__}/docs/source/examples/pil_pixels.py",
        f"pyshotter-{__version__}/docs/source/index.rst",
        f"pyshotter-{__version__}/docs/source/installation.rst",
        f"pyshotter-{__version__}/docs/source/support.rst",
        f"pyshotter-{__version__}/docs/source/usage.rst",
        f"pyshotter-{__version__}/docs/source/where.rst",
        f"pyshotter-{__version__}/pyproject.toml",
        f"pyshotter-{__version__}/src/pyshotter/__init__.py",
        f"pyshotter-{__version__}/src/pyshotter/__main__.py",
        f"pyshotter-{__version__}/src/pyshotter/base.py",
        f"pyshotter-{__version__}/src/pyshotter/darwin.py",
        f"pyshotter-{__version__}/src/pyshotter/exception.py",
        f"pyshotter-{__version__}/src/pyshotter/factory.py",
        f"pyshotter-{__version__}/src/pyshotter/linux.py",
        f"pyshotter-{__version__}/src/pyshotter/models.py",
        f"pyshotter-{__version__}/src/pyshotter/py.typed",
        f"pyshotter-{__version__}/src/pyshotter/screenshot.py",
        f"pyshotter-{__version__}/src/pyshotter/tools.py",
        f"pyshotter-{__version__}/src/pyshotter/windows.py",
        f"pyshotter-{__version__}/src/tests/__init__.py",
        f"pyshotter-{__version__}/src/tests/bench_bgra2rgb.py",
        f"pyshotter-{__version__}/src/tests/bench_general.py",
        f"pyshotter-{__version__}/src/tests/conftest.py",
        f"pyshotter-{__version__}/src/tests/res/monitor-1024x768.raw.zip",
        f"pyshotter-{__version__}/src/tests/test_bgra_to_rgb.py",
        f"pyshotter-{__version__}/src/tests/test_cls_image.py",
        f"pyshotter-{__version__}/src/tests/test_find_monitors.py",
        f"pyshotter-{__version__}/src/tests/test_get_pixels.py",
        f"pyshotter-{__version__}/src/tests/test_gnu_linux.py",
        f"pyshotter-{__version__}/src/tests/test_implementation.py",
        f"pyshotter-{__version__}/src/tests/test_issue_220.py",
        f"pyshotter-{__version__}/src/tests/test_leaks.py",
        f"pyshotter-{__version__}/src/tests/test_macos.py",
        f"pyshotter-{__version__}/src/tests/test_save.py",
        f"pyshotter-{__version__}/src/tests/test_setup.py",
        f"pyshotter-{__version__}/src/tests/test_tools.py",
        f"pyshotter-{__version__}/src/tests/test_windows.py",
        f"pyshotter-{__version__}/src/tests/third_party/__init__.py",
        f"pyshotter-{__version__}/src/tests/third_party/test_numpy.py",
        f"pyshotter-{__version__}/src/tests/third_party/test_pil.py",
    ]


def test_wheel() -> None:
    output = check_output(WHEEL, stderr=STDOUT, text=True)
    file = f"pyshotter-{__version__}-py3-none-any.whl"
    assert f"Successfully built {file}" in output
    assert "warning" not in output.lower()

    check_call([*CHECK, f"dist/{file}"])

    with ZipFile(f"dist/{file}") as fh:
        files = sorted(fh.namelist())

    assert files == [
        f"pyshotter-{__version__}.dist-info/METADATA",
        f"pyshotter-{__version__}.dist-info/RECORD",
        f"pyshotter-{__version__}.dist-info/WHEEL",
        f"pyshotter-{__version__}.dist-info/entry_points.txt",
        f"pyshotter-{__version__}.dist-info/licenses/LICENSE.txt",
        "pyshotter/__init__.py",
        "pyshotter/__main__.py",
        "pyshotter/base.py",
        "pyshotter/darwin.py",
        "pyshotter/exception.py",
        "pyshotter/factory.py",
        "pyshotter/linux.py",
        "pyshotter/models.py",
        "pyshotter/py.typed",
        "pyshotter/screenshot.py",
        "pyshotter/tools.py",
        "pyshotter/windows.py",
    ]
