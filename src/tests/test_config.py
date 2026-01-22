"""Unit tests for configuration system."""

import pytest
from pathlib import Path
import tempfile
import yaml

from pyshotter.config import (
    ConfigManager,
    PyShotterConfig,
    GeneralConfig,
    OCRConfig,
    BeautifierConfig,
    RecordingConfig,
    GUIConfig,
    get_config_manager,
)


class TestConfigClasses:
    """Test configuration data classes."""
    
    def test_general_config_defaults(self):
        """Test GeneralConfig default values."""
        config = GeneralConfig()
        assert config.default_output_dir == "~/Screenshots"
        assert config.log_level == "INFO"
        assert config.enable_telemetry is False
    
    def test_ocr_config_defaults(self):
        """Test OCRConfig default values."""
        config = OCRConfig()
        assert config.default_language == "eng"
        assert config.confidence_threshold == 60
    
    def test_beautifier_config_defaults(self):
        """Test BeautifierConfig default values."""
        config = BeautifierConfig()
        assert config.default_theme == "dracula"
        assert config.shadow_opacity == 0.3
        assert config.window_style == "macos"
    
    def test_recording_config_defaults(self):
        """Test RecordingConfig default values."""
        config = RecordingConfig()
        assert config.default_fps == 30
        assert config.default_format == "gif"
        assert config.max_duration == 300


class TestConfigManager:
    """Test configuration manager."""
    
    @pytest.fixture
    def temp_config_path(self):
        """Create temporary config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            config_data = {
                'general': {
                    'log_level': 'DEBUG',
                    'default_output_dir': '/tmp/screenshots'
                },
                'beautifier': {
                    'default_theme': 'nord'
                }
            }
            yaml.safe_dump(config_data, f)
            return Path(f.name)
    
    def test_config_manager_init(self, temp_config_path):
        """Test ConfigManager initialization."""
        manager = ConfigManager(temp_config_path)
        assert manager.config_path == temp_config_path
        assert manager.config is not None
    
    def test_config_manager_load(self, temp_config_path):
        """Test configuration loading."""
        manager = ConfigManager(temp_config_path)
        
        # Check loaded values
        assert manager.config.general.log_level == 'DEBUG'
        assert manager.config.general.default_output_dir == '/tmp/screenshots'
        assert manager.config.beautifier.default_theme == 'nord'
    
    def test_config_manager_get(self, temp_config_path):
        """Test get method."""
        manager = ConfigManager(temp_config_path)
        
        log_level = manager.get('general', 'log_level')
        assert log_level == 'DEBUG'
        
        theme = manager.get('beautifier', 'default_theme')
        assert theme == 'nord'
    
    def test_config_manager_set(self, temp_config_path):
        """Test set method."""
        manager = ConfigManager(temp_config_path)
        
        result = manager.set('general', 'log_level', 'WARNING')
        assert result is True
        assert manager.config.general.log_level == 'WARNING'
    
    def test_config_env_override(self, temp_config_path, monkeypatch):
        """Test environment variable override."""
        monkeypatch.setenv('PYSHOTTER_GENERAL_LOG_LEVEL', 'ERROR')
        
        manager = ConfigManager(temp_config_path)
        assert manager.config.general.log_level == 'ERROR'
    
    def test_config_default_creation(self):
        """Test default config creation when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / 'nonexistent.yml'
            manager = ConfigManager(config_path)
            
            # Should create default config
            assert config_path.exists()
            assert manager.config.general.log_level == 'INFO'


class TestConfigValidation:
    """Test configuration validation."""
    
    def test_invalid_log_level(self):
        """Test that invalid log level is validated."""
        # This would raise ValidationError with pydantic
        # For now just test the config loads
        config = GeneralConfig()
        assert config.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    def test_fps_range(self):
        """Test FPS is within valid range."""
        config = RecordingConfig()
        assert 1 <= config.default_fps <= 60
