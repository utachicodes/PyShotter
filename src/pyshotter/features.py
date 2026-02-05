"""Advanced features for PyShotter.

This module provides advanced screenshot features including:
- OCR text extraction
- Sensitive data redaction
- Multi-monitor panorama
- Change detection
- Hotkey management
- Screenshot history and search
- Annotation tools
- Sharing capabilities
"""

import re
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from .screenshot import ScreenShot


class AnnotationFeature:
    """Smart annotation tools for screenshots."""
    
    def __init__(self):
        if not OPENCV_AVAILABLE:
            raise ImportError("opencv-python is required for annotation features. Install with: pip install opencv-python")
    
    def add_text(self, screenshot: ScreenShot, text: str, position: Tuple[int, int], 
                 font_size: int = 20, color: Tuple[int, int, int] = (255, 0, 0)) -> ScreenShot:
        """Add text annotation to a screenshot.
        
        Args:
            screenshot: The screenshot to annotate
            text: Text to add
            position: (x, y) position for text
            font_size: Font size
            color: RGB color tuple
            
        Returns:
            Annotated screenshot
        """
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        
        # Add text using OpenCV
        cv2.putText(img_array, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_size/30, color, 2)
        
        annotated_rgb = img_array.tobytes()
        return ScreenShot(
            rgb=annotated_rgb,
            size=screenshot.size,
            pos=screenshot.pos
        )
    
    def add_rectangle(self, screenshot: ScreenShot, top_left: Tuple[int, int], 
                     bottom_right: Tuple[int, int], color: Tuple[int, int, int] = (255, 0, 0),
                     thickness: int = 2) -> ScreenShot:
        """Add rectangle annotation to a screenshot.
        
        Args:
            screenshot: The screenshot to annotate
            top_left: Top-left corner (x, y)
            bottom_right: Bottom-right corner (x, y)
            color: RGB color tuple
            thickness: Line thickness
            
        Returns:
            Annotated screenshot
        """
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        
        cv2.rectangle(img_array, top_left, bottom_right, color, thickness)
        
        annotated_rgb = img_array.tobytes()
        return ScreenShot(
            rgb=annotated_rgb,
            size=screenshot.size,
            pos=screenshot.pos
        )
    
    def add_arrow(self, screenshot: ScreenShot, start: Tuple[int, int], end: Tuple[int, int],
                  color: Tuple[int, int, int] = (255, 0, 0), thickness: int = 2) -> ScreenShot:
        """Add arrow annotation to a screenshot.
        
        Args:
            screenshot: The screenshot to annotate
            start: Arrow start point (x, y)
            end: Arrow end point (x, y)
            color: RGB color tuple
            thickness: Line thickness
            
        Returns:
            Annotated screenshot
        """
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        
        cv2.arrowedLine(img_array, start, end, color, thickness)
        
        annotated_rgb = img_array.tobytes()
        return ScreenShot(
            rgb=annotated_rgb,
            size=screenshot.size,
            pos=screenshot.pos
        )
    
    def add_circle(self, screenshot: ScreenShot, center: Tuple[int, int], radius: int,
                   color: Tuple[int, int, int] = (255, 0, 0), thickness: int = 2) -> ScreenShot:
        """Add circle annotation to a screenshot.
        
        Args:
            screenshot: The screenshot to annotate
            center: Circle center (x, y)
            radius: Circle radius
            color: RGB color tuple
            thickness: Line thickness (-1 for filled)
            
        Returns:
            Annotated screenshot
        """
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        
        cv2.circle(img_array, center, radius, color, thickness)
        
        annotated_rgb = img_array.tobytes()
        return ScreenShot(
            rgb=annotated_rgb,
            size=screenshot.size,
            pos=screenshot.pos
        )
    
    def add_highlight(self, screenshot: ScreenShot, region: Tuple[int, int, int, int],
                      color: Tuple[int, int, int] = (255, 255, 0), alpha: float = 0.3) -> ScreenShot:
        """Add highlight overlay to a region.
        
        Args:
            screenshot: The screenshot to annotate
            region: (x, y, width, height) region to highlight
            color: RGB color tuple
            alpha: Transparency (0.0 to 1.0)
            
        Returns:
            Annotated screenshot
        """
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        x, y, w, h = region
        
        # Create overlay
        overlay = img_array.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        
        # Blend with original
        cv2.addWeighted(overlay, alpha, img_array, 1 - alpha, 0, img_array)
        
        annotated_rgb = img_array.tobytes()
        return ScreenShot(
            rgb=annotated_rgb,
            size=screenshot.size,
            pos=screenshot.pos
        )


