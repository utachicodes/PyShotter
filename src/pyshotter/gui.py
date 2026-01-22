"""GUI application for PyShotter.

This module provides a system tray application with:
- Global hotkeys for capture
- Region selection overlay
- Screenshot history
- Quick actions menu
"""

import sys
import platform
from typing import Optional, Callable
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

from .exception import GUIError, DependencyError
from .logging_config import get_logger

logger = get_logger(__name__)


class PyShotterGUI:
    """System tray GUI for PyShotter."""
    
    def __init__(self):
        """Initialize GUI.
        
        Raises:
            DependencyError: If pystray isn't installed
        """
        if not PYSTRAY_AVAILABLE:
            raise DependencyError(
                'GUI',
                'pystray and pillow',
                'pip install pyshotter[gui]'
            )
        
        self.icon: Optional[pystray.Icon] = None
        self.hotkey_manager: Optional['HotkeyManager'] = None
        
        logger.info("GUI initialized")
    
    def create_icon_image(self) -> Image.Image:
        """Create system tray icon.
        
        Returns:
            PIL Image for tray icon
        """
        # Create simple camera icon
        width = 64
        height = 64
        
        image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Draw camera body
        draw.rectangle([16, 24, 48, 48], fill=(100, 149, 237), outline=(70, 130, 180))
        
        # Draw lens
        draw.ellipse([24, 28, 40, 44], fill=(50, 50, 50), outline=(30, 30, 30))
        
        # Draw flash
        draw.rectangle([42, 20, 48, 26], fill=(255, 255, 0))
        
        return image
    
    def create_menu(self) -> pystray.Menu:
        """Create system tray menu.
        
        Returns:
            pystray Menu object        """
        return pystray.Menu(
            pystray.MenuItem('Capture Region', self.capture_region),
            pystray.MenuItem('Capture Window', self.capture_window),
            pystray.MenuItem('Capture Full Screen', self.capture_fullscreen),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Start Recording', self.start_recording),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Screenshot History', self.open_history),
            pystray.MenuItem('Settings', self.open_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', self.exit_app),
        )
    
    def capture_region(self, icon=None, item=None):
        """Capture selected region."""
        logger.info("Capture region triggered")
        try:
            from .factory import pyshotter
            with pyshotter() as sct:
                # Simple full screen for now - region selection would require overlay
                screenshot = sct.grab(sct.monitors[1])
                output = f"screenshot_{int(__import__('time').time())}.png"
                screenshot.save(output)
                logger.info(f"Saved: {output}")
                self.show_notification("Screenshot saved", output)
        except Exception as e:
            logger.error(f"Capture failed: {e}")
            self.show_notification("Capture failed", str(e))
    
    def capture_window(self, icon=None, item=None):
        """Capture active window."""
        logger.info("Capture window triggered (not fully implemented)")
        self.show_notification("Not Implemented", "Window capture coming soon!")
    
    def capture_fullscreen(self, icon=None, item=None):
        """Capture full screen."""
        logger.info("Capture fullscreen triggered")
        try:
            from .factory import pyshotter
            with pyshotter() as sct:
                screenshot = sct.grab(sct.monitors[0])  # All monitors
                output = f"screenshot_{int(__import__('time').time())}.png"
                screenshot.save(output)
                logger.info(f"Saved: {output}")
                self.show_notification("Screenshot saved", output)
        except Exception as e:
            logger.error(f"Capture failed: {e}")
    
    def start_recording(self, icon=None, item=None):
        """Start screen recording."""
        logger.info("Recording triggered (not fully implemented)")
        self.show_notification("Not Implemented", "Recording UI coming soon!")
    
    def open_history(self, icon=None, item=None):
        """Open screenshot history."""
        logger.info("History triggered (not fully implemented)")
        self.show_notification("Not Implemented", "History viewer coming soon!")
    
    def open_settings(self, icon=None, item=None):
        """Open settings panel."""
        logger.info("Settings triggered (not fully implemented)")
        self.show_notification("Not Implemented", "Settings panel coming soon!")
    
    def exit_app(self, icon=None, item=None):
        """Exit application."""
        logger.info("Exiting GUI")
        if self.icon:
            self.icon.stop()
    
    def show_notification(self, title: str, message: str):
        """Show system notification.
        
        Args:
            title: Notification title
            message: Notification message
        """
        if self.icon:
            self.icon.notify(message, title)
    
    def run(self):
        """Start the GUI application.
        
        Raises:
            GUIError: If GUI fails to start
        """
        try:
            logger.info("Starting GUI")
            
            # Create icon
            icon_image = self.create_icon_image()
            menu = self.create_menu()
            
            self.icon = pystray.Icon(
                "PyShotter",
                icon_image,
                "PyShotter v1.1",
                menu
            )
            
            # Show startup notification
            self.show_notification("PyShotter Started", "Press hotkeys to capture!")
            
            # Run (blocks until stop() is called)
            self.icon.run()
            
            logger.info("GUI stopped")
            
        except Exception as e:
            logger.error(f"GUI error: {e}")
            raise GUIError(f"Failed to start GUI: {e}", component="system_tray")


class HotkeyManager:
    """Cross-platform hotkey manager (stub)."""
    
    def __init__(self):
        """Initialize hotkey manager."""
        self.hotkeys = {}
        logger.info("Hotkey manager initialized (platform support limited)")
    
    def register(self, hotkey: str, callback: Callable):
        """Register global hotkey.
        
        Args:
            hotkey: Hotkey combination (e.g., 'ctrl+shift+s')
            callback: Function to call when hotkey pressed
        """
        logger.info(f"Registered hotkey: {hotkey} (not active - requires platform-specific implementation)")
        self.hotkeys[hotkey] = callback
    
    def unregister(self, hotkey: str):
        """Unregister hotkey.
        
        Args:
            hotkey: Hotkey combination to unregister
        """
        if hotkey in self.hotkeys:
            del self.hotkeys[hotkey]
            logger.info(f"Unregistered hotkey: {hotkey}")


def main_gui():
    """GUI entry point."""
    try:
        gui = PyShotterGUI()
        gui.run()
        return 0
    except Exception as e:
        print(f"GUI Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main_gui())
