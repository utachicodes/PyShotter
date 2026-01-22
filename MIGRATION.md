# PyShotter v1.1 Migration Guide

This guide helps you upgrade from PyShotter v1.0 to v1.1.

## Breaking Changes

### 1. Import Changes

**v1.x:**
```python
from pyshotter import pyshotter
```

**v2.0:** (No change, backward compatible)
```python
from pyshotter import pyshotter
```

### 2. New Optional Dependencies

v2.0 introduces new feature groups that require additional dependencies:

```bash
# All features
pip install pyshotter[full]

# Individual features
pip install pyshotter[recording]  # Screen recording
pip install pyshotter[gui]        # GUI application
pip install pyshotter[ai]         # AI redaction & face blur
pip install pyshotter[config]     # Configuration management
pip install pyshotter[cli]        # Rich CLI output
```

### 3. CLI Changes

The CLI now has many more options:

**New Flags:**
- `--ocr` - Extract text
- `--redact` - Redact sensitive data
- `--beautify` - Beautify code screenshots
- `--record` - Record screen
- `--json` - JSON output

**Example:**
```bash
# v1.x
pyshotter -m 1 -o screenshot.png

# v2.0 (backward compatible + new features)
pyshotter -m 1 -o screenshot.png --beautify --theme dracula
```

## New Features

### 1. Code Beautification

```python
from pyshotter.beautifier import CodeBeautifierFeature

beautifier = CodeBeautifierFeature(theme='dracula')
beautified = beautifier.beautify(screenshot)
```

### 2. Screen Recording

```python
from pyshotter.recording import ScreenRecordingFeature

recorder = ScreenRecordingFeature(fps=30, format='gif')
output = recorder.record(duration=10, output='recording.gif')
```

### 3. AI-Powered Redaction

```python
from pyshotter.ai_features import EnhancedRedactionFeature

redactor = EnhancedRedactionFeature(mode='blur')
redacted = redactor.redact_with_template(screenshot, 'gdpr')
```

### 4. Face Blurring

```python
from pyshotter.ai_features import FaceBlurFeature

face_blur = FaceBlurFeature()
blurred = face_blur.blur_faces(screenshot)
```

### 5. GUI Application

```bash
# Launch GUI
pyshotter-gui
```

## Configuration

v2.0 introduces configuration file support:

**Location:** `~/.pyshotter/config.yml`

**Example:**
```yaml
general:
  default_output_dir: ~/Screenshots
  log_level: INFO

beautifier:
  default_theme: dracula
  shadow_opacity: 0.5

recording:
  default_fps: 30
  default_format: gif
```

## Deprecations

None - v1.1 is fully backward compatible with v1.0 for core screenshot functionality.

## Upgrade Checklist

- [ ] Install v1.1: `pip install --upgrade pyshotter`
- [ ] Install optional dependencies for features you need
- [ ] Update CLI scripts if using new flags
- [ ] Review configuration options in `~/.pyshotter/config.yml`
- [ ] Test your existing code (should work without changes)

## Getting Help

- Documentation: https://pyshotter.readthedocs.io
- Issues: https://github.com/utachicodes/pyshotter/issues
- Examples: See `examples/` directory
