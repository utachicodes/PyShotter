=====
Usage
=====

Import
======

So PyShotter can be used as simply as::

    from pyshotter import pyshotter

Or import the good one based on your operating system::

    # GNU/Linux
    from pyshotter.linux import MSS as pyshotter

    # macOS
    from pyshotter.darwin import MSS as pyshotter

    # Microsoft Windows
    from pyshotter.windows import MSS as pyshotter


Instance
========

So the module can be used as simply as::

    with pyshotter() as sct:
        # ...

Intensive Use
=============

If you plan to integrate PyShotter inside your own module or software, pay attention to using it wisely.

This is a bad usage::

    for _ in range(100):
        with pyshotter() as sct:
            sct.shot()

This is a much better usage, memory efficient::

    with pyshotter() as sct:
        for _ in range(100):
            sct.shot()

Also, it is a good thing to save the PyShotter instance inside an attribute of your class and calling it when needed.


GNU/Linux
---------

On GNU/Linux, you can specify which display to use (useful for distant screenshots via SSH)::

    with pyshotter(display=":0.0") as sct:
        # ...

A more specific example (only valid on GNU/Linux):

.. literalinclude:: examples/linux_display_keyword.py
    :lines: 9-


Command Line
============

You can use ``pyshotter`` via the CLI::

    pyshotter --help

Or via direct call from Python::

    $ python -m pyshotter --help
    usage: __main__.py [-h] [-c COORDINATES] [-l {0,1,2,3,4,5,6,7,8,9}]
                    [-m MONITOR] [-o OUTPUT] [-q] [-v] [--with-cursor]

    options:
    -h, --help            show this help message and exit
    -c COORDINATES, --coordinates COORDINATES
                          the part of the screen to capture: top, left, width, height
    -l {0,1,2,3,4,5,6,7,8,9}, --level {0,1,2,3,4,5,6,7,8,9}
                          the PNG compression level
    -m MONITOR, --monitor MONITOR
                          the monitor to screenshot
    -o OUTPUT, --output OUTPUT
                          the output file name
    --with-cursor         include the cursor
    -q, --quiet           do not print created files
    -v, --version         show program's version number and exit

.. versionadded:: 3.1.1

.. versionadded:: 8.0.0
    ``--with-cursor`` to include the cursor in screenshots.
