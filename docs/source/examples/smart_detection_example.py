"""Smart Detection Example

This example demonstrates how to use PyShotter's smart detection features.
"""

from pyshotter import pyshotter, SmartDetectionFeature, AnnotationFeature

def detect_and_annotate():
    """Detect code regions and windows, then annotate them."""
    
    with pyshotter() as sct:
        # Take a screenshot
        screenshot = sct.grab(sct.monitors[0])
        
        # Initialize smart detection
        detector = SmartDetectionFeature()
        
        # Detect code regions
        print("🔍 Detecting code regions...")
        code_regions = detector.detect_code_regions(screenshot)
        print(f"Found {len(code_regions)} code regions")
        
        # Detect windows
        print("🖥️ Detecting windows...")
        windows = detector.detect_windows(screenshot)
        print(f"Found {len(windows)} windows")
        
        # Annotate detected regions
        annotator = AnnotationFeature()
        annotated = screenshot
        
        # Highlight code regions with rectangles
        for i, region in enumerate(code_regions[:5]):  # Limit to first 5
            x, y, w, h = region['bbox']
            annotated = annotator.add_rectangle(
                annotated,
                (x, y),
                (x + w, y + h),
                color=(0, 255, 0),  # Green for code
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
        
        # Highlight windows with circles
        for i, window in enumerate(windows[:3]):  # Limit to first 3
            x, y, w, h = window['bbox']
            center_x = x + w // 2
            center_y = y + h // 2
            radius = min(w, h) // 4
            
            annotated = annotator.add_circle(
                annotated,
                (center_x, center_y),
                radius,
                color=(255, 0, 0),  # Red for windows
                thickness=2
            )
            # Add label
            annotated = annotator.add_text(
                annotated,
                f"Window {i+1}",
                (x, y - 20),
                font_size=16,
                color=(255, 0, 0)
            )
        
        # Save the annotated screenshot
        annotated.save("smart_detection_result.png")
        print("✅ Smart detection result saved as 'smart_detection_result.png'")
        
        return code_regions, windows

def analyze_screenshot():
    """Analyze screenshot content and provide insights."""
    
    with pyshotter() as sct:
        screenshot = sct.grab(sct.monitors[0])
        detector = SmartDetectionFeature()
        
        # Get detection results
        code_regions = detector.detect_code_regions(screenshot)
        windows = detector.detect_windows(screenshot)
        
        # Analyze and report
        print("📊 Screenshot Analysis")
        print("=" * 30)
        print(f"📏 Screenshot size: {screenshot.size}")
        print(f"🔍 Code regions detected: {len(code_regions)}")
        print(f"🖥️ Windows detected: {len(windows)}")
        
        if code_regions:
            total_code_area = sum(region['area'] for region in code_regions)
            print(f"📝 Total code area: {total_code_area} pixels")
        
        if windows:
            largest_window = max(windows, key=lambda w: w['area'])
            print(f"🖼️ Largest window: {largest_window['bbox']}")
        
        # Provide recommendations
        print("\n💡 Recommendations:")
        if len(code_regions) > 3:
            print("  - Consider annotating important code sections")
        if len(windows) > 2:
            print("  - Multiple windows detected - consider panorama mode")
        if not code_regions and not windows:
            print("  - No specific content detected - try different detection settings")

if __name__ == "__main__":
    print("🧠 PyShotter Smart Detection Demo")
    print("=" * 50)
    
    # Run detection and annotation
    code_regions, windows = detect_and_annotate()
    
    print("\n" + "=" * 50)
    
    # Run analysis
    analyze_screenshot() 