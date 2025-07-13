# PyShotter

[![PyPI version](https://badge.fury.io/py/pyshotter.svg)](https://badge.fury.io/py/pyshotter)
[![Tests workflow](https://github.com/utachicodes/pyshotter/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/utachicodes/pyshotter/actions/workflows/tests.yml)
[![Downloads](https://static.pepy.tech/personalized-badge/pyshotter?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/pyshotter)

> [!TIP]
> **PyShotter** - Smart, annotated, and shareable screenshots for Python.

```python
from pyshotter import pyshotter

# The simplest use, save a screenshot of the 1st monitor
with pyshotter() as sct:
    sct.shot()
```

An ultra-fast cross-platform screenshot library that makes it easy to capture, annotate, and share screenshots from your Python code.

## Features

### Smart Detection
- **Code Region Detection** - Automatically detect code blocks and windows using computer vision
- **Window Detection** - Smart identification of application windows and UI elements
- **OCR Text Extraction** - Extract text from screenshots using Tesseract OCR engine
- **Content Analysis** - Intelligent analysis of screenshot content for better processing

### Rich Annotation
- **Text Annotations** - Add text with custom fonts, sizes, and colors
- **Shape Drawing** - Rectangles, circles, arrows, and custom geometric shapes
- **Smart Highlighting** - Semi-transparent overlays for emphasis and focus
- **Quick Markup** - One-line annotation commands for rapid screenshot editing
- **Layer Management** - Multiple annotation layers with proper compositing

### Easy Sharing
- **Clipboard Copy** - Copy screenshots directly to system clipboard
- **Shareable Links** - Generate instant shareable URLs for screenshots
- **Cloud Upload** - Upload to cloud services with embedded metadata
- **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux
- **Metadata Support** - Rich metadata embedding for better organization

### Advanced Features
- **Sensitive Data Redaction** - Automatically blur emails, phone numbers, credit cards, and SSNs
- **Multi-Monitor Panorama** - Stitch all monitors into one panoramic image
- **Change Detection** - Highlight changes between screenshots with configurable sensitivity
- **Customizable Hotkeys** - Set global hotkeys for screenshot capture and annotation
- **Screenshot History & Search** - Searchable history with metadata and OCR text indexing
- **High Performance** - Optimized for speed and efficiency using ctypes
- **Thread-Safe** - Safe for multi-threaded applications

## Installation

### Recommended Installation

```shell
python -m pip install -U --user pyshotter
```

### Optional Dependencies

For enhanced features, install additional dependencies:

```shell
# For OCR and advanced image processing
python -m pip install pyshotter[ocr]

# For annotation features
python -m pip install pyshotter[annotation]

# For sharing features
python -m pip install pyshotter[sharing]

# For cloud upload capabilities
python -m pip install pyshotter[cloud]

# For development
python -m pip install pyshotter[dev]
```

## Quick Start

### Basic Screenshot Capture

```python
from pyshotter import pyshotter

# Take a screenshot of the first monitor
with pyshotter() as sct:
    sct.shot()

# Take screenshots of all monitors
with pyshotter() as sct:
    for i, monitor in enumerate(sct.monitors):
        sct.shot(mon=i)
```

### Smart Detection and Analysis

```python
from pyshotter import pyshotter, SmartDetectionFeature, OCRFeature

with pyshotter() as sct:
    screenshot = sct.grab(sct.monitors[0])
    
    # Detect code regions and windows
    detector = SmartDetectionFeature()
    code_regions = detector.detect_code_regions(screenshot)
    windows = detector.detect_windows(screenshot)
    
    print(f"Found {len(code_regions)} code regions")
    print(f"Found {len(windows)} windows")
    
    # Extract text using OCR
    ocr = OCRFeature()
    text = ocr.extract_text(screenshot)
    print(f"Extracted text: {text}")
```

### Rich Annotation

```python
from pyshotter import pyshotter, AnnotationFeature

with pyshotter() as sct:
    screenshot = sct.grab(sct.monitors[0])
    
    # Initialize annotation
    annotator = AnnotationFeature()
    
    # Add text annotation
    annotated = annotator.add_text(
        screenshot, 
        "Important Code Here!", 
        (100, 100),
        font_size=24,
        color=(255, 0, 0)  # Red text
    )
    
    # Add rectangle around a region
    annotated = annotator.add_rectangle(
        annotated,
        (50, 50),      # Top-left corner
        (400, 200),    # Bottom-right corner
        color=(0, 255, 0),  # Green rectangle
        thickness=3
    )
    
    # Add arrow pointing to something
    annotated = annotator.add_arrow(
        annotated,
        (150, 150),    # Start point
        (300, 100),    # End point
        color=(0, 0, 255),  # Blue arrow
        thickness=2
    )
    
    # Add circle highlight
    annotated = annotator.add_circle(
        annotated,
        (200, 150),    # Center point
        30,             # Radius
        color=(255, 255, 0),  # Yellow circle
        thickness=2
    )
    
    # Add highlight overlay
    annotated = annotator.add_highlight(
        annotated,
        (100, 100, 200, 100),  # (x, y, width, height)
        color=(255, 255, 0),    # Yellow highlight
        alpha=0.3               # 30% transparency
    )
    
    # Save the annotated screenshot
    annotated.save("annotated_screenshot.png")
```

### Easy Sharing

```python
from pyshotter import pyshotter, SharingFeature

with pyshotter() as sct:
    screenshot = sct.grab(sct.monitors[0])
    
    # Initialize sharing
    sharer = SharingFeature()
    
    # Copy to clipboard
    if sharer.copy_to_clipboard(screenshot):
        print("Screenshot copied to clipboard!")
    
    # Generate shareable link
    link = sharer.generate_shareable_link(screenshot)
    print(f"Shareable link: {link}")
    
    # Save with metadata
    metadata = {
        "title": "My Screenshot",
        "description": "Screenshot taken with PyShotter",
        "tags": ["python", "screenshot", "demo"],
        "author": "Abdoullah Ndao",
        "timestamp": "2024-12-19"
    }
    
    sharer.save_with_metadata(screenshot, "screenshot.png", metadata)
```

### Sensitive Data Redaction

```python
from pyshotter import pyshotter, RedactionFeature

with pyshotter() as sct:
    screenshot = sct.grab(sct.monitors[0])
    
    # Initialize redaction
    redaction = RedactionFeature()
    
    # Redact sensitive data
    clean_screenshot = redaction.redact_sensitive_data(screenshot)
    clean_screenshot.save("clean_screenshot.png")
```

### Multi-Monitor Panorama

```python
from pyshotter import pyshotter, PanoramaFeature

with pyshotter() as sct:
    # Capture all monitors
    screenshots = []
    for monitor in sct.monitors:
        screenshot = sct.grab(monitor)
        screenshots.append(screenshot)
    
    # Create panoramic image
    panorama = PanoramaFeature()
    panoramic_screenshot = panorama.create_panorama(screenshots)
    panoramic_screenshot.save("panorama.png")
```

### Change Detection

```python
import time
from pyshotter import pyshotter, ChangeDetectionFeature

with pyshotter() as sct:
    # Take first screenshot
    previous = sct.grab(sct.monitors[0])
    
    # Wait for changes
    time.sleep(5)
    
    # Take second screenshot
    current = sct.grab(sct.monitors[0])
    
    # Detect changes
    detector = ChangeDetectionFeature()
    changes = detector.detect_changes(current, previous, threshold=0.1)
    changes.save("changes.png")
```

### Screenshot History and Search

```python
from pyshotter import pyshotter, ScreenshotHistory

# Initialize history manager
history = ScreenshotHistory()

with pyshotter() as sct:
    screenshot = sct.grab(sct.monitors[0])
    
    # Add to history with metadata
    screenshot_id = history.add_screenshot(
        screenshot,
        metadata={
            "tags": ["desktop", "work"],
            "window_title": "Example Window",
            "description": "Sample screenshot for demonstration"
        }
    )
    
    # Search history
    results = history.search_history("work")
    for result in results:
        print(f"Found: {result['id']} - {result['timestamp']}")
```

## API Reference

### Core Functions

#### `pyshotter(**kwargs)`
Factory function that returns a platform-specific screenshot instance.

**Parameters:**
- `mon` (int): Monitor index (default: 0)
- `output` (str): Output filename pattern
- `with_cursor` (bool): Include cursor in screenshot
- `compression_level` (int): PNG compression level (0-9)

**Returns:**
- Platform-specific screenshot instance

#### `sct.shot(**kwargs)`
Take a screenshot and save it to a file.

**Parameters:**
- `mon` (int): Monitor index or monitor dict
- `output` (str): Output filename
- `with_cursor` (bool): Include cursor

**Returns:**
- List of saved filenames

#### `sct.grab(monitor)`
Capture a screenshot without saving.

**Parameters:**
- `monitor` (dict): Monitor configuration

**Returns:**
- ScreenShot object

### Smart Detection Features

#### `SmartDetectionFeature.detect_code_regions(screenshot)`
Detect code-like regions in screenshots.

**Parameters:**
- `screenshot` (ScreenShot): Screenshot to analyze

**Returns:**
- List of dictionaries with bounding boxes and confidence scores

#### `SmartDetectionFeature.detect_windows(screenshot)`
Detect application windows in screenshots.

**Parameters:**
- `screenshot` (ScreenShot): Screenshot to analyze

**Returns:**
- List of dictionaries with window bounding boxes

### Annotation Features

#### `AnnotationFeature.add_text(screenshot, text, position, font_size, color)`
Add text annotation to a screenshot.

**Parameters:**
- `screenshot` (ScreenShot): Screenshot to annotate
- `text` (str): Text to add
- `position` (tuple): (x, y) position
- `font_size` (int): Font size
- `color` (tuple): RGB color tuple

**Returns:**
- Annotated ScreenShot object

#### `AnnotationFeature.add_rectangle(screenshot, top_left, bottom_right, color, thickness)`
Add rectangle annotation to a screenshot.

**Parameters:**
- `screenshot` (ScreenShot): Screenshot to annotate
- `top_left` (tuple): Top-left corner (x, y)
- `bottom_right` (tuple): Bottom-right corner (x, y)
- `color` (tuple): RGB color tuple
- `thickness` (int): Line thickness

**Returns:**
- Annotated ScreenShot object

### Sharing Features

#### `SharingFeature.copy_to_clipboard(screenshot)`
Copy screenshot to system clipboard.

**Parameters:**
- `screenshot` (ScreenShot): Screenshot to copy

**Returns:**
- bool: Success status

#### `SharingFeature.generate_shareable_link(screenshot, service)`
Generate a shareable link for the screenshot.

**Parameters:**
- `screenshot` (ScreenShot): Screenshot to share
- `service` (str): Sharing service name

**Returns:**
- str: Shareable URL or None

## Examples

### Basic Usage

```python
from pyshotter import pyshotter

# Simple screenshot
with pyshotter() as sct:
    sct.shot()

# Screenshot with cursor
with pyshotter(with_cursor=True) as sct:
    sct.shot()

# Screenshot of specific monitor
with pyshotter() as sct:
    sct.shot(mon=1)  # Second monitor
```

### Advanced Usage

```python
from pyshotter import pyshotter, AnnotationFeature, SharingFeature

with pyshotter() as sct:
    # Capture screenshot
    screenshot = sct.grab(sct.monitors[0])
    
    # Annotate
    annotator = AnnotationFeature()
    annotated = annotator.add_text(screenshot, "Hello World!", (100, 100))
    annotated = annotator.add_rectangle(annotated, (50, 50), (300, 200))
    
    # Share
    sharer = SharingFeature()
    sharer.copy_to_clipboard(annotated)
    
    # Save
    annotated.save("final_screenshot.png")
```

## Development

### Setup Development Environment

```shell
git clone https://github.com/utachicodes/pyshotter.git
cd pyshotter
python -m pip install -e ".[dev]"
```

### Running Tests

```shell
python -m pytest
```

### Code Quality Checks

```shell
# Format code
ruff format src/

# Lint code
ruff check src/

# Type checking
mypy src/

# Run all checks
ruff check src/ && mypy src/ && python -m pytest
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Guidelines

1. **Code Style**: Follow PEP 8 and use Ruff for formatting
2. **Type Hints**: All functions should have proper type annotations
3. **Documentation**: Add docstrings for all public functions
4. **Tests**: Write tests for new features
5. **Examples**: Update examples when adding new features

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Author

**Abdoullah Ndao** - [GitHub](https://github.com/utachicodes) - abdoullahaljersi@gmail.com

## Acknowledgments

- Built with love for the Python community
- Cross-platform compatibility using ctypes
- Smart features for modern development workflows
- Inspired by the need for better screenshot tools in Python

## Support

- **Documentation**: [https://pyshotter.readthedocs.io](https://pyshotter.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/utachicodes/pyshotter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/utachicodes/pyshotter/discussions)
- **Email**: abdoullahaljersi@gmail.com

---

**PyShotter** - Making screenshots smart, annotated, and shareable!
