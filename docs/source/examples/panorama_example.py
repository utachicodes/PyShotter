"""Multi-Monitor Panorama Example

This example demonstrates how to create a panoramic image from multiple monitors.
"""

from pyshotter import pyshotter, PanoramaFeature

def create_panorama():
    """Create a panoramic image from all monitors."""
    
    # Take screenshots of all monitors
    with pyshotter() as sct:
        screenshots = []
        
        # Capture each monitor
        for i, monitor in enumerate(sct.monitors):
            screenshot = sct.grab(monitor)
            screenshots.append(screenshot)
            print(f"Captured monitor {i+1}: {screenshot.size}")
        
        # Initialize panorama feature
        panorama = PanoramaFeature()
        
        # Create panoramic image
        panoramic_screenshot = panorama.create_panorama(screenshots)
        
        # Save the panorama
        panoramic_screenshot.save("panorama.png")
        print(f"Panoramic image saved: {panoramic_screenshot.size}")

if __name__ == "__main__":
    create_panorama() 
