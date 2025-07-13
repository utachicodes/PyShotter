"""Sensitive Data Redaction Example

This example demonstrates how to automatically redact sensitive information from screenshots.
"""

from pyshotter import pyshotter, RedactionFeature

def redact_sensitive_data():
    """Redact sensitive data from a screenshot."""
    
    # Take a screenshot
    with pyshotter() as sct:
        screenshot = sct.grab(sct.monitors[0])
        
        # Initialize redaction feature
        redaction = RedactionFeature()
        
        # Redact sensitive data
        clean_screenshot = redaction.redact_sensitive_data(screenshot)
        
        # Save the redacted screenshot
        clean_screenshot.save("redacted_screenshot.png")
        print("Sensitive data has been redacted and saved to 'redacted_screenshot.png'")

if __name__ == "__main__":
    redact_sensitive_data() 
