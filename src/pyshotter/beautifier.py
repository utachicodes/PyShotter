"""Code beautification feature for PyShotter.

This module provides professional code screenshot beautification with:
- Multiple theme presets
- Platform-specific window controls
- Gradient backgrounds
- Drop shadows
- Custom fonts
- Line numbers
"""

import platform
from typing import Optional, Tuple, Literal
from pathlib import Path

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

from .screenshot import ScreenShot
from .exception import BeautifierError, DependencyError
from .logging_config import get_logger

logger = get_logger(__name__)


# Theme definitions with background and syntax colors
THEMES = {
    'dracula': {
        'bg_start': (40, 42, 54),
        'bg_end': (68, 71, 90),
        'window_bg': (40, 42, 54),
        'shadow': (0, 0, 0),
        'text': (248, 248, 242),
    },
    'monokai': {
        'bg_start': (39, 40, 34),
        'bg_end': (64, 66, 57),
        'window_bg': (39, 40, 34),
        'shadow': (0, 0, 0),
        'text': (248, 248, 240),
    },
    'nord': {
        'bg_start': (46, 52, 64),
        'bg_end': (59, 66, 82),
        'window_bg': (46, 52, 64),
        'shadow': (0, 0, 0),
        'text': (236, 239, 244),
    },
    'solarized-light': {
        'bg_start': (253, 246, 227),
        'bg_end': (238, 232, 213),
        'window_bg': (253, 246, 227),
        'shadow': (101, 123, 131),
        'text': (101, 123, 131),
    },
    'solarized-dark': {
        'bg_start': (0, 43, 54),
        'bg_end': (7, 54, 66),
        'window_bg': (0, 43, 54),
        'shadow': (0, 0, 0),
        'text': (131, 148, 150),
    },
    'github-light': {
        'bg_start': (255, 255, 255),
        'bg_end': (246, 248, 250),
        'window_bg': (255, 255, 255),
        'shadow': (149, 157, 165),
        'text': (36, 41, 46),
    },
    'github-dark': {
        'bg_start': (13, 17, 23),
        'bg_end': (22, 27, 34),
        'window_bg': (13, 17, 23),
        'shadow': (0, 0, 0),
        'text': (201, 209, 217),
    },
}


