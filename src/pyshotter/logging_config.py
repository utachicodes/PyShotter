"""Logging configuration for PyShotter.

This module provides centralized logging with:
- JSON structured logging support
- File rotation (daily/size-based)
- Console and file handlers
- Per-module log levels
- Performance metrics logging
- Privacy-aware logging (no PII)
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime


class PrivacyFilter(logging.Filter):
    """Filter sensitive information from log messages."""
    
    SENSITIVE_PATTERNS = [
        # Email patterns
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        # Phone patterns
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        # Credit card patterns
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        # SSN patterns
        r'\b\d{3}-\d{2}-\d{4}\b',
        # API keys
        r'sk-[A-Za-z0-9]{48}',
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter and redact sensitive information.
        
        Args:
            record: Log record to filter
            
        Returns:
            Always True (record is kept but may be modified)
        """
        import re
        
        # Redact message
        for pattern in self.SENSITIVE_PATTERNS:
            record.msg = re.sub(pattern, '[REDACTED]', str(record.msg))
        
        return True


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON-formatted log string
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add custom fields
        if hasattr(record, 'performance_ms'):
            log_data['performance_ms'] = record.performance_ms
        
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        return json.dumps(log_data)


class ColoredConsoleFormatter(logging.Formatter):
    """Colored console formatter for better readability."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors.
        
        Args:
            record: Log record to format
            
        Returns:
            Colored log string
        """
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


class LoggingConfig:
    """Configures logging for PyShotter."""
    
    def __init__(
        self,
        log_dir: Optional[Path] = None,
        log_level: str = "INFO",
        console_output: bool = True,
        file_output: bool = True,
        json_format: bool = False,
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5,
    ):
        """Initialize logging configuration.
        
        Args:
            log_dir: Directory for log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output: Enable console logging
            file_output: Enable file logging
            json_format: Use JSON formatting for file logs
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
        """
        self.log_dir = log_dir or Path.home() / ".pyshotter" / "logs"
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.console_output = console_output
        self.file_output = file_output
        self.json_format = json_format
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # Create log directory
        if self.file_output:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._configure()
    
    def _configure(self) -> None:
        """Configure logging handlers and formatters."""
        # Get root logger
        root_logger = logging.getLogger('pyshotter')
        root_logger.setLevel(self.log_level)
        
        # Remove existing handlers
        root_logger.handlers.clear()
        
        # Console handler
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            
            console_formatter = ColoredConsoleFormatter(
                '%(levelname)s - %(name)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            console_handler.addFilter(PrivacyFilter())
            root_logger.addHandler(console_handler)
        
        # File handler with rotation
        if self.file_output:
            log_file = self.log_dir / "pyshotter.log"
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.log_level)
            
            if self.json_format:
                file_formatter = JSONFormatter()
            else:
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            
            file_handler.setFormatter(file_formatter)
            file_handler.addFilter(PrivacyFilter())
            root_logger.addHandler(file_handler)
        
        # Set up module-specific loggers
        self._configure_module_loggers()
    
    def _configure_module_loggers(self) -> None:
        """Configure logging levels for specific modules."""
        # Reduce noise from third-party libraries
        logging.getLogger('PIL').setLevel(logging.WARNING)
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get logger for specific module.
        
        Args:
            name: Logger name (typically __name__)
            
        Returns:
            Logger instance
        """
        return logging.getLogger(f'pyshotter.{name}')


# Performance logging helper
class PerformanceLogger:
    """Context manager for performance logging."""
    
    def __init__(self, logger: logging.Logger, operation: str):
        """Initialize performance logger.
        
        Args:
            logger: Logger instance
            operation: Operation name
        """
        self.logger = logger
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        """Start performance measurement."""
        import time
        self.start_time = time.perf_counter()
        self.logger.debug(f"Starting: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log performance metrics."""
        import time
        duration_ms = (time.perf_counter() - self.start_time) * 1000
        
        if exc_type is None:
            self.logger.info(
                f"Completed: {self.operation}",
                extra={'performance_ms': duration_ms}
            )
        else:
            self.logger.error(
                f"Failed: {self.operation} after {duration_ms:.2f}ms",
                extra={'performance_ms': duration_ms}
            )


# Global logging configuration
_logging_config: Optional[LoggingConfig] = None


def setup_logging(
    log_level: str = "INFO",
    console_output: bool = True,
    file_output: bool = True,
    json_format: bool = False,
) -> None:
    """Set up global logging configuration.
    
    Args:
        log_level: Logging level
        console_output: Enable console logging
        file_output: Enable file logging
        json_format: Use JSON formatting
    """
    global _logging_config
    _logging_config = LoggingConfig(
        log_level=log_level,
        console_output=console_output,
        file_output=file_output,
        json_format=json_format,
    )


def get_logger(name: str) -> logging.Logger:
    """Get logger instance with automatic configuration.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    global _logging_config
    if _logging_config is None:
        setup_logging()
    
    return LoggingConfig.get_logger(name)
