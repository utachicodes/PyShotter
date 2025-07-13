"""PyShotter: Smart, annotated, and shareable screenshots for Python.

Features:
- Smart detection of code regions and windows
- Rich annotation tools (text, shapes, highlights)
- Easy sharing (clipboard, links, cloud)
- OCR Text Extraction
- Sensitive Data Redaction
- Multi-Monitor Panorama
- Change Detection
- Customizable Hotkeys
- Screenshot History & Search

See: https://pyshotter.readthedocs.io
"""

from .exception import ScreenShotError
from .factory import pyshotter
from .features import (
    AnnotationFeature,
    SharingFeature,
    SmartDetectionFeature,
    OCRFeature,
    RedactionFeature,
    PanoramaFeature,
    ChangeDetectionFeature,
    HotkeyManager,
    ScreenshotHistory,
)

__version__ = "1.0.0"
__author__ = "Abdoullah Ndao"
__email__ = "abdoullahaljersi@gmail.com"
__date__ = "2024"
__copyright__ = "Copyright (c) 2024-2025, Abdoullah Ndao"

__all__ = (
    "ScreenShotError",
    "pyshotter",
    "AnnotationFeature",
    "SharingFeature", 
    "SmartDetectionFeature",
    "OCRFeature",
    "RedactionFeature", 
    "PanoramaFeature",
    "ChangeDetectionFeature",
    "HotkeyManager",
    "ScreenshotHistory",
)
