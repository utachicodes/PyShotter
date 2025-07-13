"""Advanced Features Example

This example demonstrates all of PyShotter's advanced features working together.
"""

import time
from pyshotter import (
    pyshotter, 
    OCRFeature, 
    RedactionFeature, 
    PanoramaFeature, 
    ChangeDetectionFeature, 
    ScreenshotHistory
)

def demonstrate_all_features():
    """Demonstrate all advanced features of PyShotter."""
    
    print("🚀 PyShotter Advanced Features Demo")
    print("=" * 50)
    
    with pyshotter() as sct:
        # 1. Take screenshots of all monitors
        print("\n📸 Taking screenshots of all monitors...")
        screenshots = []
        for i, monitor in enumerate(sct.monitors):
            screenshot = sct.grab(monitor)
            screenshots.append(screenshot)
            print(f"  Monitor {i+1}: {screenshot.size}")
        
        # 2. OCR Text Extraction
        print("\n🔍 Extracting text with OCR...")
        ocr = OCRFeature()
        text = ocr.extract_text(screenshots[0])
        print(f"  Extracted text: {text[:100]}...")
        
        # 3. Sensitive Data Redaction
        print("\n🔒 Redacting sensitive data...")
        redaction = RedactionFeature()
        clean_screenshot = redaction.redact_sensitive_data(screenshots[0])
        clean_screenshot.save("clean_screenshot.png")
        print("  Clean screenshot saved as 'clean_screenshot.png'")
        
        # 4. Multi-Monitor Panorama
        print("\n🖥️ Creating panoramic image...")
        panorama = PanoramaFeature()
        panoramic_screenshot = panorama.create_panorama(screenshots)
        panoramic_screenshot.save("panorama.png")
        print(f"  Panorama saved as 'panorama.png' ({panoramic_screenshot.size})")
        
        # 5. Change Detection
        print("\n🔄 Detecting changes...")
        time.sleep(2)  # Wait for potential changes
        current_screenshot = sct.grab(sct.monitors[0])
        
        change_detector = ChangeDetectionFeature()
        changes_screenshot = change_detector.detect_changes(
            current_screenshot, 
            screenshots[0]
        )
        changes_screenshot.save("changes.png")
        print("  Changes saved as 'changes.png'")
        
        # 6. Screenshot History and Search
        print("\n📚 Managing screenshot history...")
        history = ScreenshotHistory()
        
        # Add screenshots to history
        for i, screenshot in enumerate(screenshots):
            screenshot_id = history.add_screenshot(
                screenshot,
                metadata={
                    "tags": [f"monitor_{i+1}", "demo"],
                    "description": f"Screenshot from monitor {i+1}"
                }
            )
            print(f"  Added screenshot {i+1} with ID: {screenshot_id}")
        
        # Search history
        results = history.search_history("demo")
        print(f"  Found {len(results)} screenshots in history")
        
        print("\n✅ All features demonstrated successfully!")
        print("\nGenerated files:")
        print("  - clean_screenshot.png (redacted)")
        print("  - panorama.png (multi-monitor)")
        print("  - changes.png (change detection)")
        print("  - History saved to ~/.pyshotter/history/")

if __name__ == "__main__":
    demonstrate_all_features() 
