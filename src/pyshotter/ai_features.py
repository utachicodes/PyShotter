"""AI-powered editing features for PyShotter.

This module provides:
- Enhanced sensitive data redaction
- Face detection and blurring
- Privacy templates (HIPAA, GDPR, etc.)
"""

import re
from typing import List, Dict, Optional, Literal, Tuple
from pathlib import Path

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    from PIL import Image, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from .screenshot import ScreenShot
from .exception import DependencyError
from .logging_config import get_logger

logger = get_logger(__name__)

# Privacy templates with PII patterns
PRIVACY_TEMPLATES = {
    'medical': {
        'patterns': {
            'mrn': r'\b[A-Z]{2}\d{6,8}\b',
            'dob': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        },
        'description': 'HIPAA-compliant medical record redaction'
    },
    'financial': {
        'patterns': {
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'cvv': r'\b\d{3,4}\b',
            'account': r'\b\d{8,17}\b',
            'routing': r'\b\d{9}\b',
        },
        'description': 'PCI-DSS financial data redaction'
    },
    'government': {
        'patterns': {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'passport': r'\b[A-Z]{1,2}\d{6,9}\b',
            'license': r'\b[A-Z]\d{7,8}\b',
        },
        'description': 'Government ID redaction'
    },
    'corporate': {
        'patterns': {
            'employee_id': r'\bEMP\d{4,6}\b',
            'internal_id': r'\b[A-Z]{2,3}-\d{4,6}\b',
        },
        'description': 'Corporate internal data redaction'
    },
    'gdpr': {
        'patterns': {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',
            'ip': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        },
        'description': 'EU GDPR compliance redaction'
    },
}


