"""Unit tests for screen recording."""

import pytest
import time
import tempfile
from pathlib import Path

from pyshotter.recording import ScreenRecordingFeature
from pyshotter.exception import RecordingError, DependencyError


class TestScreenRecording:
    """Test screen recording feature."""
    
    def test_recording_init_valid_params(self):
        """Test recorder initialization with valid parameters."""
        recorder = ScreenRecordingFeature(fps=30, quality='high', format='gif')
        assert recorder.fps == 30
        assert recorder.quality == 'high'
        assert recorder.format == 'gif'
    
    def test_recording_init_invalid_fps(self):
        """Test recorder initialization with invalid FPS."""
        with pytest.raises(RecordingError):
            ScreenRecordingFeature(fps=0)  # Too low
        
        with pytest.raises(RecordingError):
            ScreenRecordingFeature(fps=100)  # Too high
    
    def test_recording_start_stop(self):
        """Test starting and stopping recording."""
        recorder = ScreenRecordingFeature()
        
        # Start recording
        recording_id = recorder.start_recording(max_duration=2)
        assert recording_id is not None
        assert recording_id in recorder._recordings
        
        # Let it record for a bit
        time.sleep(0.5)
        
        # Stop recording
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as f:
            output_path = recorder.stop_recording(recording_id, f.name)
            assert Path(output_path).exists()
            
            # Cleanup
            Path(output_path).unlink()
    
    def test_recording_short_duration(self):
        """Test recording for short duration."""
        recorder = ScreenRecordingFeature(fps=10)
        
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as f:
            output_path = recorder.record(
                duration=1,
                output=f.name
            )
            
            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size > 0
            
            # Cleanup
            Path(output_path).unlink()
    
    def test_recording_progress_callback(self):
        """Test progress callback functionality."""
        recorder = ScreenRecordingFeature(fps=10)
        
        callback_called = [False]
        
        def progress_callback(frame_count, elapsed, eta):
            callback_called[0] = True
            assert frame_count > 0
            assert elapsed >= 0
        
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as f:
            output_path = recorder.record(
                duration=1,
                output=f.name,
                progress_callback=progress_callback
            )
            
            # Callback should have been called
            assert callback_called[0]
            
            # Cleanup
            Path(output_path).unlink()
    
    def test_recording_formats(self):
        """Test different recording formats."""
        for fmt in ['gif', 'mp4']:
            recorder = ScreenRecordingFeature(format=fmt)
            
            with tempfile.NamedTemporaryFile(suffix=f'.{fmt}', delete=False) as f:
                try:
                    output_path = recorder.record(duration=0.5, output=f.name)
                    assert Path(output_path).exists()
                finally:
                    if Path(f.name).exists():
                        Path(f.name).unlink()
    
    def test_recording_invalid_id(self):
        """Test stopping non-existent recording."""
        recorder = ScreenRecordingFeature()
        
        with pytest.raises(RecordingError):
            recorder.stop_recording('invalid_id')
    
    def test_recording_cleanup(self):
        """Test that recordings are cleaned up."""
        recorder = ScreenRecordingFeature()
        
        recording_id = recorder.start_recording(max_duration=1)
        assert recording_id in recorder._recordings
        
        time.sleep(0.2)
        
        with tempfile.NamedTemporaryFile(suffix='.gif') as f:
            recorder.stop_recording(recording_id, f.name)
        
        # Should be cleaned up
        assert recording_id not in recorder._recordings


@pytest.mark.benchmark
class TestRecordingPerformance:
    """Performance tests for recording."""
    
    def test_frame_capture_performance(self, benchmark):
        """Benchmark frame capture performance."""
        recorder = ScreenRecordingFeature(fps=30)
        
        # This will test the recording initialization
        def record_short():
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as f:
                output = recorder.record(duration=0.5, output=f.name)
                Path(output).unlink()
        
        benchmark(record_short)
