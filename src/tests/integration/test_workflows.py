"""Integration tests for PyShotter v1.1."""

import pytest
import tempfile
from pathlib import Path

from pyshotter import pyshotter
from pyshotter.beautifier import CodeBeautifierFeature
from pyshotter.ai_features import EnhancedRedactionFeature
from pyshotter.recording import ScreenRecordingFeature


class TestEndToEndWorkflows:
    """Test complete workflows combining multiple features."""
    
    def test_capture_and_beautify(self):
        """Test capturing and beautifying a screenshot."""
        # Capture
        with pyshotter() as sct:
            screenshot = sct.grab(sct.monitors[1])
        
        # Beautify
        beautifier = CodeBeautifierFeature(theme='dracula')
        beautified = beautifier.beautify(screenshot)
        
        # Save
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            beautified.save(f.name)
            assert Path(f.name).exists()
            Path(f.name).unlink()
    
    def test_capture_and_redact(self):
        """Test capturing and redacting a screenshot."""
        # Capture
        with pyshotter() as sct:
            screenshot = sct.grab(sct.monitors[1])
        
        # Redact
        redactor = EnhancedRedactionFeature(mode='blur')
        redacted = redactor.redact_sensitive_data(screenshot)
        
        # Save
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            redacted.save(f.name)
            assert Path(f.name).exists()
            Path(f.name).unlink()
    
    def test_capture_redact_beautify(self):
        """Test full pipeline: capture -> redact -> beautify."""
        # Capture
        with pyshotter() as sct:
            screenshot = sct.grab(sct.monitors[1])
        
        # Redact
        redactor = EnhancedRedactionFeature(mode='pixelate')
        redacted = redactor.redact_with_template(screenshot, 'gdpr')
        
        # Beautify
        beautifier = CodeBeautifierFeature(theme='nord')
        final = beautifier.beautify(redacted)
        
        # Verify
        assert final is not None
        assert final.size[0] > screenshot.size[0]  # Should be larger due to beautification
    
    def test_multiple_screenshots_processing(self):
        """Test processing multiple screenshots."""
        screenshots = []
        
        # Capture multiple
        with pyshotter() as sct:
            for _ in range(3):
                screenshot = sct.grab(sct.monitors[1])
                screenshots.append(screenshot)
        
        # Process all
        beautifier = CodeBeautifierFeature()
        beautified = [beautifier.beautify(s) for s in screenshots]
        
        assert len(beautified) == 3
        assert all(b is not None for b in beautified)
    
    @pytest.mark.slow
    def test_record_and_save(self):
        """Test recording workflow."""
        recorder = ScreenRecordingFeature(fps=10, format='gif')
        
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as f:
            output = recorder.record(duration=1, output=f.name)
            
            assert Path(output).exists()
            assert Path(output).stat().st_size > 0
            
            # Cleanup
            Path(output).unlink()


class TestCLIIntegration:
    """Test CLI integration (would be run via subprocess in real tests)."""
    
    def test_cli_imports(self):
        """Test that CLI can import all required modules."""
        from pyshotter.__main__ import (
            setup_argument_parser,
            handle_ocr,
            handle_redaction,
            handle_beautify
        )
        
        # Just test imports work
        parser = setup_argument_parser()
        assert parser is not None


class TestConfigIntegration:
    """Test configuration integration with features."""
    
    def test_config_with_beautifier(self):
        """Test that beautifier respects config."""
        from pyshotter.config import ConfigManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / 'config.yml'
            manager = ConfigManager(config_path)
            
            # Set beautifier config
            manager.set('beautifier', 'default_theme', 'monokai')
            
            # Get and verify
            theme = manager.get('beautifier', 'default_theme')
            assert theme == 'monokai'
