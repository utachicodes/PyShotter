# Release Checklist for PyShotter v1.1

## Pre-Release

- [x] All features implemented
- [x] Tests written and passing
- [x] Documentation updated
- [x] CHANGELOG.md created
- [x] MIGRATION.md created
- [ ] Version bumped in `src/pyshotter/__init__.py`
- [ ] All CI/CD checks passing

## Testing

- [ ] Run full test suite locally:
  ```bash
  pytest --cov=pyshotter --cov-report=term-missing
  ```

- [ ] Test installation from wheel:
  ```bash
  python -m build
  pip install dist/*.whl
  ```

- [ ] Manual testing of key features:
  - [ ] Screenshot capture
  - [ ] Code beautification  
  - [ ] Screen recording
  - [ ] OCR extraction
  - [ ] Face blurring
  - [ ] GUI application

## Documentation

- [ ] README.md updated with v1.1 features
- [ ] Examples tested and working
- [ ] API documentation generated
- [ ] Migration guide reviewed

## Git & GitHub

- [ ] All changes committed
- [ ] Create release branch: `git checkout -b release/v1.1.0`
- [ ] Push to GitHub: `git push origin release/v1.1.0`
- [ ] Create Pull Request to main
- [ ] Get approvals (if applicable)
- [ ] Merge to main
- [ ] Create git tag:
  ```bash
  git tag -a v1.1.0 -m "PyShotter v1.1.0 - Major feature release"
  git push origin v1.1.0
  ```

## PyPI Release

### Test PyPI (Optional but Recommended)
```bash
# Build
python -m build

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ pyshotter
```

### Production PyPI
```bash
# Build distribution
python -m build

# Check distribution
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Or use GitHub Actions automated release (triggered by tag)
```

## Post-Release

- [ ] Verify package on PyPI: https://pypi.org/project/pyshotter/
- [ ] Test installation: `pip install pyshotter==1.1.0`
- [ ] Create GitHub Release with notes
- [ ] Update GitHub repository description
- [ ] Tweet/announce release (optional)
- [ ] Monitor for issues

## Commands Reference

```bash
# Version bump
# Edit src/pyshotter/__init__.py: __version__ = "1.1.0"

# Build
python -m build

# Check
twine check dist/*

# Upload to Test PyPI  
twine upload --repository testpypi dist/*

# Upload to Production PyPI
twine upload dist/*

# Create and push tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# GitHub Actions will automatically:
# - Run tests
# - Build packages
# - Publish to PyPI (with tag)
# - Create GitHub release
```

## Environment Setup

Make sure you have:
```bash
pip install build twine

# For testing
pip install pytest pytest-cov

# PyPI credentials
# Set in ~/.pypirc or use tokens:
# PYPI_API_TOKEN (in GitHub secrets for CI)
# TEST_PYPI_API_TOKEN (for test uploads)
```

## Troubleshooting

- **Build fails**: Check `pyproject.toml` syntax
- **Upload fails**: Verify PyPI credentials
- **Import fails**: Check package structure in `dist/`
- **Tests fail**: Run locally first, check dependencies
