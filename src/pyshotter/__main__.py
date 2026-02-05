"""Enhanced CLI for PyShotter v1.1.

This module provides comprehensive command-line interface with:
- OCR text extraction
- Sensitive data redaction  
- Code beautification
- Screen recording
- Batch processing
- Rich output formatting
"""

import os
import sys
import json
from argparse import ArgumentParser, Namespace

from pyshotter import __version__
from pyshotter.exception import ScreenShotError
from pyshotter.factory import pyshotter
from pyshotter.tools import to_png
from pyshotter.logging_config import setup_logging, get_logger

# Import optional features with fallbacks
try:
    from pyshotter.beautifier import CodeBeautifierFeature, get_available_themes  # noqa: F401
    BEAUTIFIER_AVAILABLE = True
except ImportError:
    BEAUTIFIER_AVAILABLE = False

try:
    from pyshotter.recording import ScreenRecordingFeature  # noqa: F401
    RECORDING_AVAILABLE = True
except ImportError:
    RECORDING_AVAILABLE = False

try:
    from pyshotter.ai_features import EnhancedRedactionFeature, FaceBlurFeature  # noqa: F401
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

try:
    from pyshotter.features import OCRFeature  # noqa: F401
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn  # noqa: F401
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


logger = get_logger(__name__)


def setup_argument_parser() -> ArgumentParser:
    """Create enhanced argument parser with all features.
    
    Returns:
        Configured ArgumentParser
    """
    cli_args = ArgumentParser(
        prog="pyshotter",
        description="PyShotter v1.1 - Smart, annotated, and shareable screenshots"
    )
    
    # Basic options
    cli_args.add_argument(
        "-c", "--coordinates",
        default="",
        type=str,
        help="the part of the screen to capture: top,left,width,height"
    )
    cli_args.add_argument(
        "-l", "--level",
        default=6,
        type=int,
        choices=list(range(10)),
        help="the PNG compression level"
    )
    cli_args.add_argument(
        "-m", "--monitor",
        default=0,
        type=int,
        help="the monitor to screenshot"
    )
    cli_args.add_argument(
        "-o", "--output",
        default="monitor-{mon}.png",
        help="the output file name"
    )
    cli_args.add_argument(
        "--with-cursor",
        default=False,
        action="store_true",
        help="include the cursor"
    )
    cli_args.add_argument(
        "-q", "--quiet",
        default=False,
        action="store_true",
        help="do not print created files"
    )
    cli_args.add_argument(
        "-v", "--version",
        action="version",
        version=__version__
    )
    cli_args.add_argument(
        "--verbose",
        action="store_true",
        help="increase logging verbosity"
    )
    
    # OCR options
    if OCR_AVAILABLE:
        ocr_group = cli_args.add_argument_group('OCR options')
        ocr_group.add_argument(
            "--ocr",
            action="store_true",
            help="extract text using OCR"
        )
        ocr_group.add_argument(
            "--ocr-lang",
            default="eng",
            help="OCR language (default: eng)"
        )
        ocr_group.add_argument(
            "--ocr-confidence",
            type=int,
            default=60,
            help="minimum OCR confidence threshold (0-100)"
        )
    
    # Redaction options
    if AI_AVAILABLE:
        redact_group = cli_args.add_argument_group('Redaction options')
        redact_group.add_argument(
            "--redact",
            action="store_true",
            help="redact sensitive data"
        )
        redact_group.add_argument(
            "--redact-patterns",
            default="email,phone,ssn",
            help="comma-separated list of patterns to redact"
        )
        redact_group.add_argument(
            "--redact-style",
            choices=['blur', 'pixelate', 'block', 'generate'],
            default='blur',
            help="redaction style"
        )
        redact_group.add_argument(
            "--redact-template",
            choices=['medical', 'financial', 'government', 'corporate', 'gdpr'],
            help="use privacy template"
        )
        redact_group.add_argument(
            "--blur-faces",
            action="store_true",
            help="automatically blur detected faces"
        )
    
    # Beautifier options
    if BEAUTIFIER_AVAILABLE:
        beauty_group = cli_args.add_argument_group('Beautification options')
        beauty_group.add_argument(
            "--beautify",
            action="store_true",
            help="beautify code screenshot"
        )
        beauty_group.add_argument(
            "--beautify-theme",
            choices=get_available_themes(),
            default='dracula',
            help="code beautification theme"
        )
        beauty_group.add_argument(
            "--beautify-padding",
            type=int,
            default=60,
            help="padding around screenshot (pixels)"
        )
        beauty_group.add_argument(
            "--beautify-shadow",
            type=float,
            default=0.5,
            help="shadow intensity (0.0-1.0)"
        )
    
    # Recording options
    if RECORDING_AVAILABLE:
        record_group = cli_args.add_argument_group('Recording options')
        record_group.add_argument(
            "--record",
            type=float,
            metavar="DURATION",
            help="record screen for DURATION seconds"
        )
        record_group.add_argument(
            "--record-fps",
            type=int,
            default=30,
            help="recording frame rate (1-60)"
        )
        record_group.add_argument(
            "--record-format",
            choices=['gif', 'mp4'],
            default='gif',
            help="recording output format"
        )
        record_group.add_argument(
            "--record-quality",
            choices=['low', 'medium', 'high', 'lossless'],
            default='high',
            help="recording quality"
        )
    
    # Output options
    cli_args.add_argument(
        "--json",
        action="store_true",
        help="output metadata in JSON format"
    )
    cli_args.add_argument(
        "--batch",
        type=str,
        metavar="DIR",
        help="batch process all screenshots in directory"
    )
    
    return cli_args


