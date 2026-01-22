"""Unit tests for code beautifier."""

import pytest
import numpy as np
from PIL import Image

from pyshotter.screenshot import ScreenShot
from pyshotter.beautifier import CodeBeautifierFeature, get_available_themes, THEMES
from pyshotter.exception import BeautifierError, DependencyError


class TestCodeBeautifier:
    """Test code beautification feature."""
    
    @pytest.fixture
    def sample_screenshot(self):
        """Create a sample screenshot for testing."""
        # Create simple 100x100 RGB image
        img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        img_bytes = img_array.tobytes()
        return ScreenShot(rgb=img_bytes, size=(100, 100), pos=(0, 0))
    
    def test_beautifier_init_valid_theme(self):
        """Test beautifier initialization with valid theme."""
        beautifier = CodeBeautifierFeature(theme='dracula')
        assert beautifier.theme == 'dracula'
        assert beautifier.theme_colors == THEMES['dracula']
    
    def test_beautifier_init_invalid_theme(self):
        """Test beautifier initialization with invalid theme."""
        with pytest.raises(BeautifierError) as exc_info:
            CodeBeautifierFeature(theme='invalid_theme')
        
        assert 'Unknown theme' in str(exc_info.value)
    
    def test_beautifier_window_style_auto_detect(self):
        """Test automatic window style detection."""
        beautifier = CodeBeautifierFeature()
        assert beautifier.window_style in ['macos', 'windows', 'linux']
    
    def test_beautifier_window_style_override(self):
        """Test manual window style override."""
        beautifier = CodeBeautifierFeature(window_style='windows')
        assert beautifier.window_style == 'windows'
    
    def test_beautify_increases_size(self, sample_screenshot):
        """Test that beautification increases image size (due to padding)."""
        beautifier = CodeBeautifierFeature()
        beautified = beautifier.beautify(sample_screenshot, padding=50)
        
        # Original is 100x100, with 50px padding on each side should be 200x200 + controls
        assert beautified.width > sample_screenshot.width
        assert beautified.height > sample_screenshot.height
    
    def test_beautify_with_different_themes(self, sample_screenshot):
        """Test beautification with different themes."""
        for theme_name in get_available_themes():
            beautifier = CodeBeautifierFeature(theme=theme_name)
            beautified = beautifier.beautify(sample_screenshot)
            
            assert beautified is not None
            assert beautified.size[0] > 0
            assert beautified.size[1] > 0
    
    def test_beautify_gradient_background(self, sample_screenshot):
        """Test gradient background generation."""
        beautifier = CodeBeautifierFeature()
        beautified = beautifier.beautify(
            sample_screenshot,
            background_type='gradient'
        )
        assert beautified is not None
    
    def test_beautify_solid_background(self, sample_screenshot):
        """Test solid background."""
        beautifier = CodeBeautifierFeature()
        beautified = beautifier.beautify(
            sample_screenshot,
            background_type='solid'
        )
        assert beautified is not None
    
    def test_beautify_shadow_intensity(self, sample_screenshot):
        """Test different shadow intensities."""
        beautifier = CodeBeautifierFeature()
        
        # No shadow
        no_shadow = beautifier.beautify(sample_screenshot, shadow_intensity=0.0)
        assert no_shadow is not None
        
        # Full shadow
        full_shadow = beautifier.beautify(sample_screenshot, shadow_intensity=1.0)
        assert full_shadow is not None
    
    def test_get_available_themes(self):
        """Test getting available themes."""
        themes = get_available_themes()
        assert isinstance(themes, list)
        assert len(themes) == 7  # We have 7 themes
        assert 'dracula' in themes
        assert 'monokai' in themes
        assert 'nord' in themes


class TestBeautifierThemes:
    """Test theme definitions."""
    
    def test_all_themes_have_required_keys(self):
        """Test that all themes have required color keys."""
        required_keys = ['bg_start', 'bg_end', 'window_bg', 'shadow', 'text']
        
        for theme_name, theme_colors in THEMES.items():
            for key in required_keys:
                assert key in theme_colors, f"Theme {theme_name} missing key {key}"
                assert isinstance(theme_colors[key], tuple)
                assert len(theme_colors[key]) == 3  # RGB tuple
    
    def test_theme_colors_valid_range(self):
        """Test that all theme colors are valid RGB values."""
        for theme_name, theme_colors in THEMES.items():
            for key, color in theme_colors.items():
                for channel in color:
                    assert 0 <= channel <= 255, f"Invalid color in {theme_name}.{key}"


@pytest.mark.benchmark
class TestBeautifierPerformance:
    """Benchmark tests for beautifier."""
    
    @pytest.fixture
    def large_screenshot(self):
        """Create a large screenshot for benchmarking."""
        img_array = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        img_bytes = img_array.tobytes()
        return ScreenShot(rgb=img_bytes, size=(1920, 1080), pos=(0, 0))
    
    def test_beautify_performance(self, benchmark, large_screenshot):
        """Benchmark beautification performance."""
        beautifier = CodeBeautifierFeature()
        
        result = benchmark(beautifier.beautify, large_screenshot)
        assert result is not None
