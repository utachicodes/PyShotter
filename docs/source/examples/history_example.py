"""Screenshot History and Search Example

This example demonstrates how to use PyShotter's history and search features.
"""

from pyshotter import pyshotter, ScreenshotHistory

def history_and_search():
    """Demonstrate screenshot history and search functionality."""
    
    # Initialize history manager
    history = ScreenshotHistory()
    
    # Take a screenshot and add to history
    with pyshotter() as sct:
        screenshot = sct.grab(sct.monitors[0])
        
        # Add to history with metadata
        screenshot_id = history.add_screenshot(
            screenshot,
            metadata={
                "tags": ["desktop", "work"],
                "window_title": "Example Window",
                "description": "Sample screenshot for demonstration"
            }
        )
        print(f"Screenshot added to history with ID: {screenshot_id}")
    
    # Search for screenshots
    print("\nSearching for screenshots...")
    results = history.search_history("work")
    
    print(f"Found {len(results)} screenshots matching 'work':")
    for result in results:
        print(f"  - ID: {result['id']}")
        print(f"    Timestamp: {result['timestamp']}")
        print(f"    Tags: {result['metadata'].get('tags', [])}")
        print(f"    OCR Text: {result['ocr_text'][:100]}...")
        print()

if __name__ == "__main__":
    history_and_search() 