class SharingFeature:
    """Smart sharing capabilities for screenshots."""
    
    def __init__(self):
        self.clipboard_available = self._check_clipboard()
    
    def _check_clipboard(self) -> bool:
        """Check if clipboard functionality is available."""
        try:
            import pyperclip
            return True
        except ImportError:
            return False
    
    def copy_to_clipboard(self, screenshot: ScreenShot) -> bool:
        """Copy screenshot to clipboard.
        
        Args:
            screenshot: Screenshot to copy
            
        Returns:
            True if successful, False otherwise
        """
        if not self.clipboard_available:
            return False
        
        try:
            import pyperclip
            from PIL import Image
            import io
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            
            # Save to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Copy to clipboard
            pyperclip.copy(img_bytes.getvalue())
            return True
        except Exception:
            return False
    
    def generate_shareable_link(self, screenshot: ScreenShot, service: str = "imgur") -> Optional[str]:
        """Generate a shareable link for the screenshot.
        
        Args:
            screenshot: Screenshot to share
            service: Sharing service ('imgur', 'pastebin', etc.)
            
        Returns:
            Shareable URL or None if failed
        """
        try:
            from PIL import Image
            import io
            import base64
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            
            # Save to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
            
            if service == "imgur":
                # For demo purposes, return a data URL
                return f"data:image/png;base64,{img_base64}"
            else:
                return f"data:image/png;base64,{img_base64}"
                
        except Exception:
            return None
    
    def save_with_metadata(self, screenshot: ScreenShot, filename: str, 
                          metadata: Dict[str, Any] = None) -> bool:
        """Save screenshot with embedded metadata.
        
        Args:
            screenshot: Screenshot to save
            filename: Output filename
            metadata: Metadata to embed
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from PIL import Image, PngInfo
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            
            # Add metadata
            if metadata:
                pnginfo = PngInfo()
                for key, value in metadata.items():
                    pnginfo.add_text(key, str(value))
                img.save(filename, "PNG", pnginfo=pnginfo)
            else:
                img.save(filename, "PNG")
            
            return True
        except Exception:
            return False


class SmartDetectionFeature:
    """Smart detection features for screenshots."""
    
    def __init__(self):
        if not OPENCV_AVAILABLE:
            raise ImportError("opencv-python is required for smart detection. Install with: pip install opencv-python")
    
    def detect_code_regions(self, screenshot: ScreenShot) -> List[Dict[str, Any]]:
        """Detect code-like regions in screenshots.
        
        Args:
            screenshot: Screenshot to analyze
            
        Returns:
            List of detected code regions with bounding boxes
        """
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Detect text-like regions (simple approach)
        # In a real implementation, you'd use more sophisticated OCR/text detection
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        code_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 20:  # Filter small regions
                code_regions.append({
                    'bbox': (x, y, w, h),
                    'area': w * h,
                    'confidence': 0.8  # Placeholder confidence
                })
        
        return code_regions
    
    def detect_windows(self, screenshot: ScreenShot) -> List[Dict[str, Any]]:
        """Detect application windows in screenshots.
        
        Args:
            screenshot: Screenshot to analyze
            
        Returns:
            List of detected windows with bounding boxes
        """
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Detect edges
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        windows = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100 and h > 50:  # Filter small regions
                windows.append({
                    'bbox': (x, y, w, h),
                    'area': w * h
                })
        
        return windows


class OCRFeature:
    """OCR (Optical Character Recognition) feature for extracting text from screenshots."""
    
    def __init__(self):
        if not TESSERACT_AVAILABLE:
            raise ImportError("pytesseract is required for OCR features. Install with: pip install pytesseract")
    
    def extract_text(self, screenshot: ScreenShot, lang: str = 'eng') -> str:
        """Extract text from a screenshot using OCR.
        
        Args:
            screenshot: The screenshot to extract text from
            lang: Language code for OCR (default: 'eng')
            
        Returns:
            Extracted text as string
        """
        # Convert screenshot to PIL Image for OCR
        from PIL import Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    
    def extract_text_boxes(self, screenshot: ScreenShot, lang: str = 'eng') -> List[Dict[str, Any]]:
        """Extract text with bounding boxes from a screenshot.
        
        Args:
            screenshot: The screenshot to extract text from
            lang: Language code for OCR (default: 'eng')
            
        Returns:
            List of dictionaries with text and bounding box information
        """
        from PIL import Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        
        # Get detailed OCR data
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        
        results = []
        for i in range(len(data['text'])):
            if data['conf'][i] > 0:  # Filter out low confidence results
                results.append({
                    'text': data['text'][i],
                    'confidence': data['conf'][i],
                    'bbox': (data['left'][i], data['top'][i], 
                            data['left'][i] + data['width'][i], 
                            data['top'][i] + data['height'][i])
                })
        
        return results


class RedactionFeature:
    """Sensitive data redaction feature for screenshots."""
    
    def __init__(self):
        if not OPENCV_AVAILABLE:
            raise ImportError("opencv-python is required for redaction features. Install with: pip install opencv-python")
    
    def redact_sensitive_data(self, screenshot: ScreenShot) -> ScreenShot:
        """Redact sensitive data from a screenshot.
        
        Args:
            screenshot: The screenshot to redact
            
        Returns:
            New screenshot with sensitive data redacted
        """
        # Convert to numpy array
        img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
        
        # Extract text to find sensitive data
        ocr = OCRFeature()
        text_boxes = ocr.extract_text_boxes(screenshot)
        
        # Patterns for sensitive data
        patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b'
        }
        
        # Redact sensitive data
        for box in text_boxes:
            text = box['text']
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, text):
                    # Blur the bounding box area
                    x1, y1, x2, y2 = box['bbox']
                    img_array[y1:y2, x1:x2] = cv2.GaussianBlur(
                        img_array[y1:y2, x1:x2], (15, 15), 0
                    )
        
        # Convert back to screenshot format
        redacted_rgb = img_array.tobytes()
        return ScreenShot(
            rgb=redacted_rgb,
            size=screenshot.size,
            pos=screenshot.pos
        )


class PanoramaFeature:
    """Multi-monitor panorama feature for stitching screenshots."""
    
    def create_panorama(self, screenshots: List[ScreenShot]) -> ScreenShot:
        """Create a panoramic image from multiple monitor screenshots.
        
        Args:
            screenshots: List of screenshots from different monitors
            
        Returns:
            Panoramic screenshot
        """
        if not screenshots:
            raise ValueError("At least one screenshot is required")
        
        # Calculate total width and max height
        total_width = sum(s.width for s in screenshots)
        max_height = max(s.height for s in screenshots)
        
        # Create panoramic image
        panorama_array = np.zeros((max_height, total_width, 3), dtype=np.uint8)
        
        x_offset = 0
        for screenshot in screenshots:
            img_array = np.array(screenshot.rgb).reshape(screenshot.height, screenshot.width, 3)
            panorama_array[:screenshot.height, x_offset:x_offset + screenshot.width] = img_array
            x_offset += screenshot.width
        
        # Convert back to screenshot format
        panorama_rgb = panorama_array.tobytes()
        return ScreenShot(
            rgb=panorama_rgb,
            size=(total_width, max_height),
            pos=(0, 0)
        )


class ChangeDetectionFeature:
    """Change detection feature for comparing screenshots."""
    
    def __init__(self):
        if not OPENCV_AVAILABLE:
            raise ImportError("opencv-python is required for change detection. Install with: pip install opencv-python")
    
    def detect_changes(self, current: ScreenShot, previous: ScreenShot, 
                      threshold: float = 0.1) -> ScreenShot:
        """Detect changes between two screenshots.
        
        Args:
            current: Current screenshot
            previous: Previous screenshot
            threshold: Sensitivity threshold for change detection
            
        Returns:
            Screenshot highlighting changes
        """
        # Convert to numpy arrays
        current_array = np.array(current.rgb).reshape(current.height, current.width, 3)
        previous_array = np.array(previous.rgb).reshape(previous.height, previous.width, 3)
        
        # Convert to grayscale for comparison
        current_gray = cv2.cvtColor(current_array, cv2.COLOR_RGB2GRAY)
        previous_gray = cv2.cvtColor(previous_array, cv2.COLOR_RGB2GRAY)
        
        # Calculate difference
        diff = cv2.absdiff(current_gray, previous_gray)
        
        # Apply threshold
        _, thresh = cv2.threshold(diff, int(255 * threshold), 255, cv2.THRESH_BINARY)
        
        # Find contours of changes
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw red rectangles around changes
        result_array = current_array.copy()
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filter small changes
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(result_array, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Convert back to screenshot format
        result_rgb = result_array.tobytes()
        return ScreenShot(
            rgb=result_rgb,
            size=current.size,
            pos=current.pos
        )


class HotkeyManager:
    """Global hotkey manager for screenshot triggers."""
    
    def __init__(self):
        self.hotkeys = {}
        self._running = False
    
    def register_hotkey(self, key_combination: str, callback: callable) -> None:
        """Register a global hotkey.
        
        Args:
            key_combination: Hotkey combination (e.g., 'ctrl+shift+s')
            callback: Function to call when hotkey is pressed
        """
        self.hotkeys[key_combination] = callback
    
    def unregister_hotkey(self, key_combination: str) -> None:
        """Unregister a global hotkey.
        
        Args:
            key_combination: Hotkey combination to unregister
        """
        if key_combination in self.hotkeys:
            del self.hotkeys[key_combination]
    
    def start_listening(self) -> None:
        """Start listening for hotkeys."""
        # Implementation would depend on platform-specific libraries
        # For now, this is a placeholder
        self._running = True
    
    def stop_listening(self) -> None:
        """Stop listening for hotkeys."""
        self._running = False


class ScreenshotHistory:
    """Screenshot history and search functionality."""
    
    def __init__(self, history_dir: str = "~/.pyshotter/history"):
        self.history_dir = Path(history_dir).expanduser()
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.history_dir / "history.json"
        self._load_history()
    
    def _load_history(self) -> None:
        """Load screenshot history from file."""
        import json
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def _save_history(self) -> None:
        """Save screenshot history to file."""
        import json
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_screenshot(self, screenshot: ScreenShot, metadata: Dict[str, Any] = None) -> str:
        """Add a screenshot to history.
        
        Args:
            screenshot: The screenshot to add
            metadata: Additional metadata (window title, tags, etc.)
            
        Returns:
            Screenshot ID
        """
        import hashlib
        
        # Generate unique ID
        screenshot_id = hashlib.md5(f"{time.time()}".encode()).hexdigest()[:8]
        
        # Save screenshot
        screenshot_path = self.history_dir / f"{screenshot_id}.png"
        screenshot.save(str(screenshot_path))
        
        # Extract text if OCR is available
        ocr_text = ""
        if TESSERACT_AVAILABLE:
            try:
                ocr = OCRFeature()
                ocr_text = ocr.extract_text(screenshot)
            except:
                pass
        
        # Create history entry
        entry = {
            'id': screenshot_id,
            'timestamp': datetime.now().isoformat(),
            'path': str(screenshot_path),
            'size': screenshot.size,
            'ocr_text': ocr_text,
            'metadata': metadata or {}
        }
        
        self.history.append(entry)
        self._save_history()
        
        return screenshot_id
    
    def search_history(self, query: str) -> List[Dict[str, Any]]:
        """Search screenshot history.
        
        Args:
            query: Search query (searches in OCR text, metadata, and tags)
            
        Returns:
            List of matching screenshot entries
        """
        results = []
        query_lower = query.lower()
        
        for entry in self.history:
            # Search in OCR text
            if query_lower in entry.get('ocr_text', '').lower():
                results.append(entry)
                continue
            
            # Search in metadata
            metadata_str = json.dumps(entry.get('metadata', {})).lower()
            if query_lower in metadata_str:
                results.append(entry)
                continue
            
            # Search in tags
            tags = entry.get('metadata', {}).get('tags', [])
            if any(query_lower in tag.lower() for tag in tags):
                results.append(entry)
        
        return results
    
    def get_screenshot(self, screenshot_id: str) -> Optional[ScreenShot]:
        """Get a screenshot from history by ID.
        
        Args:
            screenshot_id: ID of the screenshot to retrieve
            
        Returns:
            Screenshot object or None if not found
        """
        for entry in self.history:
            if entry['id'] == screenshot_id:
                screenshot_path = Path(entry['path'])
                if screenshot_path.exists():
                    # Load screenshot from file
                    # This would need to be implemented based on your screenshot loading method
                    return None  # Placeholder
        return None 