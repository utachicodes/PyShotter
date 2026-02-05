"""Screen recording feature for PyShotter.

This module provides enterprise-grade screen recording with:
- Real-time encoding
- GIF and MP4 export
- Adaptive FPS
- Progress callbacks
- Region-specific recording
"""

import time
import threading
import queue
from pathlib import Path
from typing import Optional, Callable, Tuple, Literal, Dict
from datetime import datetime
import shutil

try:
    import imageio
    IMAGEIO_AVAILABLE = True
except ImportError:
    IMAGEIO_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from .exception import RecordingError, DependencyError
from .logging_config import get_logger, PerformanceLogger

logger = get_logger(__name__)


class ScreenRecordingFeature:
    """Enterprise-grade screen recording with optimization."""
    
    def __init__(
        self,
        fps: int = 30,
        quality: Literal['low', 'medium', 'high', 'lossless'] = 'high',
        format: Literal['gif', 'mp4'] = 'gif',
    ):
        """Initialize screen recorder.
        
        Args:
            fps: Frames per second (1-60)
            quality: Recording quality
            format: Output format
            
        Raises:
            DependencyError: If required libraries aren't installed
            RecordingError: If parameters are invalid
        """
        if not IMAGEIO_AVAILABLE or not NUMPY_AVAILABLE:
            raise DependencyError(
                'Screen Recording',
                'imageio and numpy',
                'pip install pyshotter[recording]'
            )
        
        if not 1 <= fps <= 60:
            raise RecordingError(f"FPS must be between 1 and 60, got {fps}")
        
        self.fps = fps
        self.quality = quality
        self.format = format
        self.frame_delay = 1.0 / fps
        
        # Recording state
        self._recordings: Dict[str, Dict] = {}
        self._next_id = 0
        
        logger.info(f"Initialized recorder: fps={fps}, quality={quality}, format={format}")
    
    def record(
        self,
        duration: float,
        output: str,
        region: Optional[Tuple[int, int, int, int]] = None,
        progress_callback: Optional[Callable[[int, float, float], None]] = None,
    ) -> str:
        """Record screen for fixed duration.
        
        Args:
            duration: Recording duration in seconds
            output: Output file path
            region: Optional region (x, y, width, height)
            progress_callback: Optional callback(frame_count, elapsed, eta)
            
        Returns:
            Path to saved recording
            
        Raises:
            RecordingError: If recording fails
        """
        recording_id = None
        try:
            logger.info(f"Starting recording: duration={duration}s, output={output}")
            
            # Start recording
            recording_id = self.start_recording(
                region=region,
                progress_callback=progress_callback,
                max_duration=duration
            )
            
            # Wait for duration
            time.sleep(duration)
            
            # Stop and save
            output_path = self.stop_recording(recording_id, output)
            
            logger.info(f"Recording completed: {output_path}")
            return output_path
            
        except Exception as e:
            if recording_id:
                self._cleanup_recording(recording_id)
            logger.error(f"Recording failed: {e}")
            raise RecordingError(f"Recording failed: {e}", recording_id=recording_id)
    
    def start_recording(
        self,
        region: Optional[Tuple[int, int, int, int]] = None,
        progress_callback: Optional[Callable[[int, float, float], None]] = None,
        max_duration: float = 300,
    ) -> str:
        """Start recording asynchronously.
        
        Args:
            region: Optional region to record
            progress_callback: Optional progress callback
            max_duration: Maximum recording duration (safety limit)
            
        Returns:
            Recording ID
            
        Raises:
            RecordingError: If recording fails to start
        """
        try:
            # Check disk space
            if not self._check_disk_space():
                raise RecordingError("Insufficient disk space for recording")
            
            recording_id = f"rec_{self._next_id}"
            self._next_id += 1
            
            # Create recording state
            recording = {
                'id': recording_id,
                'region': region,
                'frames': [],
                'start_time': time.time(),
                'max_duration': max_duration,
                'progress_callback': progress_callback,
                'stop_event': threading.Event(),
                'pause_event': threading.Event(),
                'frame_queue': queue.Queue(maxsize=60),  # Buffer up to 2 seconds at 30fps
                'overlay_text': None,
            }
            
            self._recordings[recording_id] = recording
            
            # Start capture thread
            capture_thread = threading.Thread(
                target=self._capture_loop,
                args=(recording_id,),
                daemon=True
            )
            capture_thread.start()
            recording['capture_thread'] = capture_thread
            
            logger.info(f"Started recording: {recording_id}")
            return recording_id
            
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            raise RecordingError(f"Failed to start recording: {e}")
    
    def stop_recording(self, recording_id: str, output: Optional[str] = None) -> str:
        """Stop recording and save to file.
        
        Args:
            recording_id: Recording ID from start_recording()
            output: Optional output path (auto-generated if not provided)
            
        Returns:
            Path to saved file
            
        Raises:
            RecordingError: If recording doesn't exist or save fails
        """
        if recording_id not in self._recordings:
            raise RecordingError(f"Unknown recording ID: {recording_id}", recording_id=recording_id)
        
        try:
            recording = self._recordings[recording_id]
            logger.info(f"Stopping recording: {recording_id}")
            
            # Signal stop
            recording['stop_event'].set()
            
            # Wait for capture thread
            if 'capture_thread' in recording:
                recording['capture_thread'].join(timeout=5.0)
            
            # Generate output path if not provided
            if output is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output = f"recording_{timestamp}.{self.format}"
            
            # Save recording
            output_path = self._save_recording(recording, output)
            
            # Cleanup
            self._cleanup_recording(recording_id)
            
            logger.info(f"Recording saved: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            raise RecordingError(f"Failed to stop recording: {e}", recording_id=recording_id)
    
    def pause_recording(self, recording_id: str) -> None:
        """Pause recording.
        
        Args:
            recording_id: Recording ID
        """
        if recording_id in self._recordings:
            self._recordings[recording_id]['pause_event'].set()
            logger.info(f"Paused recording: {recording_id}")

    def resume_recording(self, recording_id: str) -> None:
        """Resume recording.
        
        Args:
            recording_id: Recording ID
        """
        if recording_id in self._recordings:
            self._recordings[recording_id]['pause_event'].clear()
            logger.info(f"Resumed recording: {recording_id}")

    def set_overlay(self, recording_id: str, text: Optional[str]) -> None:
        """Set watermark overlay for recording.
        
        Args:
            recording_id: Recording ID
            text: Watermark text (None to disable)
        """
        if recording_id in self._recordings:
            self._recordings[recording_id]['overlay_text'] = text
            logger.info(f"Set overlay for {recording_id}: {text}")
    
    def _capture_loop(self, recording_id: str) -> None:
        """Background loop to capture frames.
        
        Args:
            recording_id: Recording ID
        """
        recording = self._recordings[recording_id]
        stop_event = recording['stop_event']
        start_time = recording['start_time']
        max_duration = recording['max_duration']
        callback = recording['progress_callback']
        
        frame_count = 0
        
        try:
            from .factory import pyshotter
            
            with pyshotter() as sct:
                while not stop_event.is_set():
                    loop_start = time.time()
                    
                    # Check max duration
                    elapsed = time.time() - start_time
                    if elapsed >= max_duration:
                        logger.warning(f"Max duration reached: {max_duration}s")
                        break
                    
                    # Capture frame
                    try:
                        if pause_event.is_set():
                            time.sleep(0.1)
                            continue

                        if recording['region']:
                            x, y, w, h = recording['region']
                            monitor = {'left': x, 'top': y, 'width': w, 'height': h}
                        else:
                            monitor = sct.monitors[1]  # Primary monitor
                        
                        screenshot = sct.grab(monitor)
                        
                        # Convert to numpy array for imageio
                        img_array = np.frombuffer(screenshot.rgb, dtype=np.uint8)
                        img_array = img_array.reshape(screenshot.height, screenshot.width, 3).copy()
                        
                        # Apply overlay if set
                        if recording['overlay_text']:
                            img_array = self._apply_overlay(img_array, recording['overlay_text'])

                        recording['frames'].append(img_array)
                        frame_count += 1
                        
                        # Progress callback
                        if callback and frame_count % 10 == 0:  # Every 10 frames
                            eta = (max_duration - elapsed) if max_duration < float('inf') else 0
                            callback(frame_count, elapsed, eta)
                        
                    except Exception as e:
                        logger.error(f"Frame capture failed: {e}")
                        break
                    
                    # Maintain FPS
                    loop_time = time.time() - loop_start
                    sleep_time = max(0, self.frame_delay - loop_time)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
            
            logger.info(f"Capture loop finished: {frame_count} frames")
            
        except Exception as e:
            logger.error(f"Capture loop error: {e}")
    
    def _save_recording(self, recording: Dict, output: str) -> str:
        """Save recording to file.
        
        Args:
            recording: Recording state dict
            output: Output path
            
        Returns:
            Path to saved file
        """
        frames = recording['frames']
        
        if not frames:
            raise RecordingError("No frames captured")
        
        logger.info(f"Saving {len(frames)} frames to {output}")
        
        with PerformanceLogger(logger, f"save recording ({len(frames)} frames)"):
            try:
                if self.format == 'gif':
                    # Save as GIF with optimization
                    imageio.mimsave(
                        output,
                        frames,
                        format='GIF',
                        fps=self.fps,
                        loop=0,  # Infinite loop
                    )
                else:  # mp4
                    # Save as MP4
                    imageio.mimsave(
                        output,
                        frames,
                        format='MP4',
                        fps=self.fps,
                        codec='libx264',
                        quality=8 if self.quality == 'high' else 5,
                    )
                
                return str(Path(output).absolute())
                
            except Exception as e:
                raise RecordingError(f"Failed to save recording: {e}")
    
    def _check_disk_space(self, required_gb: float = 1.0) -> bool:
        """Check if sufficient disk space is available.
        
        Args:
            required_gb: Required space in GB
            
        Returns:
            True if sufficient space available
        """
        try:
            usage = shutil.disk_usage(Path.home())
            free_gb = usage.free / (1024 ** 3)
            return free_gb >= required_gb
        except Exception:
            return True  # Assume OK if check fails
    
    def _cleanup_recording(self, recording_id: str) -> None:
        """Clean up recording resources.
        
        Args:
            recording_id: Recording ID
        """
        if recording_id in self._recordings:
            recording = self._recordings[recording_id]
            # Clear frames to free memory
            if 'frames' in recording:
                recording['frames'].clear()
            del self._recordings[recording_id]
            logger.debug(f"Cleaned up recording: {recording_id}")

    def _apply_overlay(self, img_array: np.ndarray, text: str) -> np.ndarray:
        """Apply simple text watermark to frame."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.fromarray(img_array)
            draw = ImageDraw.Draw(img)
            
            # Simple watermark bottom-right
            h, w = img_array.shape[:2]
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
                
            draw.text((w - 150, h - 30), text, fill=(255, 255, 255), font=font)
            return np.array(img)
        except Exception as e:
            logger.warning(f"Failed to apply overlay: {e}")
            return img_array
