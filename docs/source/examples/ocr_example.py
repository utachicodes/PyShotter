"""OCR Text Extraction Example

This example demonstrates how to extract text from screenshots using PyShotter's OCR feature.
"""

from pyshotter import pyshotter, OCRFeature

def extract_text_from_screenshot():
    """Extract text from a screenshot using OCR."""
    
    # Take a screenshot
    with pyshotter() as sct:
        screenshot = sct.grab(sct.monitors[0])
        
        # Initialize OCR feature
        ocr = OCRFeature()
        
        # Extract text
        text = ocr.extract_text(screenshot)
        print(f"Extracted text: {text}")
        
        # Extract text with bounding boxes
        text_boxes = ocr.extract_text_boxes(screenshot)
        print(f"Found {len(text_boxes)} text elements:")
        
        for i, box in enumerate(text_boxes[:5]):  # Show first 5
            print(f"  {i+1}. '{box['text']}' (confidence: {box['confidence']}%)")

if __name__ == "__main__":
    extract_text_from_screenshot() 