"""Example: Code Beautification

This example shows how to use the code beautifier to create
professional-looking code screenshots.
"""

from pyshotter import pyshotter
from pyshotter.beautifier import CodeBeautifierFeature, get_available_themes

def main():
    # Take a screenshot of your code editor
    with pyshotter() as sct:
        screenshot = sct.grab(sct.monitors[1])
    
    # Initialize beautifier with a theme
    beautifier = CodeBeautifierFeature(theme='dracula')
    
    # Beautify the screenshot
    beautified = beautifier.beautify(
        screenshot,
        padding=60,
        shadow_intensity=0.5,
        background_type='gradient'
    )
    
    # Save
    beautified.save('beautiful_code.png')
    print("Saved: beautiful_code.png")
    
    # Show available themes
    print(f"\nAvailable themes: {', '.join(get_available_themes())}")


if __name__ == '__main__':
    main()