def handle_ocr(screenshot_path: str, options: Namespace) -> dict:
    """Handle OCR extraction.
    
    Args:
        screenshot_path: Path to screenshot
        options: CLI options
        
    Returns:
        Dict with OCR results
    """
    from PIL import Image
    from pyshotter.features import OCRFeature
    from pyshotter.screenshot import ScreenShot
    
    logger.info(f"Performing OCR on {screenshot_path}")
    
    # Load screenshot
    img = Image.open(screenshot_path)
    img_bytes = img.tobytes()
    screenshot = ScreenShot(rgb=img_bytes, size=img.size, pos=(0, 0))
    
    # Extract text
    ocr = OCRFeature()
    text = ocr.extract_text(screenshot, lang=options.ocr_lang)
    
    if not options.quiet:
        if RICH_AVAILABLE:
            console.print(f"[bold green]OCR Text:[/bold green]\n{text}")
        else:
            print(f"OCR Text:\n{text}")
    
    return {'text': text, 'language': options.ocr_lang}


def handle_redaction(screenshot_path: str, options: Namespace) -> str:
    """Handle redaction.
    
    Args:
        screenshot_path: Path to screenshot
        options: CLI options
        
    Returns:
        Path to redacted screenshot
    """
    from PIL import Image
    from pyshotter.ai_features import EnhancedRedactionFeature, FaceBlurFeature
    from pyshotter.screenshot import ScreenShot
    
    logger.info(f"Redacting {screenshot_path}")
    
    # Load screenshot
    img = Image.open(screenshot_path)
    img_bytes = img.tobytes()
    screenshot = ScreenShot(rgb=img_bytes, size=img.size, pos=(0, 0))
    
    # Apply redaction
    redactor = EnhancedRedactionFeature(mode=options.redact_style)
    
    if options.redact_template:
        redacted = redactor.redact_with_template(screenshot, options.redact_template)
    else:
        patterns = options.redact_patterns.split(',')
        redacted = redactor.redact_sensitive_data(screenshot, patterns)
    
    # Apply face blurring if requested
    if options.blur_faces:
        face_blur = FaceBlurFeature()
        redacted = face_blur.blur_faces(redacted)
    
    # Save
    output_path = screenshot_path.replace('.png', '_redacted.png')
    redacted.save(output_path)
    
    if not options.quiet:
        if RICH_AVAILABLE:
            console.print(f"[green]✓[/green] Saved redacted: {output_path}")
        else:
            print(f"Saved redacted: {output_path}")
    
    return output_path


def handle_beautify(screenshot_path: str, options: Namespace) -> str:
    """Handle beautification.
    
    Args:
        screenshot_path: Path to screenshot
        options: CLI options
        
    Returns:
        Path to beautified screenshot
    """
    from PIL import Image
    from pyshotter.beautifier import CodeBeautifierFeature
    from pyshotter.screenshot import ScreenShot
    
    logger.info(f"Beautifying {screenshot_path}")
    
    # Load screenshot
    img = Image.open(screenshot_path)
    img_bytes = img.tobytes()
    screenshot = ScreenShot(rgb=img_bytes, size=img.size, pos=(0, 0))
    
    # Beautify
    beautifier = CodeBeautifierFeature(theme=options.beautify_theme)
    beautified = beautifier.beautify(
        screenshot,
        padding=options.beautify_padding,
        shadow_intensity=options.beautify_shadow
    )
    
    # Save
    output_path = screenshot_path.replace('.png', '_beautified.png')
    beautified.save(output_path)
    
    if not options.quiet:
        if RICH_AVAILABLE:
            console.print(f"[green]✓[/green] Saved beautified: {output_path}")
        else:
            print(f"Saved beautified: {output_path}")
    
    return output_path