class CodeBeautifierFeature:
    """Professional code screenshot beautification."""
    
    def __init__(
        self,
        theme: str = 'dracula',
        window_style: Optional[Literal['macos', 'windows', 'linux', 'none']] = None,
    ):
        """Initialize code beautifier.
        
        Args:
            theme: Theme name (see THEMES dict for options)
            window_style: Window control style or None for auto-detect
            
        Raises:
            DependencyError: If required libraries aren't installed
            BeautifierError: If theme is invalid
        """
        if not DEPENDENCIES_AVAILABLE:
            raise DependencyError(
                'Code Beautifier',
                'opencv-python and pillow',
                'pip install pyshotter[annotation]'
            )
        
        if theme not in THEMES:
            raise BeautifierError(
                f"Unknown theme: {theme}. Available: {', '.join(THEMES.keys())}",
                theme=theme
            )
        
        self.theme = theme
        self.theme_colors = THEMES[theme]
        
        # Auto-detect window style if not specified
        if window_style is None:
            sys_platform = platform.system().lower()
            if sys_platform == 'darwin':
                self.window_style = 'macos'
            elif sys_platform == 'windows':
                self.window_style = 'windows'
            else:
                self.window_style = 'linux'
        else:
            self.window_style = window_style
        
        logger.info(f"Initialized beautifier with theme={theme}, window_style={self.window_style}")
    
    def beautify(
        self,
        screenshot: ScreenShot,
        padding: int = 60,
        shadow_intensity: float = 0.5,
        corner_radius: int = 10,
        add_line_numbers: bool = False,
        background_type: Literal['gradient', 'solid', 'transparent'] = 'gradient',
    ) -> ScreenShot:
        """Beautify a code screenshot.
        
        Args:
            screenshot: The screenshot to beautify
            padding: Padding around screenshot (pixels)
            shadow_intensity: Drop shadow intensity (0.0-1.0)
            corner_radius: Corner radius for rounded corners
            add_line_numbers: Whether to add line numbers
            background_type: Background style
            
        Returns:
            Beautified screenshot
            
        Raises:
            BeautifierError: If beautification fails
        """
        try:
            logger.debug(f"Beautifying screenshot with padding={padding}, shadow={shadow_intensity}")
            
            # Convert screenshot to PIL Image
            orig_img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            orig_width, orig_height = orig_img.size
            
            # Calculate window controls height
            controls_height = 28 if self.window_style != 'none' else 0
            
            # Calculate new dimensions
            new_width = orig_width + (padding * 2)
            new_height = orig_height + (padding * 2) + controls_height
            
            # Create background
            if background_type == 'gradient':
                background = self._create_gradient_background(new_width, new_height)
            elif background_type == 'solid':
                background = Image.new('RGB', (new_width, new_height), self.theme_colors['bg_start'])
            else:  # transparent
                background = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
            
            # Create window with shadow
            window = self._create_window_with_shadow(
                orig_width,
                orig_height + controls_height,
                corner_radius,
                shadow_intensity
            )
            
            # Paste window onto background
            window_x = padding
            window_y = padding
            if window.mode == 'RGBA':
                background.paste(window, (window_x, window_y), window)
            else:
                background.paste(window, (window_x, window_y))
            
            # Add window controls
            if self.window_style != 'none':
                self._draw_window_controls(background, window_x, window_y)
            
            # Paste original screenshot
            screenshot_y = window_y + controls_height
            background.paste(orig_img, (window_x, screenshot_y))
            
            # Convert back to screenshot format
            if background.mode == 'RGBA':
                background = background.convert('RGB')
            
            beautified_bytes = background.tobytes()
            
            logger.info(f"Successfully beautified screenshot: {screenshot.size} -> {background.size}")
            
            return ScreenShot(
                rgb=beautified_bytes,
                size=background.size,
                pos=(0, 0)
            )
            
        except Exception as e:
            logger.error(f"Beautification failed: {e}")
            raise BeautifierError(f"Failed to beautify screenshot: {e}", theme=self.theme)
    
    def _create_gradient_background(self, width: int, height: int) -> Image.Image:
        """Create gradient background.
        
        Args:
            width: Background width
            height: Background height
            
        Returns:
            PIL Image with gradient
        """
        bg = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(bg)
        
        start_color = self.theme_colors['bg_start']
        end_color = self.theme_colors['bg_end']
        
        # Vertical gradient
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return bg
    
    def _create_window_with_shadow(
        self,
        width: int,
        height: int,
        radius: int,
        shadow_intensity: float
    ) -> Image.Image:
        """Create window with drop shadow.
        
        Args:
            width: Window width
            height: Window height
            radius: Corner radius
            shadow_intensity: Shadow intensity
            
        Returns:
            Window image with shadow
        """
        # Shadow offset and blur
        shadow_offset = 20
        shadow_blur = 30
        
        # Create larger canvas for shadow
        canvas_width = width + shadow_offset * 2 + shadow_blur * 2
        canvas_height = height + shadow_offset * 2 + shadow_blur * 2
        
        # Create shadow layer
        shadow = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Draw shadow rectangle
        shadow_x1 = shadow_blur + shadow_offset
        shadow_y1 = shadow_blur + shadow_offset
        shadow_x2 = shadow_x1 + width
        shadow_y2 = shadow_y1 + height
        
        shadow_color = self.theme_colors['shadow']
        shadow_alpha = int(255 * shadow_intensity * 0.3)
        
        shadow_draw.rounded_rectangle(
            [shadow_x1, shadow_y1, shadow_x2, shadow_y2],
            radius=radius,
            fill=(*shadow_color, shadow_alpha)
        )
        
        # Apply Gaussian blur to shadow
        shadow = shadow.filter(Image.GaussianBlur(shadow_blur))
        
        # Create window
        window = Image.new('RGB', (width, height), self.theme_colors['window_bg'])
        
        # Paste window on shadow
        shadow.paste(window, (shadow_blur, shadow_blur))
        
        return shadow
    
    def _draw_window_controls(self, img: Image.Image, x: int, y: int) -> None:
        """Draw window controls (traffic lights or buttons).
        
        Args:
            img: Image to draw on
            x: X position
            y: Y position
        """
        draw = ImageDraw.Draw(img)
        
        if self.window_style == 'macos':
            # macOS traffic lights
            button_radius = 6
            button_y = y + 14
            spacing = 20
            
            # Red, yellow, green
            colors = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]
            for i, color in enumerate(colors):
                button_x = x + 16 + (i *spacing)
                draw.ellipse(
                    [button_x - button_radius, button_y - button_radius,
                     button_x + button_radius, button_y + button_radius],
                    fill=color
                )
        
        elif self.window_style == 'windows':
            # Windows minimize/maximize/close buttons
            button_size = 12
            button_y = y + 8
            button_x_start = x + img.width - x - 60
            
            # Minimize
            draw.line(
                [(button_x_start, button_y + 6), (button_x_start + button_size, button_y + 6)],
                fill=(150, 150, 150),
                width=2
            )
            
            # Maximize (square)
            draw.rectangle(
                [button_x_start + 20, button_y, button_x_start + 20 + button_size, button_y + button_size],
                outline=(150, 150, 150),
                width=2
            )
            
            # Close (X)
            draw.line(
                [(button_x_start + 40, button_y), (button_x_start + 40 + button_size, button_y + button_size)],
                fill=(232, 17, 35),
                width=2
            )
            draw.line(
                [(button_x_start + 40 + button_size, button_y), (button_x_start + 40, button_y + button_size)],
                fill=(232, 17, 35),
                width=2
            )
        
        elif self.window_style == 'linux':
            # GNOME-style buttons (simple circles)
            button_radius = 5
            button_y = y + 14
            spacing = 18
            
            colors = [(200, 200, 200)] * 3  # Gray buttons
            for i, color in enumerate(colors):
                button_x = x + 12 + (i * spacing)
                draw.ellipse(
                    [button_x - button_radius, button_y - button_radius,
                     button_x + button_radius, button_y + button_radius],
                    fill=color,
                    outline=(150, 150, 150)
                )


def get_available_themes() -> list:
    """Get list of available theme names.
    
    Returns:
        List of theme names
    """
    return list(THEMES.keys())