class EnhancedRedactionFeature:
    """Enhanced redaction with multiple modes and templates."""
    
    def __init__(
        self,
        mode: Literal['blur', 'pixelate', 'block', 'generate'] = 'blur',
    ):
        """Initialize redaction feature.
        
        Args:
            mode: Redaction mode
            
        Raises:
            DependencyError: If required libraries aren't installed
        """
        if not OPENCV_AVAILABLE or not PIL_AVAILABLE:
            raise DependencyError(
                'Enhanced Redaction',
                'opencv-python and pillow',
                'pip install pyshotter[ai]'
            )
        
        self.mode = mode
        self.custom_patterns: Dict[str, str] = {}
        
        logger.info(f"Initialized redaction with mode={mode}")
    
    def add_custom_patterns(self, patterns: Dict[str, str]) -> None:
        """Add custom regex patterns for redaction.
        
        Args:
            patterns: Dict of pattern_name: regex_pattern
        """
        self.custom_patterns.update(patterns)
        logger.info(f"Added {len(patterns)} custom patterns")
    
    def redact_with_template(
        self,
        screenshot: ScreenShot,
        template: Literal['medical', 'financial', 'government', 'corporate', 'gdpr'],
    ) -> ScreenShot:
        """Redact using privacy template.
        
        Args:
            screenshot: Screenshot to redact
            template: Privacy template name
            
        Returns:
            Redacted screenshot
        """
        if template not in PRIVACY_TEMPLATES:
            raise ValueError(f"Unknown template: {template}")
        
        patterns = PRIVACY_TEMPLATES[template]['patterns']
        logger.info(f"Redacting with template: {template}")
        
        return self.redact_sensitive_data(screenshot, list(patterns.keys()), patterns)
    
    def redact_sensitive_data(
        self,
        screenshot: ScreenShot,
        pattern_types: Optional[List[str]] = None,
        custom_patterns: Optional[Dict[str, str]] = None,
        blur_strength: float = 15.0,
    ) -> ScreenShot:
        """Redact sensitive data from screenshot.
        
        Args:
            screenshot: Screenshot to redact
            pattern_types: List of pattern types to redact
            custom_patterns: Optional custom regex patterns
            blur_strength: Blur strength for blur mode
            
        Returns:
            Redacted screenshot
        """
        try:
            # Convert to PIL Image for OCR
            from .features import OCRFeature
            
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            img_array = np.array(img)
            
            # Extract text boxes using OCR
            try:
                ocr = OCRFeature()
                text_boxes = ocr.extract_text_boxes(screenshot)
            except Exception as e:
                logger.warning(f"OCR failed, skipping text detection: {e}")
                text_boxes = []
            
            # Build pattern dict
            all_patterns = {}
            
            # Add default patterns
            default_patterns = {
                'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
                'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            }
            
            if pattern_types:
                for ptype in pattern_types:
                    if ptype in default_patterns:
                        all_patterns[ptype] = default_patterns[ptype]
            else:
                all_patterns = default_patterns
            
            # Add custom patterns
            if custom_patterns:
                all_patterns.update(custom_patterns)
            if self.custom_patterns:
                all_patterns.update(self.custom_patterns)
            
            # Find and redact matches
            redacted_count = 0
            for box in text_boxes:
                text = box['text']
                bbox = box['bbox']
                
                for pattern_name, pattern in all_patterns.items():
                    if re.search(pattern, text):
                        logger.debug(f"Found {pattern_name} match, redacting")
                        img_array = self._apply_redaction(
                            img_array,
                            bbox,
                            blur_strength
                        )
                        redacted_count += 1
                        break
            
            logger.info(f"Redacted {redacted_count} sensitive items")
            
            # Convert back to screenshot
            redacted_img = Image.fromarray(img_array)
            redacted_bytes = redacted_img.tobytes()
            
            return ScreenShot(
                rgb=redacted_bytes,
                size=screenshot.size,
                pos=screenshot.pos
            )
            
        except Exception as e:
            logger.error(f"Redaction failed: {e}")
            return screenshot  # Return original on error
    
    def _apply_redaction(
        self,
        img_array: np.ndarray,
        bbox: Tuple[int, int, int, int],
        strength: float
    ) -> np.ndarray:
        """Apply redaction to region.
        
        Args:
            img_array: Image array
            bbox: Bounding box (x1, y1, x2, y2)
            strength: Redaction strength
            
        Returns:
            Modified image array
        """
        x1, y1, x2, y2 = bbox
        x1, y1, x2, y2 = max(0, x1), max(0, y1), min(img_array.shape[1], x2), min(img_array.shape[0], y2)
        
        if x2 <= x1 or y2 <= y1:
            return img_array
        
        region = img_array[y1:y2, x1:x2]
        
        if self.mode == 'blur':
            # Gaussian blur
            ksize = int(strength) | 1  # Ensure odd
            region = cv2.GaussianBlur(region, (ksize, ksize), 0)
        
        elif self.mode == 'pixelate':
            # Pixelation
            h, w = region.shape[:2]
            pixel_size = max(8, int(strength))
            temp = cv2.resize(region, (max(1, w // pixel_size), max(1, h // pixel_size)), interpolation=cv2.INTER_LINEAR)
            region = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        
        elif self.mode == 'block':
            # Solid block
            region[:] = (0, 0, 0)
        
        elif self.mode == 'generate':
            # Simple block pattern (more advanced generation would require AI)
            region[:] = (50, 50, 50)
            for i in range(0, region.shape[0], 4):
                region[i:i+2, :] = (70, 70, 70)
        
        img_array[y1:y2, x1:x2] = region
        return img_array


class FaceBlurFeature:
    """Face detection and blurring for privacy."""
    
    def __init__(
        self,
        detection_method: Literal['haar', 'dnn'] = 'haar',
        blur_strength: float = 30.0,
        expand_ratio: float = 1.2,
    ):
        """Initialize face blur feature.
        
        Args:
            detection_method: Detection method (haar cascade or DNN)
            blur_strength: Blur strength
            expand_ratio: Ratio to expand blur region around face
            
        Raises:
            DependencyError: If OpenCV isn't installed
        """
        if not OPENCV_AVAILABLE:
            raise DependencyError(
                'Face Blur',
                'opencv-python',
                'pip install pyshotter[ai]'
            )
        
        self.detection_method = detection_method
        self.blur_strength = blur_strength
        self.expand_ratio = expand_ratio
        
        self.face_cascade = None
        self.dnn_net = None
        
        # Load appropriate detector
        if detection_method == 'haar':
            self._load_haar_detector()
            logger.info("Loaded Haar cascade face detector")
        else:  # dnn
            if not self._load_dnn_detector():
                # Fallback to Haar if DNN model not available
                logger.warning("DNN model not available, falling back to Haar cascade")
                self._load_haar_detector()
                self.detection_method = 'haar'
            else:
                logger.info("Loaded DNN face detector")
    
    def _load_haar_detector(self):
        """Load Haar cascade detector."""
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
    
    def _load_dnn_detector(self) -> bool:
        """Load DNN face detector.
        
        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            # Try to load pre-trained DNN model
            # Using OpenCV's DNN module with Caffe model
            from pathlib import Path
            import urllib.request
            
            model_dir = Path.home() / '.pyshotter' / 'models'
            model_dir.mkdir(parents=True, exist_ok=True)
            
            prototxt_path = model_dir / 'deploy.prototxt'
            model_path = model_dir / 'res10_300x300_ssd_iter_140000.caffemodel'
            
            # Download models if not present
            if not prototxt_path.exists():
                logger.info("Downloading DNN prototxt...")
                prototxt_url = 'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt'
                urllib.request.urlretrieve(prototxt_url, prototxt_path)
            
            if not model_path.exists():
                logger.info("Downloading DNN model (may take a moment)...")
                model_url = 'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel'
                urllib.request.urlretrieve(model_url, model_path)
            
            # Load the model
            self.dnn_net = cv2.dnn.readNetFromCaffe(str(prototxt_path), str(model_path))
            return True
            
        except Exception as e:
            logger.warning(f"Failed to load DNN model: {e}")
            return False
    
    def detect_faces(self, screenshot: ScreenShot) -> List[Dict]:
        """Detect faces in screenshot.
        
        Args:
            screenshot: Screenshot to analyze
            
        Returns:
            List of face info dicts with bbox and confidence
        """
        try:
            # Convert to array
            img_array = np.frombuffer(screenshot.rgb, dtype=np.uint8)
            img_array = img_array.reshape(screenshot.height, screenshot.width, 3)
            
            if self.detection_method == 'dnn' and self.dnn_net is not None:
                # DNN detection
                blob = cv2.dnn.blobFromImage(
                    img_array, 1.0, (300, 300),
                    (104.0, 177.0, 123.0)
                )
                self.dnn_net.setInput(blob)
                detections = self.dnn_net.forward()
                
                results = []
                h, w = img_array.shape[:2]
                
                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    
                    if confidence > 0.5:  # Confidence threshold
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (x, y, x2, y2) = box.astype("int")
                        
                        # Convert to x, y, w, h format
                        results.append({
                            'bbox': (x, y, x2 - x, y2 - y),
                            'confidence': float(confidence)
                        })
                
                logger.info(f"DNN detected {len(results)} faces")
                return results
            
            else:
                # Haar cascade detection
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                results = []
                for (x, y, w, h) in faces:
                    results.append({
                        'bbox': (x, y, w, h),
                        'confidence': 0.9  # Haar doesn't provide confidence
                    })
                
                logger.info(f"Haar detected {len(results)} faces")
                return results
            
        except Exception as e:
            logger.error(f"Face detection failed: {e}")
            return []
    
    def blur_faces(
        self,
        screenshot: ScreenShot,
        exclude_faces: Optional[List[str]] = None,
    ) -> ScreenShot:
        """Blur detected faces in screenshot.
        
        Args:
            screenshot: Screenshot to process
            exclude_faces: Optional list of face IDs to exclude (not implemented)
            
        Returns:
            Screenshot with blurred faces
        """
        try:
            # Detect faces
            faces = self.detect_faces(screenshot)
            
            if not faces:
                logger.info("No faces detected")
                return screenshot
            
            # Convert to array
            img_array = np.frombuffer(screenshot.rgb, dtype=np.uint8)
            img_array = img_array.reshape(screenshot.height, screenshot.width, 3).copy()
            
            # Blur each face
            for face in faces:
                x, y, w, h = face['bbox']
                
                # Expand region
                expand_w = int(w * (self.expand_ratio - 1) / 2)
                expand_h = int(h * (self.expand_ratio - 1) / 2)
                
                x1 = max(0, x - expand_w)
                y1 = max(0, y - expand_h)
                x2 = min(img_array.shape[1], x + w + expand_w)
                y2 = min(img_array.shape[0], y + h + expand_h)
                
                # Extract and blur region
                face_region = img_array[y1:y2, x1:x2]
                ksize = int(self.blur_strength) | 1  # Ensure odd
                blurred = cv2.GaussianBlur(face_region, (ksize, ksize), 0)
                
                # Put back
                img_array[y1:y2, x1:x2] = blurred
            
            logger.info(f"Blurred {len(faces)} faces")
            
            # Convert back to screenshot
            blurred_bytes = img_array.tobytes()
            return ScreenShot(
                rgb=blurred_bytes,
                size=screenshot.size,
                pos=screenshot.pos
            )
            
        except Exception as e:
            logger.error(f"Face blurring failed: {e}")
            return screenshot


def get_privacy_templates() -> Dict[str, Dict]:
    """Get available privacy templates.
    
    Returns:
        Dict of template_name: template_info
    """
    return PRIVACY_TEMPLATES.copy()
