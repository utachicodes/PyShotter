"""Example: Screen Recording

This example shows how to record your screen as GIF or MP4.
"""

from pyshotter.recording import ScreenRecordingFeature

def main():
    # Initialize recorder
    recorder = ScreenRecordingFeature(
        fps=30,
        quality='high',
        format='gif'
    )
    
    # Record for 10 seconds
    print("Recording for 10 seconds...")
    
    def progress(frame_count, elapsed, eta):
        print(f"Frames: {frame_count}, Elapsed: {elapsed:.1f}s")
    
    output_path = recorder.record(
        duration=10,
        output='demo_recording.gif',
        progress_callback=progress
    )
    
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    main()
