"""Sharing Example

This example demonstrates how to easily share screenshots using PyShotter.
"""

from pyshotter import pyshotter, SharingFeature

def share_screenshot():
    """Demonstrate various sharing methods."""
    
    with pyshotter() as sct:
        # Take a screenshot
        screenshot = sct.grab(sct.monitors[0])
        
        # Initialize sharing feature
        sharer = SharingFeature()
        
        # Method 1: Copy to clipboard
        if sharer.copy_to_clipboard(screenshot):
            print("✅ Screenshot copied to clipboard!")
        else:
            print("❌ Clipboard copy failed (install pyperclip: pip install pyperclip)")
        
        # Method 2: Generate shareable link
        shareable_link = sharer.generate_shareable_link(screenshot)
        if shareable_link:
            print(f"🔗 Shareable link: {shareable_link}")
        else:
            print("❌ Failed to generate shareable link")
        
        # Method 3: Save with metadata
        metadata = {
            "title": "My Screenshot",
            "description": "Screenshot taken with PyShotter",
            "tags": ["python", "screenshot", "demo"],
            "author": "Abdoullah Ndao",
            "timestamp": "2024-12-19"
        }
        
        if sharer.save_with_metadata(screenshot, "screenshot_with_metadata.png", metadata):
            print("✅ Screenshot saved with metadata!")
        else:
            print("❌ Failed to save with metadata")

def share_annotated_screenshot():
    """Share an annotated screenshot."""
    
    from pyshotter import AnnotationFeature
    
    with pyshotter() as sct:
        screenshot = sct.grab(sct.monitors[0])
        
        # Add some annotations
        annotator = AnnotationFeature()
        annotated = annotator.add_text(screenshot, "Shared via PyShotter!", (100, 100))
        annotated = annotator.add_rectangle(annotated, (50, 50), (300, 200))
        
        # Share the annotated screenshot
        sharer = SharingFeature()
        
        # Copy to clipboard
        if sharer.copy_to_clipboard(annotated):
            print("✅ Annotated screenshot copied to clipboard!")
        
        # Generate link
        link = sharer.generate_shareable_link(annotated)
        print(f"🔗 Annotated screenshot link: {link}")

if __name__ == "__main__":
    print("📤 PyShotter Sharing Demo")
    print("=" * 40)
    
    share_screenshot()
    print("\n" + "=" * 40)
    share_annotated_screenshot() 
