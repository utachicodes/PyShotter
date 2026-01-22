"""Region selection and GUI components for PyShotter."""

import sys
from typing import Optional, Tuple, Callable

try:
    from PIL import Image, ImageDraw, ImageTk
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

from .exception import GUIError
from .logging_config import get_logger

logger = get_logger(__name__)


class RegionSelector:
    """Interactive region selection overlay."""
    
    def __init__(self):
        """Initialize region selector."""
        if not TKINTER_AVAILABLE:
            raise GUIError("Tkinter not available", component="region_selector")
        
        self.root = None
        self.canvas = None
        self.selected_region: Optional[Tuple[int, int, int, int]] = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        
    def select_region(self, callback: Optional[Callable] = None) -> Optional[Tuple[int, int, int, int]]:
        """Show overlay and let user select region.
        
        Args:
            callback: Optional callback when region selected
            
        Returns:
            Tuple of (x, y, width, height) or None if cancelled
        """
        try:
            # Create fullscreen window
            self.root = tk.Tk()
            self.root.attributes('-fullscreen', True)
            self.root.attributes('-alpha', 0.3)  # Semi-transparent
            self.root.configure(background='black')
            
            # Create canvas
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            self.canvas = tk.Canvas(
                self.root,
                width=screen_width,
                height=screen_height,
                highlightthickness=0,
                bg='black'
            )
            self.canvas.pack()
            
            # Bind mouse events
            self.canvas.bind('<Button-1>', self._on_mouse_down)
            self.canvas.bind('<B1-Motion>', self._on_mouse_move)
            self.canvas.bind('<ButtonRelease-1>', self._on_mouse_up)
            
            # Bind escape key
            self.root.bind('<Escape>', lambda e: self.root.destroy())
            
            # Add instructions
            self.canvas.create_text(
                screen_width // 2,
                50,
                text="Drag to select region. Press ESC to cancel.",
                fill='white',
                font=('Arial', 16)
            )
            
            self.root.mainloop()
            
            if callback and self.selected_region:
                callback(self.selected_region)
            
            return self.selected_region
            
        except Exception as e:
            logger.error(f"Region selection failed: {e}")
            raise GUIError(f"Region selection failed: {e}", component="region_selector")
    
    def _on_mouse_down(self, event):
        """Handle mouse down event."""
        self.start_x = event.x
        self.start_y = event.y
        
        # Create rectangle
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red',
            width=2
        )
    
    def _on_mouse_move(self, event):
        """Handle mouse move event."""
        if self.rect:
            # Update rectangle
            self.canvas.coords(
                self.rect,
                self.start_x, self.start_y,
                event.x, event.y
            )
            
            # Show dimensions
            width = abs(event.x - self.start_x)
            height = abs(event.y - self.start_y)
            
            # Update or create dimension text
            if hasattr(self, 'dim_text'):
                self.canvas.delete(self.dim_text)
            
            self.dim_text = self.canvas.create_text(
                event.x + 10, event.y + 10,
                text=f"{width} x {height}",
                fill='white',
                font=('Arial', 12)
            )
    
    def _on_mouse_up(self, event):
        """Handle mouse up event."""
        # Calculate region
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        width = x2 - x1
        height = y2 - y1
        
        if width > 10 and height > 10:  # Minimum size
            self.selected_region = (x1, y1, width, height)
            logger.info(f"Selected region: {self.selected_region}")
        
        # Close window
        if self.root:
            self.root.destroy()


class ScreenshotHistoryViewer:
    """Simple screenshot history viewer."""
    
    def __init__(self, history_dir: str = "~/.pyshotter/history"):
        """Initialize history viewer.
        
        Args:
            history_dir: Directory containing screenshot history
        """
        if not TKINTER_AVAILABLE:
            raise GUIError("Tkinter not available", component="history_viewer")
        
        from pathlib import Path
        self.history_dir = Path(history_dir).expanduser()
        self.root = None
        
    def show(self):
        """Show history viewer window."""
        try:
            self.root = tk.Tk()
            self.root.title("PyShotter History")
            self.root.geometry("800x600")
            
            # Create scrollable frame
            canvas = tk.Canvas(self.root)
            scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Load screenshots
            self._load_screenshots(scrollable_frame)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"History viewer failed: {e}")
            raise GUIError(f"History viewer failed: {e}", component="history_viewer")
    
    def _load_screenshots(self, parent):
        """Load screenshots into viewer.
        
        Args:
            parent: Parent widget
        """
        import json
        
        history_file = self.history_dir / "history.json"
        
        if not history_file.exists():
            label = tk.Label(parent, text="No history found", font=('Arial', 14))
            label.pack(pady=20)
            return
        
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            for entry in history[-20:]:  # Show last 20
                self._create_history_entry(parent, entry)
                
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            label = tk.Label(parent, text=f"Error loading history: {e}")
            label.pack(pady=20)
    
    def _create_history_entry(self, parent, entry):
        """Create widget for history entry.
        
        Args:
            parent: Parent widget
            entry: History entry dict
        """
        frame = tk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Timestamp
        timestamp = entry.get('timestamp', 'Unknown')
        tk.Label(frame, text=timestamp, font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=5)
        
        # Path
        path = entry.get('path', '')
        tk.Label(frame, text=path, font=('Arial', 9)).pack(anchor=tk.W, padx=5)
        
        # Size
        size = entry.get('size', (0, 0))
        tk.Label(frame, text=f"Size: {size[0]}x{size[1]}", font=('Arial', 9)).pack(anchor=tk.W, padx=5)


def select_region_interactive() -> Optional[Tuple[int, int, int, int]]:
    """Launch interactive region selector.
    
    Returns:
        Selected region or None
    """
    selector = RegionSelector()
    return selector.select_region()


def show_history():
    """Launch history viewer."""
    viewer = ScreenshotHistoryViewer()
    viewer.show()
