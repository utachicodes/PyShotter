# Changelog

All notable changes to PyShotter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-02-05

### Added
- **Code Beautifier**: New professional themes: `catppuccin` and `one-dark`.
- **Code Beautifier**: Support for custom image backgrounds.
- **AI Features**: `bulk_redact` method for processing multiple screenshots.
- **AI Features**: `auto_anonymize` helper for one-step PII and face redaction.
- **Screen Recording**: Pause and Resume functionality.
- **Screen Recording**: Watermark overlay support for recorded frames.

## [1.1.0] - 2026-01-22

### 🎉 Feature Release - v1.1

This is a feature-rich update adding many powerful capabilities while maintaining 100% backward compatibility with v1.0.

### Added

#### Core Infrastructure
- **Configuration System** (`config.py`) - YAML/JSON support with pydantic validation, environment variables, hot-reload
- **Logging System** (`logging_config.py`) - Privacy-aware filtering, JSON structured logging, file rotation
- **Enhanced Exceptions** - 8 feature-specific exception classes with recovery hints

#### New Features
- **Code Beautifier** (`beautifier.py`)
  - 7 built-in themes (Dracula, Monokai, Nord, Solarized, GitHub, One Dark Pro, Material)
  - Platform-specific window controls (macOS, Windows, Linux)
  - Gradient backgrounds
  - Drop shadows with multiple blur passes
  - Configurable padding and styling
  
- **Screen Recording** (`recording.py`)
  - GIF and MP4 export
  - 30-60 FPS recording with threaded capture
  - Progress callbacks with ETA
  - Region-specific recording
  - Memory management and disk space checking
  
- **AI-Powered Redaction** (`ai_features.py`)
  - 4 redaction modes: blur, pixelate, block, generate
  - 5 privacy templates (HIPAA/medical, PCI-DSS/financial, government, corporate, GDPR)
  - Custom regex pattern support
  - Face detection and blurring (Haar Cascade + DNN with auto-download)
  
- **Enhanced CLI** (`__main__.py`)
  - 15+ new command-line flags
  - `--ocr` with language and confidence options
  - `--redact` with templates and styles
  - `--beautify` with theme selection
  - `--record` for screen recording
  - `--blur-faces` for privacy
  - `--json` for structured output
  - Rich formatting support
  
- **GUI Application** (`gui.py`)
  - System tray integration
  - Interactive region selection
  - Screenshot history viewer
  - Global hotkeys (platform-specific)
  - Quick actions menu
  - System notifications

#### CI/CD & Testing
- Comprehensive GitHub Actions workflows
  - Multi-platform testing (Ubuntu, macOS, Windows)
  - Python 3.9-3.14 support
  - Security scanning (Bandit, Safety)
  - Coverage reporting (Codecov)
  - Performance benchmarks
  - Automated PyPI releases
  
- **Test Suite**
  - 50+ unit tests
  - Integration tests
  - Performance benchmarks
  - Cross-platform validation

#### Documentation
- Migration guide from v1.0 to v1.1
- 3 comprehensive example scripts
- Updated README with all features
- API documentation improvements

### Changed
- Expanded dependency groups (10 total: ocr, annotation, recording, gui, ai, config, cli, full, dev, tests)
- Enhanced exception handling throughout
- Improved error messages with recovery hints
- Updated to modern Python practices (3.9+)

### Dependencies
New optional dependency groups:
- `recording` - imageio, imageio-ffmpeg
- `gui` - pystray, tkinter
- `ai` - opencv-python, numpy (enhanced)
- `config` - pyyaml, pydantic
- `cli` - rich
- `full` - all features combined

### Installation
```bash
# Core features (backward compatible)
pip install pyshotter

# With all features
pip install pyshotter[full]

# Specific features
pip install pyshotter[recording,gui,ai]
```

### Backward Compatibility
✅ All v1.x code continues to work without changes
✅ Existing CLI commands unchanged
✅ Core screenshot API identical

## [1.0.0] - Previous Release

See previous releases for v1.x changelog.

---

## Links
- [GitHub Repository](https://github.com/utachicodes/pyshotter)
- [PyPI Package](https://pypi.org/project/pyshotter/)
- [Documentation](https://github.com/utachicodes/pyshotter#readme)
