Welcome to PyShotter's documentation!
=====================================

|PyPI Version|
|PyPI Status|
|PyPI Python Versions|
|GitHub Build Status|
|GitHub License|

.. code-block:: python

    from pyshotter import pyshotter

    # The simplest use, save a screenshot of the 1st monitor
    with pyshotter() as sct:
        sct.shot()


**PyShotter: Smart, annotated, and shareable screenshots for Python.**

An ultra-fast cross-platform screenshot library that makes it easy to capture, annotate, and share screenshots from your Python code.

**Smart Features:**
- **🔍 Smart Detection** - Automatically detect code regions and windows
- **📝 OCR Text Extraction** - Extract text from screenshots using Tesseract
- **🖥️ Window Recognition** - Identify application windows intelligently

**Rich Annotation:**
- **📝 Text Annotations** - Add text with custom fonts and colors
- **🔲 Shape Drawing** - Rectangles, circles, arrows, and highlights
- **🎯 Smart Highlighting** - Semi-transparent overlays for emphasis
- **⚡ Quick Markup** - One-line annotation commands

**Easy Sharing:**
- **📋 Clipboard Copy** - Copy screenshots directly to clipboard
- **🔗 Shareable Links** - Generate instant shareable URLs
- **☁️ Cloud Upload** - Upload to cloud services with metadata
- **📱 Cross-Platform** - Works on Windows, macOS, and Linux

**Advanced Features:**
- **🔒 Sensitive Data Redaction** - Automatically blur emails, phones, credit cards
- **🖥️ Multi-Monitor Panorama** - Stitch all monitors into one panoramic image
- **🔄 Change Detection** - Highlight changes between screenshots
- **⌨️ Customizable Hotkeys** - Set global hotkeys for screenshots
- **📚 Screenshot History & Search** - Searchable history with metadata and OCR

**Technical Highlights:**
- **Python 3.9+**, :pep:`8` compliant, thread-safe;
- Integrates well with PIL, Numpy, and OpenCV;
- Perfect for AI, Computer Vision, and automation;
- Get the `source code on GitHub <https://github.com/utachicodes/pyshotter>`_;
- Learn with a `bunch of examples <https://pyshotter.readthedocs.io/examples.html>`_;
- You can `report a bug <https://github.com/utachicodes/pyshotter/issues>`_;
- Need some help? Use the tag *pyshotter* on `Stack Overflow <https://stackoverflow.com/questions/tagged/pyshotter>`_;

+-------------------------+
|         Content         |
+-------------------------+
|.. toctree::             |
|   :maxdepth: 1          |
|                         |
|   installation          |
|   usage                 |
|   examples              |
|   support               |
|   api                   |
|   developers            |
|   where                 |
+-------------------------+

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. |PyPI Version| image:: https://img.shields.io/pypi/v/pyshotter.svg
   :target: https://pypi.python.org/pypi/pyshotter/
.. |PyPI Status| image:: https://img.shields.io/pypi/status/pyshotter.svg
   :target: https://pypi.python.org/pypi/pyshotter/
.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/pyshotter.svg
   :target: https://pypi.python.org/pypi/pyshotter/
.. |Github Build Status| image:: https://github.com/utachicodes/pyshotter/actions/workflows/tests.yml/badge.svg?branch=main
   :target: https://github.com/utachicodes/pyshotter/actions/workflows/tests.yml
.. |GitHub License| image:: https://img.shields.io/github/license/utachicodes/pyshotter.svg
   :target: https://github.com/utachicodes/pyshotter/blob/main/LICENSE.txt
