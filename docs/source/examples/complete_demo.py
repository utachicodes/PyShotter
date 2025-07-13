"""Complete PyShotter Demo

This example demonstrates all of PyShotter's smart, annotated, and shareable features.
"""

import time
from pyshotter import (
    pyshotter, 
    SmartDetectionFeature,
    AnnotationFeature,
    SharingFeature,
    OCRFeature,
    RedactionFeature,
    PanoramaFeature,
    ChangeDetectionFeature,
    ScreenshotHistory
)

def complete_pyshotter_demo():
    """Demonstrate all PyShotter features: Smart, Annotated, and Shareable."""
    
    print("🚀 PyShotter: Smart, Annotated, and Shareable Screenshots")
    print("=" * 60)
    
    with pyshotter() as sct:
        # 1. SMART DETECTION
        print("\n🧠 STEP 1: Smart Detection")
        print("-" * 30)
        
        screenshot = sct.grab(sct.monitors[0])
        
        # Detect code regions and windows
        detector = SmartDetectionFeature()
        code_regions = detector.detect_code_regions(screenshot)
        windows = detector.detect_windows(screenshot)
        
        print(f"✅ Detected {len(code_regions)} code regions")
        print(f"✅ Detected {len(windows)} windows")
        
        # 2. OCR TEXT EXTRACTION
        print("\n📝 STEP 2: OCR Text Extraction")
        print("-" * 30)
        
        ocr = OCRFeature()
        text = ocr.extract_text(screenshot)
        print(f"✅ Extracted text: {text[:100]}...")
        
        # 3. ANNOTATION
        print("\n🎨 STEP 3: Rich Annotation")
        print("-" * 30)
        
        annotator = AnnotationFeature()
        annotated = screenshot
        
        # Add text annotation
        annotated = annotator.add_text(
            annotated, 
            "PyShotter Demo", 
            (50, 50),
            font_size=24,
            color=(255, 0, 0)
        )
        
        # Add rectangle around detected code regions
        for i, region in enumerate(code_regions[:3]):
            x, y, w, h = region['bbox']
            annotated = annotator.add_rectangle(
                annotated,
                (x, y),
                (x + w, y + h),
                color=(0, 255, 0),
                thickness=2
            )
            # Add label
            annotated = annotator.add_text(
                annotated,
                f"Code {i+1}",
                (x, y - 20),
                font_size=16,
                color=(0, 255, 0)
            )
        
        # Add arrow pointing to important area
        annotated = annotator.add_arrow(
            annotated,
            (100, 100),
            (300, 150),
            color=(0, 0, 255),
            thickness=3
        )
        
        # Add highlight
        annotated = annotator.add_highlight(
            annotated,
            (200, 200, 150, 100),
            color=(255, 255, 0),
            alpha=0.3
        )
        
        print("✅ Added text, shapes, arrows, and highlights")
        
        # 4. SHARING
        print("\n📤 STEP 4: Easy Sharing")
        print("-" * 30)
        
        sharer = SharingFeature()
        
        # Copy to clipboard
        if sharer.copy_to_clipboard(annotated):
            print("✅ Screenshot copied to clipboard!")
        
        # Generate shareable link
        link = sharer.generate_shareable_link(annotated)
        print(f"✅ Shareable link generated: {link[:50]}...")
        
        # Save with metadata
        metadata = {
            "title": "PyShotter Demo Screenshot",
            "description": "Smart, annotated, and shareable screenshot",
            "tags": ["demo", "pyshotter", "smart", "annotated", "shareable"],
            "author": "Abdoullah Ndao",
            "features_used": ["smart_detection", "annotation", "sharing"]
        }
        
        sharer.save_with_metadata(annotated, "demo_screenshot.png", metadata)
        print("✅ Screenshot saved with metadata")
        
        # 5. ADVANCED FEATURES
        print("\n🔧 STEP 5: Advanced Features")
        print("-" * 30)
        
        # Redaction
        redaction = RedactionFeature()
        clean_screenshot = redaction.redact_sensitive_data(screenshot)
        clean_screenshot.save("redacted_screenshot.png")
        print("✅ Sensitive data redacted")
        
        # Panorama (if multiple monitors)
        if len(sct.monitors) > 1:
            panorama = PanoramaFeature()
            screenshots = [sct.grab(monitor) for monitor in sct.monitors]
            panoramic = panorama.create_panorama(screenshots)
            panoramic.save("panorama.png")
            print("✅ Multi-monitor panorama created")
        
        # Change detection
        time.sleep(1)  # Wait a bit
        current_screenshot = sct.grab(sct.monitors[0])
        change_detector = ChangeDetectionFeature()
        changes = change_detector.detect_changes(current_screenshot, screenshot)
        changes.save("changes.png")
        print("✅ Change detection completed")
        
        # History and search
        history = ScreenshotHistory()
        screenshot_id = history.add_screenshot(
            annotated,
            metadata={
                "tags": ["demo", "complete"],
                "description": "Complete PyShotter demo screenshot"
            }
        )
        print(f"✅ Added to history with ID: {screenshot_id}")
        
        # Search history
        results = history.search_history("demo")
        print(f"✅ Found {len(results)} screenshots in history")
        
        # 6. FINAL RESULT
        print("\n🎉 STEP 6: Final Result")
        print("-" * 30)
        
        # Save the final annotated screenshot
        annotated.save("complete_demo_result.png")
        
        print("✅ Complete demo finished!")
        print("\n📁 Generated files:")
        print("  - complete_demo_result.png (annotated)")
        print("  - redacted_screenshot.png (clean)")
        print("  - changes.png (change detection)")
        if len(sct.monitors) > 1:
            print("  - panorama.png (multi-monitor)")
        print("  - demo_screenshot.png (with metadata)")
        print("  - History saved to ~/.pyshotter/history/")
        
        print("\n🚀 PyShotter makes screenshots smart, annotated, and shareable!")

if __name__ == "__main__":
    complete_pyshotter_demo() 