def handle_recording(options: Namespace) -> str:
    """Handle screen recording.
    
    Args:
        options: CLI options
        
    Returns:
        Path to recording
    """
    from pyshotter.recording import ScreenRecordingFeature
    
    logger.info(f"Recording for {options.record} seconds")
    
    recorder = ScreenRecordingFeature(
        fps=options.record_fps,
        quality=options.record_quality,
        format=options.record_format
    )
    
    # Progress callback
    def progress(frame_count, elapsed, eta):
        if not options.quiet and RICH_AVAILABLE:
            console.print(f"Recording... Frames: {frame_count}, Elapsed: {elapsed:.1f}s")
    
    # Record
    output_name = f"recording_{int(time.time())}.{options.record_format}"
    output_path = recorder.record(
        duration=options.record,
        output=output_name,
        progress_callback=progress if not options.quiet else None
    )
    
    if not options.quiet:
        if RICH_AVAILABLE:
            console.print(f"[green]✓[/green] Saved recording: {output_path}")
        else:
            print(f"Saved recording: {output_path}")
    
    return output_path


def main(*args: str) -> int:
    """Main CLI logic.
    
    Args:
        *args: Command line arguments
        
    Returns:
        Exit code
    """
    cli_args = setup_argument_parser()
    options = cli_args.parse_args(args or None)
    
    # Setup logging
    log_level = "DEBUG" if options.verbose else "INFO"
    setup_logging(log_level=log_level, console_output=not options.quiet)
    
    logger.info(f"PyShotter v{__version__} starting")
    
    try:
        # Handle recording mode
        if hasattr(options, 'record') and options.record:
            if not RECORDING_AVAILABLE:
                print("Error: Recording requires additional dependencies. Install with: pip install pyshotter[recording]")
                return 1
            
            output_path = handle_recording(options)
            
            if options.json:
                output_data = {
                    'type': 'recording',
                    'path': output_path,
                    'duration': options.record,
                    'fps': options.record_fps,
                    'format': options.record_format
                }
                print(json.dumps(output_data, indent=2))
            
            return 0
        
        # Standard screenshot mode
        kwargs = {"mon": options.monitor, "output": options.output}
        
        if options.coordinates:
            try:
                top, left, width, height = options.coordinates.split(",")
            except ValueError:
                print("Coordinates syntax: top,left,width,height")
                return 2
            
            kwargs["mon"] = {
                "top": int(top),
                "left": int(left),
                "width": int(width),
                "height": int(height),
            }
            if options.output == "monitor-{mon}.png":
                kwargs["output"] = "sct-{top}x{left}_{width}x{height}.png"
        
        # Capture screenshot(s)
        files_created = []
        
        with pyshotter(with_cursor=options.with_cursor) as sct:
            if options.coordinates:
                output = kwargs["output"].format(**kwargs["mon"])
                sct_img = sct.grab(kwargs["mon"])
                to_png(sct_img.rgb, sct_img.size, level=options.level, output=output)
                files_created.append(os.path.realpath(output))
            else:
                for file_name in sct.save(**kwargs):
                    files_created.append(os.path.realpath(file_name))
        
        # Process files
        results = []
        for file_path in files_created:
            result = {'path': file_path}
            
            # OCR
            if hasattr(options, 'ocr') and options.ocr:
                if not OCR_AVAILABLE:
                    print("Error: OCR requires additional dependencies. Install with: pip install pyshotter[ocr]")
                    return 1
                result['ocr'] = handle_ocr(file_path, options)
            
            # Redaction
            if hasattr(options, 'redact') and options.redact:
                if not AI_AVAILABLE:
                    print("Error: Redaction requires additional dependencies. Install with: pip install pyshotter[ai]")
                    return 1
                redacted_path = handle_redaction(file_path, options)
                result['redacted_path'] = redacted_path
                file_path = redacted_path  # Use redacted for further processing
            
            # Beautification
            if hasattr(options, 'beautify') and options.beautify:
                if not BEAUTIFIER_AVAILABLE:
                    print("Error: Beautification requires additional dependencies. Install with: pip install pyshotter[annotation]")
                    return 1
                beautified_path = handle_beautify(file_path, options)
                result['beautified_path'] = beautified_path
            
            results.append(result)
            
            # Print path if not quiet and not JSON
            if not options.quiet and not options.json:
                if RICH_AVAILABLE:
                    console.print(f"[green]✓[/green] {file_path}")
                else:
                    print(file_path)
        
        # JSON output
        if options.json:
            print(json.dumps(results, indent=2))
        
        return 0
        
    except ScreenShotError as e:
        if not options.quiet:
            logger.error(f"Screenshot error: {e}")
            if hasattr(e, 'recovery_hint') and e.recovery_hint:
                print(f"Recovery hint: {e.recovery_hint}")
        return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=options.verbose)
        return 1


if __name__ == "__main__":  # pragma: nocover
    import time
    sys.exit(main())
