"""Configuration management for PyShotter.

This module provides a robust configuration system with:
- YAML/JSON file support
- Environment variable overrides
- Schema validation using pydantic
- Hot-reload capability
- Per-feature configuration sections
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from pydantic import BaseModel, Field, field_validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False


class GeneralConfig(BaseModel if PYDANTIC_AVAILABLE else object):
    """General application configuration."""
    default_output_dir: str = Field(default="~/Screenshots")
    log_level: str = Field(default="INFO")
    enable_telemetry: bool = Field(default=False)
    
    if PYDANTIC_AVAILABLE:
        @field_validator('log_level')
        @classmethod
        def validate_log_level(cls, v: str) -> str:
            """Validate log level."""
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if v.upper() not in valid_levels:
                raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
            return v.upper()


class OCRConfig(BaseModel if PYDANTIC_AVAILABLE else object):
    """OCR feature configuration."""
    default_language: str = Field(default="eng")
    confidence_threshold: int = Field(default=60, ge=0, le=100)
    tesseract_path: Optional[str] = Field(default=None)


class BeautifierConfig(BaseModel if PYDANTIC_AVAILABLE else object):
    """Code beautifier configuration."""
    default_theme: str = Field(default="dracula")
    shadow_opacity: float = Field(default=0.3, ge=0.0, le=1.0)
    window_style: str = Field(default="macos")
    default_font: str = Field(default="JetBrains Mono")
    
    if PYDANTIC_AVAILABLE:
        @field_validator('window_style')
        @classmethod
        def validate_window_style(cls, v: str) -> str:
            """Validate window style."""
            valid_styles = ['macos', 'windows', 'linux', 'none']
            if v.lower() not in valid_styles:
                raise ValueError(f"Invalid window style: {v}. Must be one of {valid_styles}")
            return v.lower()


class RecordingConfig(BaseModel if PYDANTIC_AVAILABLE else object):
    """Screen recording configuration."""
    default_fps: int = Field(default=30, ge=1, le=60)
    default_format: str = Field(default="gif")
    max_duration: int = Field(default=300, ge=1)  # 5 minutes
    quality: str = Field(default="high")
    
    if PYDANTIC_AVAILABLE:
        @field_validator('default_format')
        @classmethod
        def validate_format(cls, v: str) -> str:
            """Validate recording format."""
            valid_formats = ['gif', 'mp4']
            if v.lower() not in valid_formats:
                raise ValueError(f"Invalid format: {v}. Must be one of {valid_formats}")
            return v.lower()


class GUIConfig(BaseModel if PYDANTIC_AVAILABLE else object):
    """GUI configuration."""
    theme: str = Field(default="dark")
    hotkey_capture: str = Field(default="ctrl+shift+s")
    hotkey_record: str = Field(default="ctrl+shift+r")
    show_notifications: bool = Field(default=True)
    start_with_system: bool = Field(default=False)


class PyShotterConfig(BaseModel if PYDANTIC_AVAILABLE else object):
    """Main PyShotter configuration."""
    general: GeneralConfig = Field(default_factory=GeneralConfig)
    ocr: OCRConfig = Field(default_factory=OCRConfig)
    beautifier: BeautifierConfig = Field(default_factory=BeautifierConfig)
    recording: RecordingConfig = Field(default_factory=RecordingConfig)
    gui: GUIConfig = Field(default_factory=GUIConfig)


class ConfigManager:
    """Manages PyShotter configuration with file persistence and validation."""
    
    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".pyshotter" / "config.yml",
        Path.home() / ".pyshotter" / "config.yaml",
        Path.home() / ".config" / "pyshotter" / "config.yml",
    ]
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """Initialize config manager.
        
        Args:
            config_path: Optional custom config file path
            
        Raises:
            ImportError: If required dependencies are missing
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self._find_config_file()
        
        self.config: PyShotterConfig = PyShotterConfig()
        self._load_config()
    
    def _find_config_file(self) -> Path:
        """Find existing config file or return default path.
        
        Returns:
            Path to config file
        """
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                return path
        return self.DEFAULT_CONFIG_PATHS[0]
    
    def _load_config(self) -> None:
        """Load configuration from file with error handling."""
        if not self.config_path.exists():
            # Create default config
            self._save_config()
            return
        
        try:
            if YAML_AVAILABLE:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
            else:
                import json
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # Apply environment variable overrides
            self._apply_env_overrides(data)
            
            if PYDANTIC_AVAILABLE:
                self.config = PyShotterConfig(**data)
            else:
                # Fallback: manually set attributes
                self._load_dict_config(data)
                
        except Exception as e:
            # Log error and use defaults
            import warnings
            warnings.warn(f"Error loading config from {self.config_path}: {e}. Using defaults.")
            self.config = PyShotterConfig()
    
    def _apply_env_overrides(self, data: Dict[str, Any]) -> None:
        """Apply environment variable overrides.
        
        Args:
            data: Configuration dictionary to update
        """
        # Example: PYSHOTTER_GENERAL_LOG_LEVEL=DEBUG
        prefix = "PYSHOTTER_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                parts = key[len(prefix):].lower().split('_')
                if len(parts) >= 2:
                    section = parts[0]
                    setting = '_'.join(parts[1:])
                    if section not in data:
                        data[section] = {}
                    # Type conversion
                    if value.lower() in ['true', 'false']:
                        data[section][setting] = value.lower() == 'true'
                    elif value.isdigit():
                        data[section][setting] = int(value)
                    else:
                        try:
                            data[section][setting] = float(value)
                        except ValueError:
                            data[section][setting] = value
    
    def _load_dict_config(self, data: Dict[str, Any]) -> None:
        """Load config from dictionary without pydantic (fallback).
        
        Args:
            data: Configuration dictionary
        """
        # Simple attribute setting for fallback mode
        for section, values in data.items():
            if hasattr(self.config, section):
                section_obj = getattr(self.config, section)
                for key, value in values.items():
                    if hasattr(section_obj, key):
                        setattr(section_obj, key, value)
    
    def _save_config(self) -> None:
        """Save current configuration to file with error handling."""
        try:
            # Create directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert config to dictionary
            if PYDANTIC_AVAILABLE:
                data = self.config.model_dump()
            else:
                data = self._config_to_dict()
            
            # Save to file
            if YAML_AVAILABLE:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(data, f, default_flow_style=False)
            else:
                import json
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                    
        except Exception as e:
            import warnings
            warnings.warn(f"Error saving config to {self.config_path}: {e}")
    
    def _config_to_dict(self) -> Dict[str, Any]:
        """Convert config object to dictionary (fallback mode).
        
        Returns:
            Configuration as dictionary
        """
        result = {}
        for section in ['general', 'ocr', 'beautifier', 'recording', 'gui']:
            if hasattr(self.config, section):
                section_obj = getattr(self.config, section)
                result[section] = {
                    key: getattr(section_obj, key)
                    for key in dir(section_obj)
                    if not key.startswith('_') and not callable(getattr(section_obj, key))
                }
        return result
    
    def get(self, section: str, key: Optional[str] = None) -> Any:
        """Get configuration value with error handling.
        
        Args:
            section: Configuration section (e.g., 'general', 'ocr')
            key: Optional key within section
            
        Returns:
            Configuration value or None if not found
        """
        try:
            section_obj = getattr(self.config, section, None)
            if section_obj is None:
                return None
            
            if key is None:
                return section_obj
            
            return getattr(section_obj, key, None)
        except Exception:
            return None
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """Set configuration value with validation.
        
        Args:
            section: Configuration section
            key: Key within section
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            section_obj = getattr(self.config, section, None)
            if section_obj is None:
                return False
            
            setattr(section_obj, key, value)
            self._save_config()
            return True
        except Exception:
            return False
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = PyShotterConfig()
        self._save_config()


# Global config instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[Union[str, Path]] = None) -> ConfigManager:
    """Get or create global config manager.
    
    Args:
        config_path: Optional custom config file path
        
    Returns:
        Global ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager


def get_config(section: str, key: Optional[str] = None) -> Any:
    """Convenience function to get config value.
    
    Args:
        section: Configuration section
        key: Optional key within section
        
    Returns:
        Configuration value
    """
    return get_config_manager().get(section, key)
