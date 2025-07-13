"""Annotation Example

This example demonstrates how to add rich annotations to screenshots using PyShotter.
"""

from pyshotter import pyshotter, AnnotationFeature

def annotate_screenshot():
    """Add various annotations to a screenshot."""
    
    with pyshotter() as sct:
        # Take a screenshot
        screenshot = sct.grab(sct.monitors[0])
        
        # Initialize annotation feature
        annotator = AnnotationFeature()
        
        # Add text annotation
        annotated = annotator.add_text(
            screenshot, 
            "Important Code Here!", 
            (100, 100),
            font_size=24,
            color=(255, 0, 0)  # Red text
        )
        
        # Add rectangle around a region
        annotated = annotator.add_rectangle(
            annotated,
            (50, 50),      # Top-left
            (400, 200),    # Bottom-right
            color=(0, 255, 0),  # Green rectangle
            thickness=3
        )
        
        # Add arrow pointing to something
        annotated = annotator.add_arrow(
            annotated,
            (150, 150),    # Start point
            (300, 100),    # End point
            color=(0, 0, 255),  # Blue arrow
            thickness=2
        )
        
        # Add circle highlight
        annotated = annotator.add_circle(
            annotated,
            (200, 150),    # Center
            30,             # Radius
            color=(255, 255, 0),  # Yellow circle
            thickness=2
        )
        
        # Add highlight overlay
        annotated = annotator.add_highlight(
            annotated,
            (100, 100, 200, 100),  # (x, y, width, height)
            color=(255, 255, 0),    # Yellow highlight
            alpha=0.3               # 30% transparency
        )
        
        # Save the annotated screenshot
        annotated.save("annotated_screenshot.png")
        print("Screenshot annotated and saved as 'annotated_screenshot.png'")

if __name__ == "__main__":
    annotate_screenshot() 