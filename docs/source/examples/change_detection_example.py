"""Change Detection Example

This example demonstrates how to detect changes between screenshots.
"""

import time
from pyshotter import pyshotter, ChangeDetectionFeature

def detect_changes():
    """Detect changes between two screenshots taken at different times."""
    
    with pyshotter() as sct:
        # Take first screenshot
        print("Taking first screenshot...")
        previous_screenshot = sct.grab(sct.monitors[0])
        
        # Wait a bit for changes
        print("Waiting 5 seconds for changes...")
        time.sleep(5)
        
        # Take second screenshot
        print("Taking second screenshot...")
        current_screenshot = sct.grab(sct.monitors[0])
        
        # Initialize change detection
        change_detector = ChangeDetectionFeature()
        
        # Detect changes
        changes_screenshot = change_detector.detect_changes(
            current_screenshot, 
            previous_screenshot
        )
        
        # Save the result
        changes_screenshot.save("changes_detected.png")
        print("Change detection completed and saved to 'changes_detected.png'")

if __name__ == "__main__":
    detect_changes() 
