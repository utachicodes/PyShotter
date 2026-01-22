"""Example: AI-Powered Redaction

This example shows how to redact sensitive data and blur faces.
"""

from pyshotter import pyshotter
from pyshotter.ai_features import EnhancedRedactionFeature, FaceBlurFeature

def main():
    # Take a screenshot
    with pyshotter() as sct:
        screenshot = sct.grab(sct.monitors[1])
    
    # Method 1: Automatic redaction
    redactor = EnhancedRedactionFeature(mode='blur')
    redacted = redactor.redact_sensitive_data(
        screenshot,
        pattern_types=['email', 'phone', 'ssn']
    )
    redacted.save('redacted.png')
    print("Saved redacted.png")
    
    # Method 2: Use privacy template
    redactor2 = EnhancedRedactionFeature(mode='pixelate')
    gdpr_redacted = redactor2.redact_with_template(screenshot, 'gdpr')
    gdpr_redacted.save('gdpr_compliant.png')
    print("Saved gdpr_compliant.png")
    
    # Method 3: Blur faces
    face_blur = FaceBlurFeature(blur_strength=30.0)
    face_blurred = face_blur.blur_faces(screenshot)
    face_blurred.save('faces_blurred.png')
    print("Saved faces_blurred.png")


if __name__ == '__main__':
    main()
