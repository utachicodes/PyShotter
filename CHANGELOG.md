# Changelog

All notable changes to PyShotter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- Initial release of PyShotter: Smart, annotated, and shareable screenshots for Python
- **Smart Detection Features:**
  - Code region detection using computer vision
  - Window detection and identification
  - OCR text extraction using Tesseract
- **Rich Annotation Tools:**
  - Text annotations with custom fonts and colors
  - Shape drawing (rectangles, circles, arrows)
  - Smart highlighting with transparency
  - Quick markup commands
- **Easy Sharing Capabilities:**
  - Clipboard copy functionality
  - Shareable link generation
  - Cloud upload with metadata
  - Cross-platform compatibility
- **Advanced Features:**
  - Sensitive data redaction (emails, phones, credit cards)
  - Multi-monitor panorama creation
  - Change detection between screenshots
  - Customizable hotkey support
  - Screenshot history and search functionality
- Cross-platform support (Windows, macOS, Linux)
- High-performance screenshot capture using ctypes
- Thread-safe operations
- Integration with PIL, NumPy, and OpenCV
- Comprehensive documentation and examples

### Changed
- Rebranded from MSS to PyShotter
- Updated all author information to Abdoullah Ndao
- Enhanced project structure and metadata
- Improved documentation with smart, annotated, and shareable focus

### Technical
- Python 3.9+ support
- PEP 8 compliant code
- Type hints throughout
- Modern packaging with pyproject.toml

---

## Version History

- **1.0.0**: Initial stable release with smart, annotated, and shareable features

## Contributing

To add entries to this changelog:

1. Add your changes under the appropriate section
2. Use the present tense ("Add" not "Added")
3. Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
4. Reference issues and pull requests when applicable
5. Update the version number and release date when releasing

## Release Process

1. Update version in `src/pyshotter/__init__.py`
2. Update this CHANGELOG.md with release date
3. Create a git tag for the release
4. Build and upload to PyPI
