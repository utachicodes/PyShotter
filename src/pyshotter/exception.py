"""Exception hierarchy for PyShotter.

This module defines all exceptions used throughout PyShotter with:
- Detailed error messages
- Context information
- Recovery suggestions
"""

from __future__ import annotations

from typing import Any, Optional


class ScreenShotError(Exception):
    """Base error handling class for PyShotter.
    
    Attributes:
        message: Error message
        details: Additional context information
        recovery_hint: Suggestion for recovering from error
    """

    def __init__(
        self, 
        message: str, 
        /, 
        *, 
        details: dict[str, Any] | None = None,
        recovery_hint: Optional[str] = None
    ) -> None:
        """Initialize exception.
        
        Args:
            message: Error message
            details: Additional context
            recovery_hint: Optional recovery suggestion
        """
        super().__init__(message)
        self.details = details or {}
        self.recovery_hint = recovery_hint


class ConfigError(ScreenShotError):
    """Configuration-related errors.
    
    Raised when:
    - Config file is invalid
    - Config validation fails
    - Required settings are missing
    """
    
    def __init__(self, message: str, config_path: Optional[str] = None, **kwargs):
        """Initialize configuration error.
        
        Args:
            message: Error message
            config_path: Path to problematic config file
            **kwargs: Additional details
        """
        details = kwargs.get('details', {})
        if config_path:
            details['config_path'] = config_path
        
        super().__init__(
            message,
            details=details,
            recovery_hint=kwargs.get('recovery_hint', 
                                    "Check config file syntax and required fields")
        )


class DependencyError(ScreenShotError):
    """Missing optional dependency errors.
    
    Raised when:
    - Required library not installed
    - Library version incompatible
    """
    
    def __init__(
        self, 
        feature: str, 
        missing_lib: str,
        install_command: Optional[str] = None,
        **kwargs
    ):
        """Initialize dependency error.
        
        Args:
            feature: Feature requiring the dependency
            missing_lib: Name of missing library
            install_command: Suggested installation command
            **kwargs: Additional details
        """
        message = f"{feature} requires '{missing_lib}' which is not installed."
        
        if install_command:
            recovery_hint = f"Install with: {install_command}"
        else:
            recovery_hint = f"Install with: pip install {missing_lib}"
        
        super().__init__(
            message,
            details={'feature': feature, 'library': missing_lib},
            recovery_hint=recovery_hint
        )


class OCRError(ScreenShotError):
    """OCR operation errors.
    
    Raised when:
    - Tesseract not found
    - OCR extraction fails
    - Invalid language specified
    """
    
    def __init__(self, message: str, **kwargs):
        """Initialize OCR error.
        
        Args:
            message: Error message
            **kwargs: Additional details
        """
        super().__init__(
            message,
            details=kwargs.get('details', {}),
            recovery_hint=kwargs.get('recovery_hint',
                                    "Ensure Tesseract is installed and in PATH")
        )


class RecordingError(ScreenShotError):
    """Screen recording errors.
    
    Raised when:
    - Recording initialization fails
    - Frame capture fails
    - Encoding fails
    - Insufficient disk space
    """
    
    def __init__(self, message: str, recording_id: Optional[str] = None, **kwargs):
        """Initialize recording error.
        
        Args:
            message: Error message
            recording_id: ID of failed recording
            **kwargs: Additional details
        """
        details = kwargs.get('details', {})
        if recording_id:
            details['recording_id'] = recording_id
        
        super().__init__(
            message,
            details=details,
            recovery_hint=kwargs.get('recovery_hint',
                                    "Check disk space and try reducing quality/FPS")
        )


class BeautifierError(ScreenShotError):
    """Code beautification errors.
    
    Raised when:
    - Theme not found
    - Font not available
    - Image processing fails
    """
    
    def __init__(self, message: str, theme: Optional[str] = None, **kwargs):
        """Initialize beautifier error.
        
        Args:
            message: Error message
            theme: Theme name that caused error
            **kwargs: Additional details
        """
        details = kwargs.get('details', {})
        if theme:
            details['theme'] = theme
        
        super().__init__(
            message,
            details=details,
            recovery_hint=kwargs.get('recovery_hint',
                                    "Try a different theme or check font installation")
        )


class GUIError(ScreenShotError):
    """GUI-related errors.
    
    Raised when:
    - System tray initialization fails
    - Hotkey registration fails
    - Window creation fails
    """
    
    def __init__(self, message: str, component: Optional[str] = None, **kwargs):
        """Initialize GUI error.
        
        Args:
            message: Error message
            component: GUI component that failed
            **kwargs: Additional details
        """
        details = kwargs.get('details', {})
        if component:
            details['component'] = component
        
        super().__init__(
            message,
            details=details,
            recovery_hint=kwargs.get('recovery_hint',
                                    "Check system permissions and try restarting")
        )


class RegionSelectionError(ScreenShotError):
    """Region selection errors.
    
    Raised when:
    - Invalid region coordinates
    - Region selection cancelled
    """
    
    def __init__(self, message: str, region: Optional[tuple] = None, **kwargs):
        """Initialize region selection error.
        
        Args:
            message: Error message
            region: Invalid region coordinates
            **kwargs: Additional details
        """
        details = kwargs.get('details', {})
        if region:
            details['region'] = region
        
        super().__init__(
            message,
            details=details,
            recovery_hint=kwargs.get('recovery_hint',
                                    "Ensure region coordinates are within screen bounds")
        )


class ValidationError(ScreenShotError):
    """Input validation errors.
    
    Raised when:
    - Invalid parameters
    - Out of range values
    - Type mismatches
    """
    
    def __init__(
        self, 
        message: str, 
        param_name: Optional[str] = None,
        expected: Optional[str] = None,
        got: Optional[Any] = None,
        **kwargs
    ):
        """Initialize validation error.
        
        Args:
            message: Error message
            param_name: Name of invalid parameter
            expected: Expected value/type
            got: Actual value received
            **kwargs: Additional details
        """
        details = kwargs.get('details', {})
        if param_name:
            details['param_name'] = param_name
        if expected:
            details['expected'] = expected
        if got is not None:
            details['got'] = str(got)
        
        super().__init__(
            message,
            details=details,
            recovery_hint=kwargs.get('recovery_hint',
                                    "Check parameter documentation for valid values")
        )
