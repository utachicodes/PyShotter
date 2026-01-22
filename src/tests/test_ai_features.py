"""Unit tests for AI features (redaction and face blurring)."""

import pytest
import numpy as np

from pyshotter.screenshot import ScreenShot
from pyshotter.ai_features import (
    EnhancedRedactionFeature,
    FaceBlurFeature,
    get_privacy_templates,
    PRIVACY_TEMPLATES
)


class TestEnhancedRedaction:
    """Test enhanced redaction feature."""
    
    @pytest.fixture
    def sample_screenshot(self):
        """Create sample screenshot."""
        img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        return ScreenShot(rgb=img_array.tobytes(), size=(100, 100), pos=(0, 0))
    
    def test_redaction_init(self):
        """Test redaction feature initialization."""
        for mode in ['blur', 'pixelate', 'block', 'generate']:
            redactor = EnhancedRedactionFeature(mode=mode)
            assert redactor.mode == mode
    
    def test_add_custom_patterns(self):
        """Test adding custom patterns."""
        redactor = EnhancedRedactionFeature()
        
        custom_patterns = {
            'api_key': r'sk-[A-Za-z0-9]{48}',
            'jwt': r'eyJ[A-Za-z0-9-_]+'
        }
        
        redactor.add_custom_patterns(custom_patterns)
        assert 'api_key' in redactor.custom_patterns
        assert 'jwt' in redactor.custom_patterns
    
    def test_redaction_modes(self, sample_screenshot):
        """Test different redaction modes."""
        for mode in ['blur', 'pixelate', 'block', 'generate']:
            redactor = EnhancedRedactionFeature(mode=mode)
            # Just test it doesn't crash
            result = redactor.redact_sensitive_data(sample_screenshot)
            assert result is not None
    
    def test_privacy_templates(self):
        """Test privacy template availability."""
        templates = get_privacy_templates()
        
        assert 'medical' in templates
        assert 'financial' in templates
        assert 'government' in templates
        assert 'corporate' in templates
        assert 'gdpr' in templates
    
    def test_template_patterns(self):
        """Test that templates have patterns."""
        for template_name, template_data in PRIVACY_TEMPLATES.items():
            assert 'patterns' in template_data
            assert 'description' in template_data
            assert len(template_data['patterns']) > 0
    
    def test_redact_with_template(self, sample_screenshot):
        """Test redaction with privacy template."""
        redactor = EnhancedRedactionFeature()
        
        for template in ['medical', 'financial', 'gdpr']:
            result = redactor.redact_with_template(sample_screenshot, template)
            assert result is not None


class TestFaceBlurring:
    """Test face blurring feature."""
    
    @pytest.fixture
    def sample_screenshot(self):
        """Create sample screenshot."""
        img_array = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        return ScreenShot(rgb=img_array.tobytes(), size=(200, 200), pos=(0, 0))
    
    def test_face_blur_init(self):
        """Test face blur initialization."""
        face_blur = FaceBlurFeature(
            detection_method='haar',
            blur_strength=30.0,
            expand_ratio=1.2
        )
        
        assert face_blur.detection_method == 'haar'
        assert face_blur.blur_strength == 30.0
        assert face_blur.expand_ratio == 1.2
    
    def test_detect_faces(self, sample_screenshot):
        """Test face detection."""
        face_blur = FaceBlurFeature()
        faces = face_blur.detect_faces(sample_screenshot)
        
        # On random noise, likely won't find faces, but should return list
        assert isinstance(faces, list)
    
    def test_blur_faces(self, sample_screenshot):
        """Test face blurring."""
        face_blur = FaceBlurFeature()
        result = face_blur.blur_faces(sample_screenshot)
        
        assert result is not None
        assert result.size == sample_screenshot.size
    
    def test_blur_strength_variation(self, sample_screenshot):
        """Test different blur strengths."""
        for strength in [10.0, 30.0, 50.0]:
            face_blur = FaceBlurFeature(blur_strength=strength)
            result = face_blur.blur_faces(sample_screenshot)
            assert result is not None


class TestPrivacyTemplates:
    """Test privacy template definitions."""
    
    def test_medical_template(self):
        """Test medical/HIPAA template."""
        template = PRIVACY_TEMPLATES['medical']
        
        assert 'mrn' in template['patterns']
        assert 'dob' in template['patterns']
        assert 'ssn' in template['patterns']
        assert 'HIPAA' in template['description']
    
    def test_financial_template(self):
        """Test financial/PCI-DSS template."""
        template = PRIVACY_TEMPLATES['financial']
        
        assert 'credit_card' in template['patterns']
        assert 'cvv' in template['patterns']
        assert 'PCI-DSS' in template['description']
    
    def test_gdpr_template(self):
        """Test GDPR compliance template."""
        template = PRIVACY_TEMPLATES['gdpr']
        
        assert 'email' in template['patterns']
        assert 'phone' in template['patterns']
        assert 'ip' in template['patterns']
        assert 'GDPR' in template['description']
