# Contributing to PyShotter

Thank you for your interest in contributing to PyShotter! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git
- pip

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/utachicodes/pyshotter.git
   cd pyshotter
   ```

2. **Install development dependencies**
   ```bash
   python -m pip install -e ".[dev]"
   ```

3. **Run tests**
   ```bash
   python -m pytest
   ```

## 📝 Code Style

We use the following tools to maintain code quality:

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Pytest** for testing

### Running Code Quality Checks

```bash
# Format code
ruff format src/

# Lint code
ruff check src/

# Type checking
mypy src/

# Run all checks
ruff check src/ && mypy src/ && python -m pytest
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src/pyshotter

# Run specific test file
python -m pytest tests/test_windows.py
```

### Writing Tests

- Tests should be in the `src/tests/` directory
- Use descriptive test names
- Include both unit tests and integration tests
- Test both success and failure cases

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Operating System** and version
2. **Python version**
3. **PyShotter version**
4. **Steps to reproduce**
5. **Expected vs actual behavior**
6. **Error messages** (if any)

## 💡 Feature Requests

When suggesting new features:

1. **Describe the feature** clearly
2. **Explain the use case** and benefits
3. **Provide examples** if possible
4. **Consider implementation** complexity

## 🔧 Pull Request Guidelines

### Before Submitting

1. **Test your changes**
   ```bash
   python -m pytest
   ruff check src/
   mypy src/
   ```

2. **Update documentation** if needed
3. **Add tests** for new features
4. **Update CHANGELOG.md** with your changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test update

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## 📚 Documentation

### Building Documentation

```bash
# Install docs dependencies
python -m pip install -e ".[docs]"

# Build documentation
cd docs
make html
```

### Documentation Guidelines

- Use clear, concise language
- Include code examples
- Keep examples up-to-date
- Follow RST formatting guidelines

## 🏷️ Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backward compatible)
- **PATCH** version for backward compatible bug fixes

## 📄 License

By contributing to PyShotter, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

Please be respectful and inclusive in all interactions. We follow the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/utachicodes/pyshotter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/utachicodes/pyshotter/discussions)
- **Email**: abdoullahaljersi@gmail.com

Thank you for contributing to PyShotter! 🚀 