"""Video creation module for generating vertical videos with audio."""

import requests
import random
from pathlib import Path
from typing import Optional
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter
import librosa
import tempfile
import subprocess
import os
import math


class VerticalVideoCreator:
    """Creates vertical or horizontal videos with audio waveform animations."""

    def __init__(self, orientation: str = "vertical"):
        """Initialize video creator with specified orientation.

        Args:
            orientation: "vertical" for 1080x1920, "horizontal" for 1920x1080
        """
        if orientation.lower() == "horizontal":
            self.width = 1920
            self.height = 1080
            self.orientation = "horizontal"
        else:
            self.width = 1080
            self.height = 1920
            self.orientation = "vertical"
        self.fps = 30

    def get_random_unsplash_image(
        self, keywords: str = "abstract,gradient,texture"
    ) -> Optional[Path]:
        """Download a random abstract image from Unsplash."""
        try:
            # Unsplash API endpoint for random photos
            url = f"https://source.unsplash.com/{self.width}x{self.height}/?{keywords}"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Save to temporary file
            temp_dir = Path(tempfile.gettempdir())
            image_path = temp_dir / f"unsplash_bg_{random.randint(1000, 9999)}.jpg"

            with open(image_path, "wb") as f:
                f.write(response.content)

            return image_path
        except Exception as e:
            print(f"Failed to download Unsplash image: {e}")
            return None

    def create_dynamic_background(
        self,
        style: str,
        amplitude: float,
        current_time: float,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
    ) -> np.ndarray:
        """Create dynamic animated background that responds to audio."""
        height, width = self.height, self.width
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        if style == "flowing-gradient":
            return self._create_flowing_gradient(
                frame, amplitude, current_time, gradient_style, custom_colors
            )
        elif style == "nebula":
            return self._create_nebula_background(
                frame,
                amplitude,
                current_time,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
            )
        elif style == "aurora":
            return self._create_aurora_background(
                frame, amplitude, current_time, gradient_style, custom_colors
            )
        elif style == "plasma":
            return self._create_plasma_background(
                frame, amplitude, current_time, gradient_style, custom_colors
            )
        elif style == "liquid-metal":
            return self._create_liquid_metal_background(
                frame, amplitude, current_time, gradient_style, custom_colors
            )
        elif style == "cosmic-dust":
            return self._create_cosmic_dust_background(
                frame, amplitude, current_time, frame_idx, gradient_style, custom_colors
            )
        elif style == "energy-waves":
            return self._create_energy_waves_background(
                frame, amplitude, current_time, gradient_style, custom_colors
            )
        elif style == "particle-field":
            return self._create_particle_field_background(
                frame, amplitude, current_time, frame_idx, gradient_style, custom_colors
            )
        elif style == "morphing-shapes":
            return self._create_morphing_shapes_background(
                frame, amplitude, current_time, frame_idx, gradient_style, custom_colors
            )
        elif style == "breathing-colors":
            return self._create_breathing_colors_background(
                frame, amplitude, current_time, gradient_style, custom_colors
            )
        else:
            # Default to flowing gradient
            return self._create_flowing_gradient(
                frame, amplitude, current_time, gradient_style, custom_colors
            )

    def _create_flowing_gradient(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create a flowing gradient background that changes with time and audio (optimized)."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [(20, 20, 50), (100, 20, 150)]  # Default colors

        # Create coordinate meshgrids
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create flowing effect with time and amplitude (vectorized)
        time_offset = current_time * 0.3
        audio_offset = amplitude * 50

        # Create flowing pattern (vectorized)
        wave1 = np.sin((x_coords + y_coords) * 0.01 + time_offset) * 0.3
        wave2 = np.sin((x_coords - y_coords) * 0.008 + time_offset * 1.2) * 0.3
        wave3 = (
            np.sin(np.sqrt(x_coords**2 + y_coords**2) * 0.005 + time_offset * 0.8) * 0.2
        )

        # Combine waves with audio influence
        flow_factor = (wave1 + wave2 + wave3 + audio_offset * 0.01) * 0.5 + 0.5
        flow_factor = np.clip(flow_factor, 0, 1)

        # Simple two-color interpolation (faster)
        if len(colors) >= 2:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            # Vectorized color interpolation
            r = (color1[0] * (1 - flow_factor) + color2[0] * flow_factor).astype(
                np.uint8
            )
            g = (color1[1] * (1 - flow_factor) + color2[1] * flow_factor).astype(
                np.uint8
            )
            b = (color1[2] * (1 - flow_factor) + color2[2] * flow_factor).astype(
                np.uint8
            )

            # Assign to frame (BGR format)
            frame[:, :, 0] = b
            frame[:, :, 1] = g
            frame[:, :, 2] = r

        return frame

    def _create_aurora_background(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create aurora borealis effect with custom gradient colors (optimized)."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [
                (0, 255, 100),
                (100, 150, 255),
                (200, 100, 255),
            ]  # Default aurora colors

        # Create coordinate meshgrids
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create flowing aurora waves (vectorized)
        wave1 = np.sin(x_coords * 0.02 + current_time * 2 + y_coords * 0.01) * 0.5
        wave2 = np.sin(x_coords * 0.015 + current_time * 1.5 + y_coords * 0.008) * 0.3
        wave3 = np.sin(x_coords * 0.01 + current_time + y_coords * 0.005) * 0.2

        # Combine waves with amplitude
        intensity = (wave1 + wave2 + wave3 + amplitude * 0.5) * 0.3 + 0.1
        intensity = np.clip(intensity, 0, 1)

        # Vertical gradient effect (stronger at top)
        vertical_factor = 1.0 - (y_coords / height) * 0.7
        intensity *= vertical_factor

        # Use custom gradient colors instead of fixed aurora colors
        phase = x_coords / width + current_time * 0.1

        # Interpolate between gradient colors based on phase
        if len(colors) >= 3:
            # Use three colors for aurora effect
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])
            color3 = np.array(colors[2]) if len(colors) > 2 else np.array(colors[0])
        else:
            # Use two colors and create a third
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])
            color3 = ((np.array(colors[0]) + np.array(colors[1])) / 2).astype(int)

        # Create color variations using phase
        phase_factor = (np.sin(phase * np.pi) + 1) / 2

        # Interpolate between colors
        r = (color1[0] * (1 - phase_factor) + color2[0] * phase_factor) * intensity
        g = (color1[1] * (1 - phase_factor) + color2[1] * phase_factor) * intensity
        b = (color1[2] * (1 - phase_factor) + color2[2] * phase_factor) * intensity

        frame[:, :, 0] = np.clip(b, 0, 255).astype(np.uint8)
        frame[:, :, 1] = np.clip(g, 0, 255).astype(np.uint8)
        frame[:, :, 2] = np.clip(r, 0, 255).astype(np.uint8)

        return frame

    def _create_plasma_background(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create plasma energy effect with custom gradient colors (optimized)."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [
                (255, 0, 100),
                (0, 255, 255),
                (255, 0, 255),
            ]  # Default plasma colors

        # Create coordinate meshgrids
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create plasma effect with multiple sine waves (vectorized)
        dx = x_coords - width / 2
        dy = y_coords - height / 2
        dist = np.sqrt(dx * dx + dy * dy)

        plasma1 = np.sin(dist * 0.02 + current_time * 3)
        plasma2 = np.sin((x_coords + y_coords) * 0.01 + current_time * 2)
        plasma3 = np.sin((x_coords - y_coords) * 0.008 + current_time * 1.5)
        plasma4 = np.sin(
            np.sqrt(np.abs(x_coords * y_coords)) * 0.01 + current_time * 2.5
        )

        # Combine with amplitude
        plasma_value = (plasma1 + plasma2 + plasma3 + plasma4 + amplitude) * 0.2 + 0.5
        plasma_value = np.clip(plasma_value, 0, 1)

        # Use gradient colors for plasma effect
        if len(colors) >= 3:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])
            color3 = np.array(colors[2])
        else:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])
            color3 = ((np.array(colors[0]) + np.array(colors[1])) / 2).astype(int)

        # Map plasma values to gradient colors using sinusoidal interpolation
        phase1 = plasma_value * np.pi
        phase2 = plasma_value * np.pi + np.pi / 3
        phase3 = plasma_value * np.pi + 2 * np.pi / 3

        # Create color channels using gradient colors
        factor1 = (np.sin(phase1) + 1) / 2
        factor2 = (np.sin(phase2) + 1) / 2
        factor3 = (np.sin(phase3) + 1) / 2

        # Interpolate between gradient colors
        r = (color1[0] * factor1 + color2[0] * factor2 + color3[0] * factor3) / 3
        g = (color1[1] * factor1 + color2[1] * factor2 + color3[1] * factor3) / 3
        b = (color1[2] * factor1 + color2[2] * factor2 + color3[2] * factor3) / 3

        # Apply amplitude intensity
        intensity = 0.5 + amplitude * 0.5
        r = (r * intensity).astype(np.uint8)
        g = (g * intensity).astype(np.uint8)
        b = (b * intensity).astype(np.uint8)

        frame[:, :, 0] = b
        frame[:, :, 1] = g
        frame[:, :, 2] = r

        return frame

    def _create_breathing_colors_background(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create breathing color effect that pulses with audio (optimized)."""
        height, width = frame.shape[:2]

        # Get base colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [(50, 0, 100), (100, 50, 200)]

        # Create coordinate meshgrids
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create breathing effect
        breath_cycle = np.sin(current_time * 1.5) * 0.3 + 0.7
        audio_pulse = amplitude * 0.5 + 0.5
        combined_pulse = (breath_cycle + audio_pulse) * 0.5

        center_x, center_y = width // 2, height // 2

        # Distance from center (vectorized)
        dx = x_coords - center_x
        dy = y_coords - center_y
        dist = np.sqrt(dx * dx + dy * dy) / max(width, height)

        # Create breathing gradient (vectorized)
        intensity = np.sin(dist * np.pi + combined_pulse * np.pi) * 0.5 + 0.5

        # Interpolate colors (vectorized)
        color1 = np.array(colors[0])
        color2 = np.array(colors[1])

        r = (color1[0] * (1 - intensity) + color2[0] * intensity).astype(np.uint8)
        g = (color1[1] * (1 - intensity) + color2[1] * intensity).astype(np.uint8)
        b = (color1[2] * (1 - intensity) + color2[2] * intensity).astype(np.uint8)

        frame[:, :, 0] = b
        frame[:, :, 1] = g
        frame[:, :, 2] = r

        return frame

    def _create_nebula_background(
        self,
        frame,
        amplitude,
        current_time,
        frame_idx,
        total_frames,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create space nebula effect with custom gradient colors."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [
                (100, 0, 200),
                (255, 100, 0),
                (0, 150, 255),
            ]  # Default nebula colors

        # Simple nebula-like effect using gradients
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create swirling pattern
        center_x, center_y = width // 2, height // 2
        dx = x_coords - center_x
        dy = y_coords - center_y
        angle = np.arctan2(dy, dx) + current_time * 0.1
        dist = np.sqrt(dx * dx + dy * dy) / max(width, height)

        # Simple nebula effect
        nebula_factor = np.sin(angle * 3 + dist * 5 + current_time) * 0.5 + 0.5
        nebula_factor = np.clip(nebula_factor * (1 + amplitude), 0, 1)

        # Use gradient colors instead of fixed colors
        if len(colors) >= 3:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])
            color3 = np.array(colors[2])
        else:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])
            color3 = ((np.array(colors[0]) + np.array(colors[1])) / 2).astype(int)

        # Interpolate between colors based on nebula factor
        factor = nebula_factor
        r = (
            color1[0] * factor + color2[0] * (1 - factor) + color3[0] * dist * 0.5
        ).astype(np.uint8)
        g = (
            color1[1] * factor + color2[1] * (1 - factor) + color3[1] * dist * 0.5
        ).astype(np.uint8)
        b = (
            color1[2] * factor + color2[2] * (1 - factor) + color3[2] * dist * 0.5
        ).astype(np.uint8)

        frame[:, :, 0] = np.clip(b, 0, 255)
        frame[:, :, 1] = np.clip(g, 0, 255)
        frame[:, :, 2] = np.clip(r, 0, 255)

        return frame

    def _create_energy_waves_background(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create energy waves background with custom gradient colors (optimized)."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [
                (0, 255, 255),
                (255, 0, 128),
                (255, 255, 0),
            ]  # Default energy colors

        # Create coordinate meshgrids
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        center_x, center_y = width // 2, height // 2
        dx = x_coords - center_x
        dy = y_coords - center_y
        dist = np.sqrt(dx * dx + dy * dy)
        angle = np.arctan2(dy, dx)

        # Create concentric energy waves (vectorized)
        wave1 = np.sin(dist * 0.02 - current_time * 5) * 0.5
        wave2 = np.sin(dist * 0.015 - current_time * 3) * 0.3
        wave3 = np.sin(angle * 4 + current_time * 2) * 0.2

        # Combine with amplitude
        energy = (wave1 + wave2 + wave3 + amplitude * 0.8) * 0.3 + 0.1
        energy = np.clip(energy, 0, 1)

        # Use gradient colors for energy waves
        if len(colors) >= 2:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            # Interpolate between colors based on energy intensity
            r = (color1[0] * (1 - energy) + color2[0] * energy).astype(np.uint8)
            g = (color1[1] * (1 - energy) + color2[1] * energy).astype(np.uint8)
            b = (color1[2] * (1 - energy) + color2[2] * energy).astype(np.uint8)
        else:
            # Fallback to default
            r = (energy * 255 * 0.5).astype(np.uint8)
            g = (energy * 255 * 0.8).astype(np.uint8)
            b = (energy * 255).astype(np.uint8)

        frame[:, :, 0] = b
        frame[:, :, 1] = g
        frame[:, :, 2] = r

        return frame

    def _create_liquid_metal_background(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create liquid metal effect with custom gradient colors (optimized)."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [(192, 192, 192), (255, 215, 0)]  # Default silver/gold colors

        # Create coordinate meshgrids
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create flowing metal effect (vectorized)
        flow1 = np.sin(x_coords * 0.01 + current_time * 2) * 0.4
        flow2 = np.sin(y_coords * 0.008 + current_time * 1.5) * 0.3
        flow3 = np.sin((x_coords + y_coords) * 0.005 + current_time * 1.2) * 0.3

        # Metallic ripples
        dx = x_coords - width / 2
        dy = y_coords - height / 2
        dist = np.sqrt(dx * dx + dy * dy)
        ripple = np.sin(dist * 0.03 + current_time * 4) * 0.2

        # Combine with amplitude
        metal_value = (flow1 + flow2 + flow3 + ripple + amplitude * 0.4) * 0.3 + 0.3
        metal_value = np.clip(metal_value, 0, 1)

        # Use gradient colors for metallic effect
        if len(colors) >= 2:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            # Interpolate between colors based on metal value
            r = (color1[0] * (1 - metal_value) + color2[0] * metal_value).astype(
                np.uint8
            )
            g = (color1[1] * (1 - metal_value) + color2[1] * metal_value).astype(
                np.uint8
            )
            b = (color1[2] * (1 - metal_value) + color2[2] * metal_value).astype(
                np.uint8
            )
        else:
            # Fallback to default metallic colors
            base_color = (metal_value * 200 + 55).astype(np.uint8)
            r = (base_color * 0.9).astype(np.uint8)
            g = (base_color * 0.95).astype(np.uint8)
            b = base_color

        frame[:, :, 0] = b
        frame[:, :, 1] = g
        frame[:, :, 2] = r

        return frame

    def _create_cosmic_dust_background(
        self,
        frame,
        amplitude,
        current_time,
        frame_idx,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create cosmic dust field effect with custom gradient colors."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [
                (10, 10, 80),
                (150, 20, 100),
                (255, 100, 50),
            ]  # Default cosmic colors

        # Simple cosmic dust effect using noise
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create dust-like pattern
        dust1 = np.sin(x_coords * 0.05 + current_time * 0.5) * 0.3
        dust2 = np.sin(y_coords * 0.07 + current_time * 0.3) * 0.3
        dust3 = np.sin((x_coords + y_coords) * 0.03 + current_time * 0.8) * 0.4

        # Combine dust patterns
        dust_intensity = (dust1 + dust2 + dust3 + amplitude * 0.5) * 0.2 + 0.1
        dust_intensity = np.clip(dust_intensity, 0, 1)

        # Use gradient colors for cosmic dust
        if len(colors) >= 2:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            # Interpolate between colors based on dust intensity
            r = (color1[0] * (1 - dust_intensity) + color2[0] * dust_intensity).astype(
                np.uint8
            )
            g = (color1[1] * (1 - dust_intensity) + color2[1] * dust_intensity).astype(
                np.uint8
            )
            b = (color1[2] * (1 - dust_intensity) + color2[2] * dust_intensity).astype(
                np.uint8
            )
        else:
            # Fallback to default space colors
            r = (dust_intensity * 80 + 10).astype(np.uint8)
            g = (dust_intensity * 60 + 10).astype(np.uint8)
            b = (dust_intensity * 150 + 20).astype(np.uint8)

        frame[:, :, 0] = b
        frame[:, :, 1] = g
        frame[:, :, 2] = r

        return frame

    def _create_particle_field_background(
        self,
        frame,
        amplitude,
        current_time,
        frame_idx,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create particle field background with custom gradient colors."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [
                (255, 0, 100),
                (0, 255, 255),
                (100, 255, 0),
            ]  # Default particle colors

        # Simple particle field effect
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create particle-like pattern
        particle1 = np.sin(x_coords * 0.08 + current_time * 2) * 0.4
        particle2 = np.sin(y_coords * 0.06 + current_time * 1.5) * 0.3
        particle3 = np.sin((x_coords * y_coords) * 0.0001 + current_time * 3) * 0.3

        # Combine particle patterns
        particle_intensity = (
            particle1 + particle2 + particle3 + amplitude * 0.8
        ) * 0.3 + 0.2
        particle_intensity = np.clip(particle_intensity, 0, 1)

        # Use gradient colors for particle field
        if len(colors) >= 2:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            # Interpolate between colors based on particle intensity
            r = (
                color1[0] * (1 - particle_intensity) + color2[0] * particle_intensity
            ).astype(np.uint8)
            g = (
                color1[1] * (1 - particle_intensity) + color2[1] * particle_intensity
            ).astype(np.uint8)
            b = (
                color1[2] * (1 - particle_intensity) + color2[2] * particle_intensity
            ).astype(np.uint8)
        else:
            # Fallback to default energy field colors
            r = (particle_intensity * 100 + 20).astype(np.uint8)
            g = (particle_intensity * 150 + 20).astype(np.uint8)
            b = (particle_intensity * 200 + 40).astype(np.uint8)

        frame[:, :, 0] = b
        frame[:, :, 1] = g
        frame[:, :, 2] = r

        return frame

    def _create_morphing_shapes_background(
        self,
        frame,
        amplitude,
        current_time,
        frame_idx,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create morphing geometric shapes background with custom gradient colors."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [
                (150, 30, 200),
                (255, 80, 20),
                (200, 200, 60),
            ]  # Default morphing colors

        # Simple morphing effect using sinusoidal patterns
        y_coords, x_coords = np.meshgrid(
            np.arange(height), np.arange(width), indexing="ij"
        )

        # Create morphing pattern
        center_x, center_y = width // 2, height // 2
        dx = x_coords - center_x
        dy = y_coords - center_y
        dist = np.sqrt(dx * dx + dy * dy) / max(width, height) * 2
        angle = np.arctan2(dy, dx)

        # Morphing based on time and amplitude
        morph_time = current_time * 0.5
        morph_pattern = np.sin(angle * 4 + morph_time) * np.sin(
            dist * 3 + morph_time * 2
        )
        morph_intensity = (morph_pattern + amplitude * 0.8) * 0.4 + 0.3
        morph_intensity = np.clip(morph_intensity, 0, 1)

        # Use gradient colors for morphing shapes
        if len(colors) >= 2:
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            # Interpolate between colors based on morph intensity
            r = (
                color1[0] * (1 - morph_intensity) + color2[0] * morph_intensity
            ).astype(np.uint8)
            g = (
                color1[1] * (1 - morph_intensity) + color2[1] * morph_intensity
            ).astype(np.uint8)
            b = (
                color1[2] * (1 - morph_intensity) + color2[2] * morph_intensity
            ).astype(np.uint8)
        else:
            # Fallback to default morphing colors
            r = (morph_intensity * 150 + 30).astype(np.uint8)
            g = (morph_intensity * 80 + 20).astype(np.uint8)
            b = (morph_intensity * 200 + 60).astype(np.uint8)

        frame[:, :, 0] = b
        frame[:, :, 1] = g
        frame[:, :, 2] = r

        return frame

    def create_fallback_background(
        self, gradient_style: str = "default", custom_colors: list = None
    ) -> Path:
        """Create a gradient background with various styles.

        Args:
            gradient_style: Style of gradient ("default", "dark_teal_orange", "sunset", "ocean",
                          "purple_pink", "forest", "midnight", "fire", "arctic", "cosmic")
            custom_colors: List of RGB tuples for custom gradient, e.g. [(255,0,0), (0,255,0), (0,0,255)]
        """
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)

        # Define predefined gradient styles
        gradient_presets = {
            "default": [
                (30, 50, 120),
                (130, 130, 255),
            ],  # Deep blue to purple (original)
            "dark_teal_orange": [
                (0, 40, 40),
                (255, 140, 60),
            ],  # Dark teal to vibrant orange
            "sunset": [(255, 94, 77), (255, 154, 0), (255, 206, 84)],  # Sunset colors
            "ocean": [(0, 119, 190), (0, 180, 216), (144, 224, 239)],  # Ocean blues
            "purple_pink": [(106, 17, 203), (255, 61, 127)],  # Deep purple to pink
            "forest": [
                (34, 139, 34),
                (107, 142, 35),
                (255, 215, 0),
            ],  # Forest green to gold
            "midnight": [
                (25, 25, 112),
                (138, 43, 226),
                (75, 0, 130),
            ],  # Midnight blues and purples
            "fire": [
                (139, 0, 0),
                (255, 69, 0),
                (255, 215, 0),
            ],  # Dark red to orange to gold
            "arctic": [
                (176, 224, 230),
                (135, 206, 235),
                (70, 130, 180),
            ],  # Arctic blues
            "cosmic": [
                (75, 0, 130),
                (138, 43, 226),
                (255, 20, 147),
                (255, 215, 0),
            ],  # Deep space colors
            # 20 NUEVOS GRADIENTES HERMOSOS
            "cherry_blossom": [
                (255, 183, 197),
                (255, 105, 180),
                (255, 20, 147),
            ],  # Flor de cerezo
            "tropical": [
                (0, 255, 127),
                (255, 215, 0),
                (255, 69, 0),
            ],  # Tropical verde-dorado-naranja
            "lavender_mist": [
                (230, 230, 250),
                (147, 112, 219),
                (138, 43, 226),
            ],  # Niebla de lavanda
            "golden_hour": [
                (255, 223, 0),
                (255, 140, 0),
                (255, 69, 0),
                (139, 0, 0),
            ],  # Hora dorada
            "emerald_sea": [
                (0, 128, 128),
                (32, 178, 170),
                (72, 209, 204),
                (175, 238, 238),
            ],  # Mar esmeralda
            "rose_gold": [
                (183, 110, 121),
                (255, 192, 203),
                (255, 215, 0),
            ],  # Oro rosa
            "northern_lights": [
                (0, 255, 127),
                (0, 191, 255),
                (138, 43, 226),
                (255, 20, 147),
            ],  # Aurora boreal
            "desert_sand": [
                (218, 165, 32),
                (255, 215, 0),
                (255, 160, 122),
                (250, 128, 114),
            ],  # Arena del desierto
            "deep_ocean": [
                (0, 0, 139),
                (0, 100, 148),
                (0, 191, 255),
                (135, 206, 235),
            ],  # Océano profundo
            "neon_cyber": [
                (255, 0, 255),
                (0, 255, 255),
                (57, 255, 20),
                (255, 255, 0),
            ],  # Neón cyberpunk
            "autumn_leaves": [
                (255, 69, 0),
                (255, 140, 0),
                (255, 215, 0),
                (139, 69, 19),
            ],  # Hojas de otoño
            "moonlight": [
                (25, 25, 112),
                (72, 61, 139),
                (176, 196, 222),
                (245, 245, 245),
            ],  # Luz de luna
            "tropical_sunset": [
                (255, 94, 77),
                (255, 154, 0),
                (255, 215, 0),
                (255, 20, 147),
                (138, 43, 226),
            ],  # Atardecer tropical
            "winter_frost": [
                (176, 224, 230),
                (173, 216, 230),
                (135, 206, 235),
                (70, 130, 180),
                (25, 25, 112),
            ],  # Escarcha invernal
            "sakura_dream": [
                (255, 228, 225),
                (255, 182, 193),
                (255, 105, 180),
                (219, 112, 147),
            ],  # Sueño de sakura
            "volcanic": [
                (139, 0, 0),
                (178, 34, 34),
                (255, 69, 0),
                (255, 215, 0),
                (255, 255, 255),
            ],  # Volcánico
            "electric_blue": [
                (0, 0, 139),
                (0, 191, 255),
                (0, 255, 255),
                (255, 255, 255),
            ],  # Azul eléctrico
            "jungle_green": [
                (0, 100, 0),
                (34, 139, 34),
                (50, 205, 50),
                (144, 238, 144),
            ],  # Verde selva
            "royal_purple": [
                (75, 0, 130),
                (106, 17, 203),
                (138, 43, 226),
                (218, 112, 214),
            ],  # Púrpura real
            "cotton_candy": [
                (255, 192, 203),
                (255, 182, 193),
                (221, 160, 221),
                (238, 130, 238),
                (255, 20, 147),
            ],  # Algodón de azúcar
        }

        # Use custom colors if provided, otherwise use preset
        if custom_colors and len(custom_colors) >= 2:
            colors = custom_colors
        else:
            colors = gradient_presets.get(gradient_style, gradient_presets["default"])

        # Create gradient
        num_colors = len(colors)
        if num_colors == 2:
            # Simple two-color gradient
            for y in range(self.height):
                ratio = y / self.height
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
                color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                draw.line([(0, y), (self.width, y)], fill=color)
        else:
            # Multi-color gradient
            for y in range(self.height):
                ratio = y / self.height
                # Determine which color segment we're in
                segment_size = 1.0 / (num_colors - 1)
                segment_index = min(int(ratio / segment_size), num_colors - 2)
                local_ratio = (ratio - segment_index * segment_size) / segment_size

                # Interpolate between the two colors in this segment
                color1 = colors[segment_index]
                color2 = colors[segment_index + 1]

                r = int(color1[0] + (color2[0] - color1[0]) * local_ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * local_ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * local_ratio)
                color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                draw.line([(0, y), (self.width, y)], fill=color)

        # Add some blur for smoothness
        image = image.filter(ImageFilter.GaussianBlur(radius=2))

        # Save to temporary file
        temp_dir = Path(tempfile.gettempdir())
        bg_path = (
            temp_dir / f"gradient_bg_{gradient_style}_{random.randint(1000, 9999)}.jpg"
        )
        image.save(bg_path, quality=95)

        return bg_path

    def extract_audio_features(
        self, audio_path: Path, max_duration: float = None
    ) -> tuple:
        """Extract audio features for waveform animation.

        Args:
            max_duration: If provided, only process first max_duration seconds of audio
        """
        try:
            # Load audio file
            if max_duration is not None:
                # Load only the first max_duration seconds
                y, sr = librosa.load(str(audio_path), duration=max_duration)
            else:
                y, sr = librosa.load(str(audio_path))

            # Get audio duration
            duration = librosa.get_duration(y=y, sr=sr)

            # Extract features for visualization
            # RMS energy for overall amplitude
            rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]

            # Spectral centroid for frequency content
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

            # Tempo and beat tracking
            try:
                tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            except:
                tempo = 120  # Default tempo
                beats = np.arange(0, len(y), sr // 2)  # Default beats every 0.5 seconds

            return {
                "duration": duration,
                "rms": rms,
                "spectral_centroids": spectral_centroids,
                "tempo": tempo,
                "beats": beats,
                "sr": sr,
                "audio_data": y,
            }
        except Exception as e:
            print(f"Error extracting audio features: {e}")
            return None

    def create_waveform_frame(
        self,
        bg_image: np.ndarray,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        style: str = "circular",
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ) -> np.ndarray:
        """Create a single frame with waveform animation."""
        frame = bg_image.copy()

        if audio_features is None:
            return frame

        # Calculate current time position
        current_time = (frame_idx / total_frames) * audio_features["duration"]

        # Get current audio amplitude
        rms_idx = min(
            int(current_time * len(audio_features["rms"]) / audio_features["duration"]),
            len(audio_features["rms"]) - 1,
        )
        current_amplitude = audio_features["rms"][rms_idx]

        # Normalize amplitude (0-1)
        max_amplitude = np.max(audio_features["rms"])
        normalized_amplitude = (
            current_amplitude / max_amplitude if max_amplitude > 0 else 0
        )

        # Create waveform visualization based on style
        if style == "sine":
            self._draw_sine_waveform(
                frame, normalized_amplitude, current_time, audio_features
            )
        elif style == "mathematical" or style == "fractal":
            self._draw_mathematical_forms(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
            )
        elif style == "julia" or style == "mandelbrot":
            self._draw_julia_fractal(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
            )
        elif style == "psychedelic" or style == "circles":
            self._draw_psychedelic_circles(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
            )
        elif style == "fluid" or style == "liquid":
            self._draw_fluid_waves(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "particles" or style == "sand":
            self._draw_particle_fall(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "morph" or style == "shapes":
            self._draw_morphing_shapes(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
            )
        elif style == "kaleidoscope" or style == "mirror":
            self._draw_kaleidoscope(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-mandala":
            self._draw_k_mandala(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-crystal":
            self._draw_k_crystal(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-flower":
            self._draw_k_flower(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-sacred":
            self._draw_k_sacred(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-tribal":
            self._draw_k_tribal(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-laser":
            self._draw_k_laser(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-web":
            self._draw_k_web(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-spiral":
            self._draw_k_spiral(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-diamond":
            self._draw_k_diamond(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "k-stars":
            self._draw_k_stars(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "breathing" or style == "zen":
            self._draw_breathing_patterns(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
            )
        elif style == "matrix" or style == "rain":
            self._draw_matrix_rain(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "starfield" or style == "space":
            self._draw_starfield(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "network" or style == "web":
            self._draw_network_web(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "swarm" or style == "flock":
            self._draw_particle_swarm(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        elif style == "explosion" or style == "fireworks":
            self._draw_fireworks_explosion(
                frame,
                normalized_amplitude,
                current_time,
                audio_features,
                frame_idx,
                total_frames,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
        else:
            self._draw_waveform(
                frame, normalized_amplitude, current_time, audio_features
            )

        return frame

    def _draw_waveform(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
    ):
        """Draw animated waveform on the frame."""
        center_x = self.width // 2
        center_y = self.height // 2

        # Create circular waveform - adjust size based on orientation
        num_bars = 64
        if self.orientation == "horizontal":
            max_radius = min(280, self.height // 4)  # Fit within horizontal frame
            min_radius = max(60, self.height // 12)
        else:
            max_radius = 200
            min_radius = 80

        for i in range(num_bars):
            angle = (2 * np.pi * i) / num_bars

            # Create animated effect based on audio
            bar_amplitude = amplitude * (1 + 0.3 * np.sin(current_time * 2 + i * 0.1))
            bar_height = min_radius + (max_radius - min_radius) * bar_amplitude

            # Calculate bar positions (clamp to frame bounds)
            inner_x = int(
                np.clip(center_x + min_radius * np.cos(angle), 0, self.width - 1)
            )
            inner_y = int(
                np.clip(center_y + min_radius * np.sin(angle), 0, self.height - 1)
            )
            outer_x = int(
                np.clip(center_x + bar_height * np.cos(angle), 0, self.width - 1)
            )
            outer_y = int(
                np.clip(center_y + bar_height * np.sin(angle), 0, self.height - 1)
            )

            # Color based on frequency content (if available)
            spectral_idx = min(
                int(
                    current_time
                    * len(audio_features["spectral_centroids"])
                    / audio_features["duration"]
                ),
                len(audio_features["spectral_centroids"]) - 1,
            )
            spectral_value = audio_features["spectral_centroids"][spectral_idx]

            # Map spectral centroid to color (clamp to valid range)
            hue = int(
                np.clip((spectral_value / 4000) * 180, 0, 179)
            )  # HSV hue is 0-179 in OpenCV
            color = cv2.applyColorMap(
                np.array([[[hue]]], dtype=np.uint8), cv2.COLORMAP_HSV
            )[0, 0]
            color = (
                int(np.clip(color[0], 0, 255)),
                int(np.clip(color[1], 0, 255)),
                int(np.clip(color[2], 0, 255)),
            )

            # Draw the bar with some transparency effect
            cv2.line(frame, (inner_x, inner_y), (outer_x, outer_y), color, 3)

        # Add central circle
        circle_radius = int(min_radius * 0.7)
        cv2.circle(frame, (center_x, center_y), circle_radius, (255, 255, 255), 2)

        # Add pulsing effect in center
        pulse_radius = int(
            np.clip(circle_radius * 0.5 * (1 + 0.3 * amplitude), 1, circle_radius)
        )
        cv2.circle(frame, (center_x, center_y), pulse_radius, (255, 255, 255), -1)

    def _draw_sine_waveform(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
    ):
        """Draw animated sine waveform across the frame."""
        if self.orientation == "horizontal":
            # For horizontal orientation, draw across width
            self._draw_sine_waveform_horizontal(
                frame, amplitude, current_time, audio_features
            )
        else:
            # For vertical orientation, draw across height
            self._draw_sine_waveform_vertical(
                frame, amplitude, current_time, audio_features
            )

    def _draw_sine_waveform_vertical(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
    ):
        """Draw animated sine waveform across the full height of the video."""
        center_x = self.width // 2

        # Parameters for the sine wave
        wave_width = 200  # Maximum width of the wave
        frequency = 2.0  # Frequency of the sine wave
        phase_speed = 3.0  # Speed of phase animation

        # Current phase based on time
        phase = current_time * phase_speed

        # Draw sine wave across the full height
        points = []
        for y in range(0, self.height, 4):  # Step by 4 pixels for performance
            # Normalize y to range [0, 1]
            y_norm = y / self.height

            # Create sine wave with audio-reactive amplitude
            wave_amplitude = (
                wave_width
                * amplitude
                * (0.5 + 0.5 * np.sin(y_norm * frequency * np.pi + phase))
            )

            # Calculate x position
            x = int(
                np.clip(
                    center_x
                    + wave_amplitude * np.sin(y_norm * frequency * 2 * np.pi + phase),
                    0,
                    self.width - 1,
                )
            )

            points.append((x, y))

        # Draw the main sine wave
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Color based on position and amplitude
                color_intensity = int(
                    np.clip(
                        128
                        + 127
                        * amplitude
                        * np.sin(points[i][1] / self.height * 4 * np.pi + current_time),
                        0,
                        255,
                    )
                )
                color = (color_intensity, 255 - color_intensity // 2, 255)

                cv2.line(frame, points[i], points[i + 1], color, 3)

        # Draw secondary waves for richness
        for offset in [-0.3, 0.3]:
            secondary_points = []
            for y in range(0, self.height, 8):
                y_norm = y / self.height
                wave_amplitude = (
                    wave_width
                    * amplitude
                    * 0.6
                    * (0.5 + 0.5 * np.sin(y_norm * frequency * np.pi + phase + offset))
                )
                x = int(
                    np.clip(
                        center_x
                        + wave_amplitude
                        * np.sin(y_norm * frequency * 2 * np.pi + phase + offset),
                        0,
                        self.width - 1,
                    )
                )
                secondary_points.append((x, y))

            if len(secondary_points) > 1:
                for i in range(len(secondary_points) - 1):
                    color = (150, 150, 255)  # Lighter blue for secondary waves
                    cv2.line(
                        frame, secondary_points[i], secondary_points[i + 1], color, 2
                    )

        # Add vertical center line with pulsing effect
        line_alpha = int(np.clip(50 + 100 * amplitude, 50, 150))
        cv2.line(frame, (center_x, 0), (center_x, self.height), (255, 255, 255), 1)

    def _draw_sine_waveform_horizontal(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
    ):
        """Draw animated sine waveform across the full width of the video."""
        center_y = self.height // 2

        # Parameters for the sine wave
        wave_height = min(150, self.height // 3)  # Maximum height of the wave
        frequency = 2.0  # Frequency of the sine wave
        phase_speed = 3.0  # Speed of phase animation

        # Current phase based on time
        phase = current_time * phase_speed

        # Draw sine wave across the full width
        points = []
        for x in range(0, self.width, 4):  # Step by 4 pixels for performance
            # Normalize x to range [0, 1]
            x_norm = x / self.width

            # Create sine wave with audio-reactive amplitude
            wave_amplitude = (
                wave_height
                * amplitude
                * (0.5 + 0.5 * np.sin(x_norm * frequency * np.pi + phase))
            )

            # Calculate y position
            y = int(
                np.clip(
                    center_y
                    + wave_amplitude * np.sin(x_norm * frequency * 2 * np.pi + phase),
                    0,
                    self.height - 1,
                )
            )

            points.append((x, y))

        # Draw the main sine wave
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Color based on position and amplitude
                color_intensity = int(
                    np.clip(
                        128
                        + 127
                        * amplitude
                        * np.sin(points[i][0] / self.width * 4 * np.pi + current_time),
                        0,
                        255,
                    )
                )
                color = (color_intensity, 255 - color_intensity // 2, 255)

                cv2.line(frame, points[i], points[i + 1], color, 3)

        # Draw secondary waves for richness
        for offset in [-0.3, 0.3]:
            secondary_points = []
            for x in range(0, self.width, 8):
                x_norm = x / self.width
                wave_amplitude = (
                    wave_height
                    * amplitude
                    * 0.6
                    * (0.5 + 0.5 * np.sin(x_norm * frequency * np.pi + phase + offset))
                )
                y = int(
                    np.clip(
                        center_y
                        + wave_amplitude
                        * np.sin(x_norm * frequency * 2 * np.pi + phase + offset),
                        0,
                        self.height - 1,
                    )
                )
                secondary_points.append((x, y))

            if len(secondary_points) > 1:
                for i in range(len(secondary_points) - 1):
                    color = (150, 150, 255)  # Lighter blue for secondary waves
                    cv2.line(
                        frame, secondary_points[i], secondary_points[i + 1], color, 2
                    )

        # Add horizontal center line with pulsing effect
        line_alpha = int(np.clip(50 + 100 * amplitude, 50, 150))
        cv2.line(frame, (0, center_y), (self.width, center_y), (255, 255, 255), 1)

    def _draw_mathematical_forms(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
    ):
        """Draw mesmerizing mathematical forms that respond to audio."""
        center_x = self.width // 2
        center_y = self.height // 2

        # Enhanced amplitude with temporal smoothing
        enhanced_amplitude = amplitude * (1 + 0.5 * np.sin(current_time * 4))

        # Color palette based on audio frequency content
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]

        # Create dynamic color scheme
        hue_shift = (spectral_value / 4000) * 360 + current_time * 30
        base_hue = int(hue_shift) % 360

        # 1. Fibonacci Spiral with audio responsiveness
        self._draw_fibonacci_spiral(
            frame, center_x, center_y, enhanced_amplitude, current_time, base_hue
        )

        # 2. Lissajous curves
        self._draw_lissajous_curves(
            frame, center_x, center_y, enhanced_amplitude, current_time, base_hue
        )

        # 3. Polar roses (mathematical flowers)
        self._draw_polar_roses(
            frame, center_x, center_y, enhanced_amplitude, current_time, base_hue
        )

        # 4. Interference patterns
        self._draw_interference_patterns(
            frame, center_x, center_y, enhanced_amplitude, current_time, base_hue
        )

        # 5. Fractal-like recursive patterns
        self._draw_recursive_patterns(
            frame, center_x, center_y, enhanced_amplitude, current_time, base_hue
        )

    def _draw_fibonacci_spiral(
        self, frame, center_x, center_y, amplitude, time, base_hue
    ):
        """Draw animated Fibonacci spiral that responds to audio."""
        golden_ratio = (1 + math.sqrt(5)) / 2
        max_radius = 300 * (1 + amplitude * 0.5)

        points = []
        for i in range(200):
            # Fibonacci spiral equation with time animation
            angle = i * 0.2 + time * 2
            radius = 5 * math.sqrt(i) * (1 + amplitude * 0.3 * math.sin(angle))

            if radius > max_radius:
                break

            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))

            if 0 <= x < self.width and 0 <= y < self.height:
                points.append((x, y))

        # Draw spiral with varying colors
        for i in range(1, len(points)):
            color_intensity = int(255 * (i / len(points)) * (1 + amplitude))
            color = self._hsv_to_bgr(base_hue + i * 2, 255, min(255, color_intensity))
            cv2.line(frame, points[i - 1], points[i], color, 2)

    def _draw_lissajous_curves(
        self, frame, center_x, center_y, amplitude, time, base_hue
    ):
        """Draw animated Lissajous curves."""
        a, b = 3, 4  # Frequency ratios
        scale = 150 * (1 + amplitude * 0.4)
        phase_shift = time * 3

        points = []
        for t in np.linspace(0, 2 * np.pi, 200):
            x = int(
                center_x + scale * math.sin(a * t + phase_shift) * (1 + amplitude * 0.3)
            )
            y = int(center_y + scale * math.sin(b * t) * (1 + amplitude * 0.3))

            if 0 <= x < self.width and 0 <= y < self.height:
                points.append((x, y))

        # Draw multiple Lissajous with different parameters
        for offset, scale_factor in [(0, 1.0), (np.pi / 3, 0.7), (np.pi / 2, 0.4)]:
            offset_points = []
            for t in np.linspace(0, 2 * np.pi, 150):
                x = int(
                    center_x
                    + scale * scale_factor * math.sin(a * t + phase_shift + offset)
                )
                y = int(center_y + scale * scale_factor * math.sin(b * t + offset))

                if 0 <= x < self.width and 0 <= y < self.height:
                    offset_points.append((x, y))

            # Draw curve
            for i in range(1, len(offset_points)):
                alpha = int(255 * scale_factor * (1 + amplitude))
                color = self._hsv_to_bgr(
                    (base_hue + offset * 60) % 360, 200, min(255, alpha)
                )
                cv2.line(frame, offset_points[i - 1], offset_points[i], color, 2)

    def _draw_polar_roses(self, frame, center_x, center_y, amplitude, time, base_hue):
        """Draw animated polar rose patterns (mathematical flowers)."""
        # Different rose patterns with varying petals
        for k, scale_factor, color_offset in [(2, 1.0, 0), (3, 0.8, 60), (5, 0.6, 120)]:
            points = []
            for theta in np.linspace(0, 4 * np.pi, 300):
                # Rose equation: r = cos(k * theta) with audio modulation
                r = (
                    abs(math.cos(k * theta))
                    * 100
                    * scale_factor
                    * (1 + amplitude * 0.6)
                )

                # Add time-based rotation and pulsing
                animated_theta = theta + time * (1 + k * 0.3)
                x = int(center_x + r * math.cos(animated_theta))
                y = int(center_y + r * math.sin(animated_theta))

                if 0 <= x < self.width and 0 <= y < self.height:
                    points.append((x, y))

            # Draw rose pattern
            for i in range(1, len(points)):
                intensity = int(255 * scale_factor * (1 + amplitude * 0.5))
                color = self._hsv_to_bgr(
                    (base_hue + color_offset + i) % 360, 180, min(255, intensity)
                )
                cv2.line(frame, points[i - 1], points[i], color, 2)

    def _draw_interference_patterns(
        self, frame, center_x, center_y, amplitude, time, base_hue
    ):
        """Draw wave interference patterns."""
        # Create multiple wave sources
        sources = [
            (center_x - 200, center_y - 300),
            (center_x + 200, center_y - 300),
            (center_x, center_y + 200),
        ]

        wave_length = 50 * (1 + amplitude * 0.3)

        # Sample points for interference calculation
        for y in range(0, self.height, 8):
            for x in range(0, self.width, 8):
                # Calculate interference from all sources
                total_amplitude = 0
                for i, (sx, sy) in enumerate(sources):
                    distance = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
                    wave_phase = (distance / wave_length) * 2 * np.pi + time * (2 + i)
                    total_amplitude += math.sin(wave_phase)

                # Normalize and enhance with audio
                normalized_amp = (total_amplitude / len(sources)) * amplitude

                if abs(normalized_amp) > 0.5:  # Only draw significant interference
                    intensity = int(abs(normalized_amp) * 255)
                    color = self._hsv_to_bgr(
                        base_hue + intensity // 4, 150, min(255, intensity)
                    )
                    cv2.circle(frame, (x, y), 2, color, -1)

    def _draw_recursive_patterns(
        self, frame, center_x, center_y, amplitude, time, base_hue
    ):
        """Draw recursive fractal-like patterns."""

        def draw_recursive_branches(x, y, length, angle, depth, max_depth):
            if depth >= max_depth or length < 5:
                return

            # Calculate end point
            end_x = int(x + length * math.cos(angle))
            end_y = int(y + length * math.sin(angle))

            # Ensure points are within bounds
            if not (0 <= end_x < self.width and 0 <= end_y < self.height):
                return

            # Color based on depth and audio
            color_intensity = int(255 * (1 - depth / max_depth) * (1 + amplitude))
            color = self._hsv_to_bgr(
                (base_hue + depth * 30 + time * 50) % 360,
                200,
                min(255, color_intensity),
            )

            # Draw line
            cv2.line(frame, (int(x), int(y)), (end_x, end_y), color, max(1, 4 - depth))

            # Recursive branches with audio-influenced angles
            branch_angle = math.pi / 4 * (1 + amplitude * 0.3)
            new_length = length * 0.7 * (1 + amplitude * 0.2)

            draw_recursive_branches(
                end_x, end_y, new_length, angle - branch_angle, depth + 1, max_depth
            )
            draw_recursive_branches(
                end_x, end_y, new_length, angle + branch_angle, depth + 1, max_depth
            )

        # Draw multiple recursive trees
        initial_length = 80 * (1 + amplitude * 0.5)
        max_depth = 6

        # Main tree upward
        draw_recursive_branches(
            center_x,
            center_y + 200,
            initial_length,
            -math.pi / 2 + time * 0.1,
            0,
            max_depth,
        )

        # Side trees with different orientations
        for angle_offset in [math.pi / 3, -math.pi / 3, math.pi]:
            offset_x = center_x + 150 * math.cos(angle_offset + time * 0.2)
            offset_y = center_y + 150 * math.sin(angle_offset + time * 0.2)
            draw_recursive_branches(
                offset_x,
                offset_y,
                initial_length * 0.6,
                angle_offset + math.pi + time * 0.3,
                0,
                max_depth - 1,
            )

    def _hsv_to_bgr(self, h, s, v):
        """Convert HSV to BGR color space for OpenCV."""
        # Normalize values
        h = max(0, min(360, h)) / 360.0
        s = max(0, min(255, s)) / 255.0
        v = max(0, min(255, v)) / 255.0

        # HSV to RGB conversion
        c = v * s
        x = c * (1 - abs((h * 6) % 2 - 1))
        m = v - c

        if 0 <= h < 1 / 6:
            r, g, b = c, x, 0
        elif 1 / 6 <= h < 2 / 6:
            r, g, b = x, c, 0
        elif 2 / 6 <= h < 3 / 6:
            r, g, b = 0, c, x
        elif 3 / 6 <= h < 4 / 6:
            r, g, b = 0, x, c
        elif 4 / 6 <= h < 5 / 6:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        # Convert to 0-255 range and BGR format for OpenCV
        return (int((b + m) * 255), int((g + m) * 255), int((r + m) * 255))

    def _get_particle_color(
        self,
        particle_id: int,
        base_hue: int,
        amplitude: float,
        time: float,
        gradient_style: str = "default",
        custom_colors: list = None,
        color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ) -> tuple:
        """Generate particle color based on the selected color scheme.

        Args:
            particle_id: Unique identifier for the particle
            base_hue: Base hue derived from audio spectrum
            amplitude: Current audio amplitude
            time: Current time
            gradient_style: Background gradient style for similarity scheme
            custom_colors: Custom background colors
            color_scheme: Color scheme type:
                - "multicolor": Rainbow colors (existing behavior)
                - "background": Colors similar to background gradient
                - "dissonant": Contrasting/clashing colors
                - "triadic": Triadic complementary color scheme
                - "monochrome": All particles use exact background gradient colors
            particle_gradient_style: Specific gradient style for particles (overrides gradient_style)
            particle_custom_colors: Custom colors specific for particles (overrides custom_colors)
        """
        # Determine which gradient colors to use for particles
        effective_gradient_style = (
            particle_gradient_style if particle_gradient_style else gradient_style
        )
        effective_custom_colors = (
            particle_custom_colors if particle_custom_colors else custom_colors
        )

        if color_scheme == "background":
            return self._get_background_similar_color(
                particle_id,
                base_hue,
                amplitude,
                time,
                effective_gradient_style,
                effective_custom_colors,
            )
        elif color_scheme == "dissonant":
            return self._get_dissonant_color(particle_id, base_hue, amplitude, time)
        elif color_scheme == "triadic":
            return self._get_triadic_color(particle_id, base_hue, amplitude, time)
        elif color_scheme == "monochrome":
            return self._get_monochrome_color(
                particle_id,
                base_hue,
                amplitude,
                time,
                effective_gradient_style,
                effective_custom_colors,
            )
        else:  # multicolor (default)
            return self._get_multicolor_particle(particle_id, base_hue, amplitude, time)

    def _get_multicolor_particle(
        self, particle_id: int, base_hue: int, amplitude: float, time: float
    ) -> tuple:
        """Generate rainbow/multicolor particle (existing behavior)."""
        particle_hue = (base_hue + particle_id * 3 + time * 20) % 360
        particle_brightness = int(120 + 135 * amplitude)
        return self._hsv_to_bgr(particle_hue, 180, min(255, particle_brightness))

    def _get_background_similar_color(
        self,
        particle_id: int,
        base_hue: int,
        amplitude: float,
        time: float,
        gradient_style: str,
        custom_colors: list,
    ) -> tuple:
        """Generate colors similar to the background gradient."""
        # Get background gradient colors
        gradient_colors = self._get_current_gradient_colors(
            gradient_style, custom_colors
        )

        # Pick a base color from the gradient
        color_index = particle_id % len(gradient_colors)
        base_color = gradient_colors[color_index]

        # Convert to HSV for easier manipulation
        base_hue_bg = self._rgb_to_hsv(base_color[0], base_color[1], base_color[2])[0]

        # Add slight variation while staying close to background
        hue_variation = (particle_id * 5 + time * 10) % 60 - 30  # ±30 degrees
        final_hue = (base_hue_bg + hue_variation) % 360

        # Brightness varies with audio
        brightness = int(100 + 100 * amplitude + (particle_id % 50))

        # Saturation slightly higher than background for visibility
        saturation = min(255, 150 + int(50 * amplitude))

        return self._hsv_to_bgr(final_hue, saturation, min(255, brightness))

    def _get_dissonant_color(
        self, particle_id: int, base_hue: int, amplitude: float, time: float
    ) -> tuple:
        """Generate dissonant/contrasting colors that clash."""
        # Use split-complementary + harsh transitions for discord
        offset_options = [150, 180, 210, 270]  # Harsh angular separations
        offset = offset_options[particle_id % len(offset_options)]

        dissonant_hue = (base_hue + offset + particle_id * 7) % 360

        # High saturation for maximum clash
        saturation = 220 + int(35 * amplitude)

        # Varied brightness with sharp contrasts
        brightness_base = 180 if particle_id % 2 == 0 else 80
        brightness = int(brightness_base + 75 * amplitude)

        return self._hsv_to_bgr(
            dissonant_hue, min(255, saturation), min(255, brightness)
        )

    def _get_triadic_color(
        self, particle_id: int, base_hue: int, amplitude: float, time: float
    ) -> tuple:
        """Generate triadic complementary colors (three colors 120° apart)."""
        # Three colors equally spaced on color wheel
        triadic_offsets = [0, 120, 240]
        color_index = particle_id % 3
        triadic_hue = (base_hue + triadic_offsets[color_index] + time * 5) % 360

        # Harmonious saturation and brightness
        saturation = 160 + int(60 * amplitude)
        brightness = int(140 + 80 * amplitude + (particle_id % 40))

        return self._hsv_to_bgr(triadic_hue, min(255, saturation), min(255, brightness))

    def _get_monochrome_color(
        self,
        particle_id: int,
        base_hue: int,
        amplitude: float,
        time: float,
        gradient_style: str,
        custom_colors: list,
    ) -> tuple:
        """Generate monochrome colors using exact background gradient colors."""
        # Get background gradient colors
        gradient_colors = self._get_current_gradient_colors(
            gradient_style, custom_colors
        )

        # Use only colors from the gradient - cycle through them
        color_index = particle_id % len(gradient_colors)
        base_color = gradient_colors[color_index]

        # Very minimal variation - just brightness changes with audio
        brightness_factor = 0.7 + 0.3 * amplitude  # Range: 0.7 to 1.0

        # Apply brightness variation to the exact gradient color
        adjusted_r = int(base_color[0] * brightness_factor)
        adjusted_g = int(base_color[1] * brightness_factor)
        adjusted_b = int(base_color[2] * brightness_factor)

        # Ensure values stay in valid range
        adjusted_r = max(0, min(255, adjusted_r))
        adjusted_g = max(0, min(255, adjusted_g))
        adjusted_b = max(0, min(255, adjusted_b))

        # Return in BGR format for OpenCV
        return (adjusted_b, adjusted_g, adjusted_r)

    def _rgb_to_hsv(self, r: int, g: int, b: int) -> tuple:
        """Convert RGB to HSV values."""
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val

        # Hue calculation
        if diff == 0:
            h = 0
        elif max_val == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_val == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360

        # Saturation calculation
        s = 0 if max_val == 0 else (diff / max_val) * 255

        # Value calculation
        v = max_val * 255

        return (h, s, v)

    def _draw_julia_fractal(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
    ):
        """Draw Julia set with infinite zoom that responds to audio."""

        # Only recalculate Julia every few frames for better performance
        if not hasattr(self, "_julia_cache") or frame_idx % 3 == 0:
            # Visually interesting and colorful zoom locations (avoiding black areas)
            zoom_points = [
                (-0.7269, 0.1889),  # Classic spiral - very colorful
                (-0.74529, 0.11307),  # Beautiful spirals - lots of detail
                (-0.7463, 0.1102),  # Elephant valley - intricate patterns
                (-0.16, 1.0407),  # Top area - colorful swirls
                (-0.8, 0.156),  # Detailed fractal boundary
                (-0.74343, 0.13182),  # Lightning pattern - high contrast
            ]

            # Cycle through zoom points based on time (faster cycling)
            cycle_time = 20.0  # 20 seconds per zoom point (faster)
            point_index = int(current_time / cycle_time) % len(zoom_points)
            local_time = (current_time % cycle_time) / cycle_time

            # Current zoom point
            center_x, center_y = zoom_points[point_index]

            # Slower, more controlled zoom to stay in interesting areas
            base_zoom = 2.0 ** (local_time * 8)  # Much slower zoom
            audio_zoom_factor = 1 + amplitude * 0.15
            zoom = base_zoom * audio_zoom_factor

            # Limit zoom to avoid getting too deep into black areas
            zoom = min(zoom, 1000)  # Max zoom cap

            # Audio-reactive center perturbation
            perturbation = amplitude * 0.0005  # Reduced perturbation
            center_x += perturbation * math.sin(current_time * 3)
            center_y += perturbation * math.cos(current_time * 4)

            # Calculate Julia parameters
            width_range = 3.0 / zoom
            height_range = width_range * (self.height / self.width)

            x_min = center_x - width_range / 2
            x_max = center_x + width_range / 2
            y_min = center_y - height_range / 2
            y_max = center_y + height_range / 2

            # Ultra-low iterations for maximum speed
            max_iter = min(20 + int(amplitude * 15), 35)  # Máximo 35 iteraciones

            # Extremely aggressive resolution scaling
            if zoom > 500:  # High zoom
                scale_factor = 0.15  # Very low resolution
            elif zoom > 100:  # Medium zoom
                scale_factor = 0.2
            elif zoom > 50:  # Low zoom
                scale_factor = 0.25
            else:
                scale_factor = 0.3  # Still very reduced

            # Calculate actual dimensions
            calc_width = int(self.width * scale_factor)
            calc_height = int(self.height * scale_factor)

            # Create coordinate arrays for vectorized computation
            x = np.linspace(x_min, x_max, calc_width)
            y = np.linspace(y_min, y_max, calc_height)
            X, Y = np.meshgrid(x, y)
            C = X + 1j * Y

            # Calculate Julia set
            julia_set = self._calculate_julia_vectorized(C, max_iter)

            # Resize back to full resolution if needed (using faster interpolation)
            if scale_factor < 1.0:
                julia_set = cv2.resize(
                    julia_set.astype(np.float32),
                    (self.width, self.height),
                    interpolation=cv2.INTER_NEAREST,  # Much faster than INTER_LINEAR
                ).astype(np.int32)

            # Get background gradient colors for the fractal
            gradient_colors = self._get_current_gradient_colors(
                gradient_style, custom_colors
            )

            # Color the fractal using the background gradient
            colored_fractal = self._color_julia(
                julia_set, max_iter, gradient_colors, amplitude, current_time
            )

            # Check if the area is too dark/black and adjust alpha accordingly
            # Calculate average brightness to avoid showing boring black areas
            gray_fractal = cv2.cvtColor(colored_fractal, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray_fractal)

            # If area is too dark, reduce visibility to let background show more
            if avg_brightness < 30:  # Very dark area
                alpha = 0.3 + amplitude * 0.1  # Show more background
            elif avg_brightness < 60:  # Somewhat dark
                alpha = 0.5 + amplitude * 0.1
            else:  # Good colorful area
                alpha = 0.8 + amplitude * 0.1

            # Cache the result
            self._julia_cache = (colored_fractal, alpha)

        # Use cached Julia calculation
        colored_fractal, alpha = self._julia_cache
        frame[:] = cv2.addWeighted(frame, 1 - alpha, colored_fractal, alpha, 0)

        # Add pulsing center point
        center_screen_x = self.width // 2
        center_screen_y = self.height // 2
        pulse_radius = int(3 + amplitude * 8)
        pulse_color = (255, 255, 255)
        cv2.circle(
            frame, (center_screen_x, center_screen_y), pulse_radius, pulse_color, 1
        )

    def _calculate_julia_vectorized(self, C: np.ndarray, max_iter: int) -> np.ndarray:
        """Calculate Julia set using optimized vectorized operations."""
        # Julia set uses a fixed constant c and starts with Z = pixel coordinates
        # Using c = -0.7 + 0.27015i for a nice looking Julia set
        julia_c = -0.7 + 0.27015j

        Z = C.copy()  # Start with pixel coordinates
        iterations = np.zeros(C.shape, dtype=np.int32)

        # Very simplified Julia calculation for speed
        for i in range(max_iter):
            # Find points that haven't diverged yet
            mask = np.abs(Z) <= 2

            if not np.any(mask):
                break

            # Julia set iteration: Z = Z^2 + c
            Z[mask] = Z[mask] ** 2 + julia_c

            # Mark newly diverged points
            newly_diverged = (np.abs(Z) > 2) & (iterations == 0)
            iterations[newly_diverged] = i

        # Points that never diverged get max_iter
        iterations[iterations == 0] = max_iter

        return iterations

    def _get_current_gradient_colors(
        self, gradient_style: str = "default", custom_colors: list = None
    ) -> list:
        """Get the current gradient colors to use for Julia coloring."""
        # Define the same gradient presets as in create_fallback_background
        gradient_presets = {
            "default": [
                (30, 50, 120),
                (130, 130, 255),
            ],  # Deep blue to purple (original)
            "dark_teal_orange": [
                (0, 40, 40),
                (255, 140, 60),
            ],  # Dark teal to vibrant orange
            "sunset": [(255, 94, 77), (255, 154, 0), (255, 206, 84)],  # Sunset colors
            "ocean": [(0, 119, 190), (0, 180, 216), (144, 224, 239)],  # Ocean blues
            "purple_pink": [(106, 17, 203), (255, 61, 127)],  # Deep purple to pink
            "forest": [
                (34, 139, 34),
                (107, 142, 35),
                (255, 215, 0),
            ],  # Forest green to gold
            "midnight": [
                (25, 25, 112),
                (138, 43, 226),
                (75, 0, 130),
            ],  # Midnight blues and purples
            "fire": [
                (139, 0, 0),
                (255, 69, 0),
                (255, 215, 0),
            ],  # Dark red to orange to gold
            "arctic": [
                (176, 224, 230),
                (135, 206, 235),
                (70, 130, 180),
            ],  # Arctic blues
            "cosmic": [
                (75, 0, 130),
                (138, 43, 226),
                (255, 20, 147),
                (255, 215, 0),
            ],  # Deep space colors
            # 20 NUEVOS GRADIENTES HERMOSOS
            "cherry_blossom": [
                (255, 183, 197),
                (255, 105, 180),
                (255, 20, 147),
            ],  # Flor de cerezo
            "tropical": [
                (0, 255, 127),
                (255, 215, 0),
                (255, 69, 0),
            ],  # Tropical verde-dorado-naranja
            "lavender_mist": [
                (230, 230, 250),
                (147, 112, 219),
                (138, 43, 226),
            ],  # Niebla de lavanda
            "golden_hour": [
                (255, 223, 0),
                (255, 140, 0),
                (255, 69, 0),
                (139, 0, 0),
            ],  # Hora dorada
            "emerald_sea": [
                (0, 128, 128),
                (32, 178, 170),
                (72, 209, 204),
                (175, 238, 238),
            ],  # Mar esmeralda
            "rose_gold": [
                (183, 110, 121),
                (255, 192, 203),
                (255, 215, 0),
            ],  # Oro rosa
            "northern_lights": [
                (0, 255, 127),
                (0, 191, 255),
                (138, 43, 226),
                (255, 20, 147),
            ],  # Aurora boreal
            "desert_sand": [
                (218, 165, 32),
                (255, 215, 0),
                (255, 160, 122),
                (250, 128, 114),
            ],  # Arena del desierto
            "deep_ocean": [
                (0, 0, 139),
                (0, 100, 148),
                (0, 191, 255),
                (135, 206, 235),
            ],  # Océano profundo
            "neon_cyber": [
                (255, 0, 255),
                (0, 255, 255),
                (57, 255, 20),
                (255, 255, 0),
            ],  # Neón cyberpunk
            "autumn_leaves": [
                (255, 69, 0),
                (255, 140, 0),
                (255, 215, 0),
                (139, 69, 19),
            ],  # Hojas de otoño
            "moonlight": [
                (25, 25, 112),
                (72, 61, 139),
                (176, 196, 222),
                (245, 245, 245),
            ],  # Luz de luna
            "tropical_sunset": [
                (255, 94, 77),
                (255, 154, 0),
                (255, 215, 0),
                (255, 20, 147),
                (138, 43, 226),
            ],  # Atardecer tropical
            "winter_frost": [
                (176, 224, 230),
                (173, 216, 230),
                (135, 206, 235),
                (70, 130, 180),
                (25, 25, 112),
            ],  # Escarcha invernal
            "sakura_dream": [
                (255, 228, 225),
                (255, 182, 193),
                (255, 105, 180),
                (219, 112, 147),
            ],  # Sueño de sakura
            "volcanic": [
                (139, 0, 0),
                (178, 34, 34),
                (255, 69, 0),
                (255, 215, 0),
                (255, 255, 255),
            ],  # Volcánico
            "electric_blue": [
                (0, 0, 139),
                (0, 191, 255),
                (0, 255, 255),
                (255, 255, 255),
            ],  # Azul eléctrico
            "jungle_green": [
                (0, 100, 0),
                (34, 139, 34),
                (50, 205, 50),
                (144, 238, 144),
            ],  # Verde selva
            "royal_purple": [
                (75, 0, 130),
                (106, 17, 203),
                (138, 43, 226),
                (218, 112, 214),
            ],  # Púrpura real
            "cotton_candy": [
                (255, 192, 203),
                (255, 182, 193),
                (221, 160, 221),
                (238, 130, 238),
                (255, 20, 147),
            ],  # Algodón de azúcar
        }

        # Use custom colors if provided, otherwise use preset
        if custom_colors and len(custom_colors) >= 2:
            base_colors = custom_colors
        else:
            base_colors = gradient_presets.get(
                gradient_style, gradient_presets["default"]
            )

        # Extend the colors for more variety in the fractal
        extended_colors = []
        for i, color in enumerate(base_colors):
            extended_colors.append(color)
            # Add intermediate colors for smoother transitions
            if i < len(base_colors) - 1:
                next_color = base_colors[i + 1]
                mid_color = (
                    (color[0] + next_color[0]) // 2,
                    (color[1] + next_color[1]) // 2,
                    (color[2] + next_color[2]) // 2,
                )
                extended_colors.append(mid_color)

        # Add black for the set interior
        extended_colors.append((0, 0, 0))

        return extended_colors

    def _color_julia(
        self,
        iterations: np.ndarray,
        max_iter: int,
        gradient_colors: list,
        amplitude: float,
        current_time: float,
    ) -> np.ndarray:
        """Color the Julia set using gradient colors with audio responsiveness - VECTORIZED."""
        height, width = iterations.shape
        colored = np.zeros((height, width, 3), dtype=np.uint8)

        # Normalize iterations
        normalized_iter = iterations.astype(np.float32) / max_iter

        # Audio-reactive color cycling (reduced range)
        color_shift = (current_time * 30 + amplitude * 50) % 180  # Reduced to HSV range

        # Create masks for points in and out of the set
        in_set_mask = iterations >= max_iter
        out_set_mask = ~in_set_mask

        # Points in the set are black
        colored[in_set_mask] = [0, 0, 0]

        if np.any(out_set_mask):
            # Vectorized processing for points outside the set
            iter_ratios = normalized_iter[out_set_mask]

            # Simplified coloring for maximum speed - minimal processing
            audio_variations = amplitude * 0.1 * np.sin(iter_ratios * 4 + current_time)
            adjusted_ratios = np.clip(iter_ratios + audio_variations, 0, 1)

            # Direct color mapping without interpolation (much faster)
            num_colors = len(gradient_colors) - 1
            color_indices = (adjusted_ratios * (num_colors - 1)).astype(np.int32)
            color_indices = np.clip(color_indices, 0, num_colors - 1)

            # Direct color assignment (no interpolation for speed)
            interpolated_colors = np.array(
                [gradient_colors[i] for i in color_indices], dtype=np.uint8
            )

            # Minimal color shift (only when significant audio)
            if color_shift != 0 and amplitude > 0.3:
                shift_amount = int(color_shift / 60) % 3  # Simple RGB channel rotation
                if shift_amount == 1:
                    interpolated_colors = interpolated_colors[
                        :, [1, 2, 0]
                    ]  # R->G, G->B, B->R
                elif shift_amount == 2:
                    interpolated_colors = interpolated_colors[
                        :, [2, 0, 1]
                    ]  # R->B, G->R, B->G

            # Assign colors to output array (BGR format for OpenCV)
            colored[out_set_mask] = interpolated_colors[:, [2, 1, 0]]  # RGB to BGR

        return colored

    def _draw_psychedelic_circles(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
    ):
        """Draw psychedelic concentric circles that zoom and pulse with audio."""
        center_x = self.width // 2
        center_y = self.height // 2

        # Enhanced amplitude with temporal smoothing
        enhanced_amplitude = amplitude * (1 + 0.7 * np.sin(current_time * 6))

        # Color palette based on audio frequency content
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]

        # Create dynamic color scheme
        hue_shift = (spectral_value / 4000) * 360 + current_time * 50
        base_hue = int(hue_shift) % 360

        # Zoom effect - creates the psychedelic infinite zoom
        zoom_speed = 2.0 + amplitude * 3.0  # Speed increases with audio
        zoom_offset = (current_time * zoom_speed * 50) % 100  # Reset every 100 pixels

        # Maximum radius to cover the entire screen
        max_radius = int(math.sqrt(self.width**2 + self.height**2)) + 100

        # Draw concentric circles with varying properties
        for i in range(0, max_radius, 8):  # Every 8 pixels for performance
            # Calculate effective radius with zoom effect
            effective_radius = (i + zoom_offset) % max_radius

            # Skip if too small
            if effective_radius < 5:
                continue

            # Audio-reactive radius modulation
            radius_variation = (
                enhanced_amplitude * 20 * math.sin(i * 0.05 + current_time * 4)
            )
            final_radius = int(effective_radius + radius_variation)

            if final_radius <= 0:
                continue

            # Dynamic color based on radius, time, and audio
            color_phase = (i * 0.02 + current_time * 3) % (2 * math.pi)
            color_intensity = int(
                128 + 127 * enhanced_amplitude * math.sin(color_phase)
            )

            # Multi-layered color scheme
            primary_hue = (base_hue + i * 2) % 360
            secondary_hue = (base_hue + i * 4 + 120) % 360

            # Alternate between different color schemes
            if i % 16 < 8:
                color = self._hsv_to_bgr(primary_hue, 200, min(255, color_intensity))
            else:
                color = self._hsv_to_bgr(
                    secondary_hue, 150, min(255, color_intensity - 30)
                )

            # Variable thickness based on audio and position
            thickness = max(1, int(2 + enhanced_amplitude * 4 * math.sin(i * 0.08)))

            # Draw the circle
            cv2.circle(frame, (center_x, center_y), final_radius, color, thickness)

        # Add central pulsing elements
        self._draw_psychedelic_center(
            frame, center_x, center_y, enhanced_amplitude, current_time, base_hue
        )

        # Add orbital elements
        self._draw_psychedelic_orbitals(
            frame, center_x, center_y, enhanced_amplitude, current_time, base_hue
        )

    def _draw_psychedelic_center(
        self, frame, center_x, center_y, amplitude, time, base_hue
    ):
        """Draw the central pulsing element of the psychedelic circles."""
        # Central pulsing circle
        pulse_radius = int(20 + amplitude * 40 * (1 + 0.5 * math.sin(time * 8)))
        center_color = self._hsv_to_bgr((base_hue + time * 100) % 360, 255, 255)
        cv2.circle(frame, (center_x, center_y), pulse_radius, center_color, -1)

        # Outer ring
        ring_radius = int(pulse_radius + 10 + amplitude * 20)
        ring_color = self._hsv_to_bgr((base_hue + 180) % 360, 200, 200)
        cv2.circle(frame, (center_x, center_y), ring_radius, ring_color, 3)

        # Inner sparkle
        for i in range(8):
            angle = (i * math.pi / 4) + time * 2
            spark_x = int(center_x + (pulse_radius * 0.6) * math.cos(angle))
            spark_y = int(center_y + (pulse_radius * 0.6) * math.sin(angle))
            spark_color = self._hsv_to_bgr((base_hue + i * 45) % 360, 255, 255)
            cv2.circle(frame, (spark_x, spark_y), 3, spark_color, -1)

    def _draw_psychedelic_orbitals(
        self, frame, center_x, center_y, amplitude, time, base_hue
    ):
        """Draw orbital elements around the psychedelic circles."""
        # Multiple orbital rings with different speeds and sizes
        orbital_configs = [
            (100, 2.0, 8, 0),  # radius, speed, count, phase_offset
            (150, -1.5, 6, math.pi / 3),
            (200, 1.0, 12, math.pi / 2),
            (250, -0.8, 4, math.pi),
        ]

        for orbit_radius, speed, count, phase_offset in orbital_configs:
            # Audio-reactive orbital radius
            dynamic_radius = orbit_radius * (1 + amplitude * 0.3)

            for i in range(count):
                angle = (i * 2 * math.pi / count) + (time * speed) + phase_offset

                # Calculate orbital position
                orb_x = int(center_x + dynamic_radius * math.cos(angle))
                orb_y = int(center_y + dynamic_radius * math.sin(angle))

                # Check bounds
                if 0 <= orb_x < self.width and 0 <= orb_y < self.height:
                    # Dynamic orbital size and color
                    orb_size = int(3 + amplitude * 8 + 3 * math.sin(time * 3 + i))
                    orb_color = self._hsv_to_bgr(
                        (base_hue + i * 30 + time * 60) % 360,
                        180,
                        int(200 + 55 * amplitude),
                    )

                    cv2.circle(frame, (orb_x, orb_y), orb_size, orb_color, -1)

                    # Add trailing effect
                    trail_angle = angle - 0.2
                    trail_x = int(
                        center_x + dynamic_radius * 0.9 * math.cos(trail_angle)
                    )
                    trail_y = int(
                        center_y + dynamic_radius * 0.9 * math.sin(trail_angle)
                    )

                    if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                        trail_color = self._hsv_to_bgr(
                            (base_hue + i * 30 + time * 60) % 360,
                            120,
                            int(100 + 50 * amplitude),
                        )
                        cv2.circle(
                            frame, (trail_x, trail_y), orb_size // 2, trail_color, -1
                        )

    def _draw_fluid_waves(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw smooth fluid waves that flow across the screen - very satisfying to watch."""
        center_x = self.width // 2
        center_y = self.height // 2

        # Enhanced amplitude with smooth transitions
        enhanced_amplitude = amplitude * (1 + 0.8 * np.sin(current_time * 3))

        # Color palette
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        hue_shift = (spectral_value / 4000) * 360 + current_time * 20
        base_hue = int(hue_shift) % 360

        # Create multiple fluid layers flowing in different directions
        num_layers = 4
        for layer in range(num_layers):
            layer_offset = layer * (2 * math.pi / num_layers)
            layer_speed = 0.5 + layer * 0.3
            layer_amplitude = enhanced_amplitude * (0.8 - layer * 0.15)

            # Calculate wave parameters for this layer
            wavelength = 80 + layer * 20
            wave_height = 40 + layer_amplitude * 60

            # Generate smooth wave points
            points = []
            for x in range(
                -50, self.width + 50, 6
            ):  # Extend beyond screen for smooth edges
                # Multiple sine waves for complexity
                y_wave1 = wave_height * math.sin(
                    (x / wavelength) * 2 * math.pi
                    + current_time * layer_speed
                    + layer_offset
                )
                y_wave2 = (
                    wave_height
                    * 0.3
                    * math.sin(
                        (x / (wavelength * 0.7)) * 2 * math.pi
                        + current_time * layer_speed * 1.3
                    )
                )

                y_final = center_y + y_wave1 + y_wave2 + (layer - num_layers / 2) * 80

                if (
                    -50 <= y_final <= self.height + 50
                ):  # Only add points within extended bounds
                    points.append((x, int(y_final)))

            # Draw flowing waves with gradient colors
            if len(points) > 1:
                # Create color variation across the wave
                layer_hue = (base_hue + layer * 45) % 360

                for i in range(len(points) - 1):
                    # Color varies along the wave
                    color_variation = int(50 * math.sin(i * 0.1 + current_time * 2))
                    wave_color = self._hsv_to_bgr(
                        layer_hue,
                        150 + color_variation,
                        int(180 + 75 * layer_amplitude),
                    )

                    # Variable thickness for depth
                    thickness = max(2, int(8 - layer * 1.5 + layer_amplitude * 3))

                    if (
                        0 <= points[i][0] < self.width
                        and 0 <= points[i][1] < self.height
                        and 0 <= points[i + 1][0] < self.width
                        and 0 <= points[i + 1][1] < self.height
                    ):
                        cv2.line(frame, points[i], points[i + 1], wave_color, thickness)

        # Add floating bubbles for extra satisfaction
        self._draw_floating_bubbles(
            frame,
            enhanced_amplitude,
            current_time,
            base_hue,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )

    def _draw_floating_bubbles(
        self,
        frame,
        amplitude,
        time,
        base_hue,
        gradient_style="default",
        custom_colors=None,
        particle_color_scheme="multicolor",
        particle_gradient_style=None,
        particle_custom_colors=None,
    ):
        """Draw floating bubbles that add to the fluid effect."""
        bubble_count = int(8 + amplitude * 12)

        for i in range(bubble_count):
            # Bubble position based on time and index for consistent movement
            phase = (time * 0.3 + i * 0.8) % (2 * math.pi)

            # Smooth floating motion
            bubble_x = int(
                self.width * 0.1 + (self.width * 0.8) * ((i + time * 0.1) % 1.0)
            )
            bubble_y = int(
                self.height * 0.2 + (self.height * 0.6) * (0.5 + 0.3 * math.sin(phase))
            )

            # Bubble size varies with audio and time
            bubble_size = int(8 + amplitude * 15 + 5 * math.sin(time * 2 + i))

            # Bubble color using new scheme
            bubble_color = self._get_particle_color(
                i,
                base_hue,
                amplitude,
                time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )

            # Draw bubble with outline
            if 0 <= bubble_x < self.width and 0 <= bubble_y < self.height:
                cv2.circle(frame, (bubble_x, bubble_y), bubble_size, bubble_color, -1)
                cv2.circle(
                    frame, (bubble_x, bubble_y), bubble_size + 1, (255, 255, 255), 1
                )

    def _draw_particle_fall(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw particles falling like sand or snow - mesmerizing to watch."""
        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 0.6 * np.sin(current_time * 4))

        # Color palette
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 15) % 360

        # Number of particles based on audio
        particle_count = int(150 + enhanced_amplitude * 200)

        for i in range(particle_count):
            # Each particle has its own lifecycle
            particle_phase = (
                current_time * (0.8 + i * 0.002) + i * 2.1
            ) % 8  # 8 second cycle

            # Particle start position (top of screen)
            start_x = int(i * 7.3) % self.width  # Pseudo-random but consistent

            # Particle falls with slight horizontal drift
            drift = 30 * math.sin(i * 0.1 + current_time * 0.5)
            particle_x = int(start_x + drift)

            # Particle y position based on fall time
            fall_speed = 50 + enhanced_amplitude * 100 + (i % 5) * 10
            particle_y = int(-20 + particle_phase * fall_speed)

            # Only draw if particle is on screen
            if 0 <= particle_x < self.width and 0 <= particle_y < self.height:
                # Particle size varies
                particle_size = max(
                    1, int(2 + enhanced_amplitude * 4 + 2 * math.sin(i * 0.3))
                )

                # Particle color varies with position and audio
                particle_color = self._get_particle_color(
                    i,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )

                cv2.circle(
                    frame, (particle_x, particle_y), particle_size, particle_color, -1
                )

                # Add glow effect for some particles
                if i % 5 == 0:  # Every 5th particle gets glow
                    glow_color = self._get_particle_color(
                        i + 1000,
                        base_hue,
                        enhanced_amplitude * 0.5,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )
                    cv2.circle(
                        frame,
                        (particle_x, particle_y),
                        particle_size + 2,
                        glow_color,
                        1,
                    )

        # Add particle accumulation at bottom
        self._draw_particle_accumulation(
            frame, enhanced_amplitude, current_time, base_hue
        )

    def _draw_particle_accumulation(self, frame, amplitude, time, base_hue):
        """Draw accumulated particles at the bottom of the screen."""
        accumulation_height = int(20 + amplitude * 40)

        # Create wavy accumulation line
        points = []
        for x in range(0, self.width, 4):
            wave_offset = 10 * amplitude * math.sin(x * 0.02 + time * 2)
            y = self.height - accumulation_height + int(wave_offset)
            points.append((x, y))

        # Fill the accumulation area
        if len(points) > 2:
            # Create polygon points for filled area
            polygon_points = points + [(self.width, self.height), (0, self.height)]
            polygon_points = np.array(polygon_points, np.int32)

            # Gradient fill
            accumulation_color = self._hsv_to_bgr(
                base_hue, 120, int(100 + 80 * amplitude)
            )
            cv2.fillPoly(frame, [polygon_points], accumulation_color)

            # Add texture to accumulation
            for i in range(0, len(points) - 1, 2):
                texture_color = self._hsv_to_bgr(
                    (base_hue + i * 2) % 360, 100, int(150 + 50 * amplitude)
                )
                cv2.line(frame, points[i], points[i + 1], texture_color, 2)

    def _draw_morphing_shapes(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
    ):
        """Draw geometric shapes that smoothly morph into each other."""
        center_x = self.width // 2
        center_y = self.height // 2

        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 0.7 * np.sin(current_time * 5))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 25) % 360

        # Shape morphing cycle (triangle -> square -> pentagon -> hexagon -> circle)
        cycle_duration = 6.0  # 6 seconds per complete cycle
        cycle_phase = (current_time % cycle_duration) / cycle_duration

        # Determine current shape transition
        shape_transitions = [
            (3, 4),  # triangle to square
            (4, 5),  # square to pentagon
            (5, 6),  # pentagon to hexagon
            (6, 8),  # hexagon to octagon
            (8, 32),  # octagon to circle (32-sided polygon)
        ]

        transition_idx = int(cycle_phase * len(shape_transitions))
        transition_idx = min(transition_idx, len(shape_transitions) - 1)
        local_phase = (cycle_phase * len(shape_transitions)) % 1.0

        start_sides, end_sides = shape_transitions[transition_idx]

        # Interpolate number of sides and create morphing shape
        num_points = 64  # High resolution for smooth morphing
        morph_radius = 80 + enhanced_amplitude * 120

        # Create two shapes and interpolate between them
        shape1_points = []
        shape2_points = []

        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi

            # First shape (start_sides)
            shape1_angle = (i / num_points) * start_sides * 2 * math.pi / start_sides
            shape1_radius = morph_radius * (
                1 + 0.1 * math.sin(angle * start_sides + current_time * 2)
            )
            shape1_x = center_x + shape1_radius * math.cos(shape1_angle)
            shape1_y = center_y + shape1_radius * math.sin(shape1_angle)
            shape1_points.append((shape1_x, shape1_y))

            # Second shape (end_sides)
            shape2_angle = (i / num_points) * end_sides * 2 * math.pi / end_sides
            shape2_radius = morph_radius * (
                1 + 0.1 * math.sin(angle * end_sides + current_time * 2)
            )
            shape2_x = center_x + shape2_radius * math.cos(shape2_angle)
            shape2_y = center_y + shape2_radius * math.sin(shape2_angle)
            shape2_points.append((shape2_x, shape2_y))

        # Interpolate between shapes for smooth morphing
        morphed_points = []
        for i in range(num_points):
            interp_x = (
                shape1_points[i][0]
                + (shape2_points[i][0] - shape1_points[i][0]) * local_phase
            )
            interp_y = (
                shape1_points[i][1]
                + (shape2_points[i][1] - shape1_points[i][1]) * local_phase
            )
            morphed_points.append((int(interp_x), int(interp_y)))

        # Draw the morphing shape with gradient colors
        for i in range(len(morphed_points)):
            next_i = (i + 1) % len(morphed_points)

            # Color varies around the shape
            point_hue = (base_hue + i * 360 // len(morphed_points)) % 360
            point_color = self._hsv_to_bgr(
                point_hue, 200, int(150 + 105 * enhanced_amplitude)
            )

            cv2.line(frame, morphed_points[i], morphed_points[next_i], point_color, 4)

        # Fill the shape with translucent color
        fill_color = self._hsv_to_bgr(base_hue, 80, int(60 + 40 * enhanced_amplitude))
        cv2.fillPoly(frame, [np.array(morphed_points, np.int32)], fill_color)

        # Add smaller morphing shapes around the main one
        for orbit in range(3):
            orbit_radius = 200 + orbit * 80
            orbit_angle = current_time * (0.5 + orbit * 0.3) + orbit * (2 * math.pi / 3)

            small_center_x = int(center_x + orbit_radius * math.cos(orbit_angle))
            small_center_y = int(center_y + orbit_radius * math.sin(orbit_angle))

            if 0 <= small_center_x < self.width and 0 <= small_center_y < self.height:
                small_radius = 30 + enhanced_amplitude * 40
                small_sides = 3 + orbit

                # Create small morphing shape
                small_points = []
                for i in range(small_sides * 4):  # More points for smoothness
                    angle = (i / (small_sides * 4)) * 2 * math.pi
                    px = int(small_center_x + small_radius * math.cos(angle))
                    py = int(small_center_y + small_radius * math.sin(angle))
                    small_points.append((px, py))

                # Draw small shape
                small_color = self._hsv_to_bgr(
                    (base_hue + orbit * 60) % 360,
                    150,
                    int(120 + 60 * enhanced_amplitude),
                )
                for i in range(len(small_points)):
                    next_i = (i + 1) % len(small_points)
                    if (
                        0 <= small_points[i][0] < self.width
                        and 0 <= small_points[i][1] < self.height
                        and 0 <= small_points[next_i][0] < self.width
                        and 0 <= small_points[next_i][1] < self.height
                    ):
                        cv2.line(
                            frame, small_points[i], small_points[next_i], small_color, 2
                        )

    def _draw_kaleidoscope(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw kaleidoscope patterns with symmetrical reflections - very mesmerizing."""
        center_x = self.width // 2
        center_y = self.height // 2

        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 0.9 * np.sin(current_time * 6))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 35) % 360

        # Kaleidoscope has multiple symmetrical segments
        num_segments = 8  # 8-fold symmetry
        segment_angle = 2 * math.pi / num_segments

        # Create base pattern in one segment, then mirror it
        max_radius = min(self.width, self.height) // 2

        # Generate organic flowing patterns
        pattern_elements = []

        # Multiple flowing lines that create the kaleidoscope pattern
        for line_idx in range(6):
            line_phase = (current_time * (0.3 + line_idx * 0.1)) % (2 * math.pi)
            line_amplitude = enhanced_amplitude * (0.5 + line_idx * 0.1)

            # Create curved line points
            line_points = []
            for t in np.linspace(0, 1, 30):
                # Curved path parameters
                base_radius = max_radius * 0.2 + t * max_radius * 0.6
                curve_offset = (
                    line_amplitude * 50 * math.sin(t * 4 * math.pi + line_phase)
                )

                # Position in first segment
                angle_in_segment = (
                    t * 0.3 + line_idx * 0.1
                ) * segment_angle + curve_offset * 0.01

                px = center_x + (base_radius + curve_offset) * math.cos(
                    angle_in_segment
                )
                py = center_y + (base_radius + curve_offset) * math.sin(
                    angle_in_segment
                )
                line_points.append((int(px), int(py)))

            pattern_elements.append(line_points)

        # Draw the pattern in all segments with symmetry
        for segment in range(num_segments):
            segment_rotation = segment * segment_angle

            for line_points in pattern_elements:
                if len(line_points) > 1:
                    # Color for this segment and line using particle color scheme
                    line_color = self._get_particle_color(
                        segment * 1000 + len(line_points),
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    # Draw the line in this segment
                    rotated_points = []
                    for px, py in line_points:
                        # Rotate point around center
                        rel_x = px - center_x
                        rel_y = py - center_y

                        rot_x = rel_x * math.cos(segment_rotation) - rel_y * math.sin(
                            segment_rotation
                        )
                        rot_y = rel_x * math.sin(segment_rotation) + rel_y * math.cos(
                            segment_rotation
                        )

                        final_x = int(center_x + rot_x)
                        final_y = int(center_y + rot_y)

                        if 0 <= final_x < self.width and 0 <= final_y < self.height:
                            rotated_points.append((final_x, final_y))

                    # Draw the rotated line
                    for i in range(len(rotated_points) - 1):
                        cv2.line(
                            frame,
                            rotated_points[i],
                            rotated_points[i + 1],
                            line_color,
                            3,
                        )

                    # Also draw mirrored version for extra symmetry
                    mirrored_points = []
                    for px, py in line_points:
                        # Mirror across the segment line and then rotate
                        rel_x = px - center_x
                        rel_y = -(py - center_y)  # Mirror across horizontal

                        rot_x = rel_x * math.cos(segment_rotation) - rel_y * math.sin(
                            segment_rotation
                        )
                        rot_y = rel_x * math.sin(segment_rotation) + rel_y * math.cos(
                            segment_rotation
                        )

                        final_x = int(center_x + rot_x)
                        final_y = int(center_y + rot_y)

                        if 0 <= final_x < self.width and 0 <= final_y < self.height:
                            mirrored_points.append((final_x, final_y))

                    # Draw mirrored line with slightly different color
                    mirror_color = self._get_particle_color(
                        segment * 1000 + len(line_points) + 500,
                        base_hue,
                        enhanced_amplitude * 0.7,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )
                    for i in range(len(mirrored_points) - 1):
                        cv2.line(
                            frame,
                            mirrored_points[i],
                            mirrored_points[i + 1],
                            mirror_color,
                            2,
                        )

        # Add central mandala-like pattern
        self._draw_kaleidoscope_center(
            frame,
            center_x,
            center_y,
            enhanced_amplitude,
            current_time,
            base_hue,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )

    def _draw_kaleidoscope_center(
        self,
        frame,
        center_x,
        center_y,
        amplitude,
        time,
        base_hue,
        gradient_style="default",
        custom_colors=None,
        particle_color_scheme="multicolor",
        particle_gradient_style=None,
        particle_custom_colors=None,
    ):
        """Draw the central mandala pattern for the kaleidoscope."""
        # Central rotating elements
        num_elements = 12
        for i in range(num_elements):
            angle = (i * 2 * math.pi / num_elements) + time * 2

            # Multiple concentric elements
            for radius_mult in [0.3, 0.5, 0.7]:
                element_radius = int(30 + amplitude * 60) * radius_mult

                element_x = int(center_x + element_radius * math.cos(angle))
                element_y = int(center_y + element_radius * math.sin(angle))

                if 0 <= element_x < self.width and 0 <= element_y < self.height:
                    element_size = max(2, int(4 + amplitude * 8 * radius_mult))
                    element_color = self._get_particle_color(
                        i + int(radius_mult * 1000),
                        base_hue,
                        amplitude,
                        time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    cv2.circle(
                        frame, (element_x, element_y), element_size, element_color, -1
                    )
                    cv2.circle(
                        frame,
                        (element_x, element_y),
                        element_size + 1,
                        (255, 255, 255),
                        1,
                    )

    def _draw_breathing_patterns(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw breathing patterns that expand and contract smoothly - very zen and satisfying."""
        center_x = self.width // 2
        center_y = self.height // 2

        # Enhanced amplitude with breathing rhythm
        breathing_cycle = 4.0  # 4 second breathing cycle
        breathing_phase = (current_time % breathing_cycle) / breathing_cycle
        breathing_amplitude = 0.5 + 0.5 * math.sin(breathing_phase * 2 * math.pi)

        enhanced_amplitude = amplitude * (0.5 + 0.5 * breathing_amplitude)

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 10) % 360

        # Multiple concentric breathing rings
        num_rings = 8
        max_radius = min(self.width, self.height) // 2 - 50

        for ring in range(num_rings):
            ring_phase = breathing_phase + (ring * 0.1)  # Staggered breathing
            ring_breathing = 0.5 + 0.5 * math.sin(ring_phase * 2 * math.pi)

            # Base radius changes with breathing
            base_radius = (ring + 1) * (max_radius / num_rings)
            ring_radius = int(
                base_radius
                * (0.4 + 0.6 * ring_breathing)
                * (1 + enhanced_amplitude * 0.3)
            )

            # Ring thickness breathes too
            ring_thickness = max(
                1, int(3 + 5 * ring_breathing + enhanced_amplitude * 4)
            )

            # Color shifts with breathing and ring position
            ring_hue = (base_hue + ring * 25 + breathing_phase * 60) % 360
            ring_saturation = int(100 + 100 * ring_breathing)
            ring_brightness = int(80 + 120 * ring_breathing + enhanced_amplitude * 55)

            ring_color = self._hsv_to_bgr(ring_hue, ring_saturation, ring_brightness)

            # Draw main breathing ring
            cv2.circle(
                frame, (center_x, center_y), ring_radius, ring_color, ring_thickness
            )

            # Add subtle inner glow
            if ring_breathing > 0.7:  # Only when expanded
                glow_color = self._hsv_to_bgr(
                    ring_hue, 50, int(50 + 50 * ring_breathing)
                )
                cv2.circle(
                    frame,
                    (center_x, center_y),
                    ring_radius - ring_thickness,
                    glow_color,
                    1,
                )

        # Add breathing particles around the rings
        self._draw_breathing_particles(
            frame,
            center_x,
            center_y,
            enhanced_amplitude,
            breathing_amplitude,
            current_time,
            base_hue,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )

        # Central breathing mandala
        self._draw_breathing_center(
            frame,
            center_x,
            center_y,
            enhanced_amplitude,
            breathing_amplitude,
            current_time,
            base_hue,
        )

    def _draw_breathing_particles(
        self,
        frame,
        center_x,
        center_y,
        amplitude,
        breathing_amplitude,
        time,
        base_hue,
        gradient_style="default",
        custom_colors=None,
        particle_color_scheme="multicolor",
        particle_gradient_style=None,
        particle_custom_colors=None,
    ):
        """Draw particles that float with the breathing rhythm."""
        particle_count = int(20 + amplitude * 30)

        for i in range(particle_count):
            # Particle orbits with breathing motion
            particle_angle = (i * 2.4 + time * 0.5) % (2 * math.pi)
            base_orbit_radius = 150 + i * 8

            # Breathing affects orbit radius
            orbit_radius = base_orbit_radius * (0.7 + 0.3 * breathing_amplitude)

            particle_x = int(center_x + orbit_radius * math.cos(particle_angle))
            particle_y = int(center_y + orbit_radius * math.sin(particle_angle))

            if 0 <= particle_x < self.width and 0 <= particle_y < self.height:
                # Particle size breathes
                particle_size = max(1, int(3 + 7 * breathing_amplitude + amplitude * 5))

                # Particle color using new scheme
                particle_color = self._get_particle_color(
                    i,
                    base_hue,
                    amplitude * breathing_amplitude,
                    time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )

                cv2.circle(
                    frame, (particle_x, particle_y), particle_size, particle_color, -1
                )

                # Add breathing glow
                if breathing_amplitude > 0.6:
                    glow_size = particle_size + 2
                    glow_color = self._get_particle_color(
                        i + 1000,
                        base_hue,
                        amplitude * breathing_amplitude * 0.5,
                        time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )
                    cv2.circle(
                        frame, (particle_x, particle_y), glow_size, glow_color, 1
                    )

    def _draw_breathing_center(
        self, frame, center_x, center_y, amplitude, breathing_amplitude, time, base_hue
    ):
        """Draw the central breathing mandala."""
        # Central pulsing flower pattern
        num_petals = 8

        for petal in range(num_petals):
            petal_angle = (petal * 2 * math.pi / num_petals) + time * 0.5

            # Petal length breathes
            petal_length = int(20 + 40 * breathing_amplitude + amplitude * 30)

            # Petal end position
            petal_end_x = int(center_x + petal_length * math.cos(petal_angle))
            petal_end_y = int(center_y + petal_length * math.sin(petal_angle))

            # Petal color
            petal_hue = (base_hue + petal * 45) % 360
            petal_color = self._hsv_to_bgr(
                petal_hue, 200, int(120 + 135 * breathing_amplitude)
            )

            # Draw petal as line with breathing thickness
            petal_thickness = max(2, int(3 + 6 * breathing_amplitude))
            cv2.line(
                frame,
                (center_x, center_y),
                (petal_end_x, petal_end_y),
                petal_color,
                petal_thickness,
            )

            # Add petal tip
            if 0 <= petal_end_x < self.width and 0 <= petal_end_y < self.height:
                tip_size = max(2, int(4 + 6 * breathing_amplitude))
                cv2.circle(frame, (petal_end_x, petal_end_y), tip_size, petal_color, -1)

        # Central breathing core
        core_radius = int(8 + 12 * breathing_amplitude + amplitude * 10)
        core_color = self._hsv_to_bgr(
            base_hue, 255, int(200 + 55 * breathing_amplitude)
        )
        cv2.circle(frame, (center_x, center_y), core_radius, core_color, -1)

        # Core outline that pulses
        outline_color = (
            (255, 255, 255)
            if breathing_amplitude > 0.8
            else self._hsv_to_bgr((base_hue + 180) % 360, 100, 200)
        )
        cv2.circle(frame, (center_x, center_y), core_radius + 1, outline_color, 2)

    def _draw_k_mandala(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw geometric mandala patterns with intricate symmetry."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 0.8 * np.sin(current_time * 4))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 25) % 360

        # 12-fold symmetry for traditional mandala
        num_segments = 12
        segment_angle = 2 * math.pi / num_segments

        # Multiple concentric rings
        for ring in range(5):
            ring_radius = 50 + ring * (40 + enhanced_amplitude * 20)

            # Create geometric patterns in each ring
            for segment in range(num_segments):
                segment_rotation = segment * segment_angle + current_time * 0.5

                # Create intricate geometric elements
                for element in range(8):
                    element_angle = element * math.pi / 4
                    element_distance = ring_radius + element * 8

                    # Calculate positions with rotation
                    rel_x = element_distance * math.cos(element_angle)
                    rel_y = element_distance * math.sin(element_angle)

                    # Rotate around segment
                    rot_x = rel_x * math.cos(segment_rotation) - rel_y * math.sin(
                        segment_rotation
                    )
                    rot_y = rel_x * math.sin(segment_rotation) + rel_y * math.cos(
                        segment_rotation
                    )

                    final_x = int(center_x + rot_x)
                    final_y = int(center_y + rot_y)

                    if 0 <= final_x < self.width and 0 <= final_y < self.height:
                        # Element color using particle scheme
                        element_color = self._get_particle_color(
                            segment * 1000 + ring * 100 + element,
                            base_hue,
                            enhanced_amplitude,
                            current_time,
                            gradient_style,
                            custom_colors,
                            particle_color_scheme,
                            particle_gradient_style,
                            particle_custom_colors,
                        )

                        # Draw geometric element
                        element_size = max(2, int(3 + enhanced_amplitude * 6))
                        cv2.circle(
                            frame, (final_x, final_y), element_size, element_color, -1
                        )

                        # Connect to center with sacred lines
                        if ring == 0:  # Only innermost ring connects to center
                            cv2.line(
                                frame,
                                (center_x, center_y),
                                (final_x, final_y),
                                element_color,
                                1,
                            )

        # Central sacred symbol
        central_radius = int(15 + enhanced_amplitude * 25)
        central_color = self._get_particle_color(
            9999,
            base_hue,
            enhanced_amplitude,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        cv2.circle(frame, (center_x, center_y), central_radius, central_color, -1)
        cv2.circle(frame, (center_x, center_y), central_radius + 2, (255, 255, 255), 2)

    def _draw_k_crystal(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw crystalline fractal patterns with sharp angular symmetry."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 0.9 * np.sin(current_time * 5))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 20) % 360

        # 6-fold symmetry like crystals
        num_segments = 6
        segment_angle = 2 * math.pi / num_segments

        # Draw crystal facets
        for segment in range(num_segments):
            segment_rotation = segment * segment_angle + current_time * 0.3

            # Create crystal structure with angular lines
            for layer in range(4):
                layer_distance = 60 + layer * (30 + enhanced_amplitude * 20)

                # Create angular crystal lines
                crystal_points = []
                for point in range(5):
                    point_angle = point * math.pi / 8
                    point_distance = layer_distance + point * 10

                    rel_x = point_distance * math.cos(point_angle)
                    rel_y = point_distance * math.sin(point_angle)

                    # Rotate
                    rot_x = rel_x * math.cos(segment_rotation) - rel_y * math.sin(
                        segment_rotation
                    )
                    rot_y = rel_x * math.sin(segment_rotation) + rel_y * math.cos(
                        segment_rotation
                    )

                    final_x = int(center_x + rot_x)
                    final_y = int(center_y + rot_y)

                    if 0 <= final_x < self.width and 0 <= final_y < self.height:
                        crystal_points.append((final_x, final_y))

                # Draw crystal structure
                if len(crystal_points) > 1:
                    crystal_color = self._get_particle_color(
                        segment * 1000 + layer * 100,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    # Draw angular crystal facets
                    for i in range(len(crystal_points) - 1):
                        cv2.line(
                            frame,
                            crystal_points[i],
                            crystal_points[i + 1],
                            crystal_color,
                            2,
                        )

                    # Mirror lines for crystalline symmetry
                    for i in range(len(crystal_points)):
                        mirror_x = 2 * center_x - crystal_points[i][0]
                        mirror_y = crystal_points[i][1]
                        if 0 <= mirror_x < self.width and 0 <= mirror_y < self.height:
                            cv2.line(
                                frame,
                                crystal_points[i],
                                (mirror_x, mirror_y),
                                crystal_color,
                                1,
                            )

        # Central crystal core
        core_size = int(10 + enhanced_amplitude * 20)
        core_color = self._get_particle_color(
            8888,
            base_hue,
            enhanced_amplitude,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        # Draw hexagonal core
        hex_points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = int(center_x + core_size * math.cos(angle))
            y = int(center_y + core_size * math.sin(angle))
            hex_points.append((x, y))
        cv2.fillPoly(frame, [np.array(hex_points, np.int32)], core_color)

    def _draw_k_flower(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw flowing flower patterns with organic petal symmetry."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 0.7 * np.sin(current_time * 3))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 15) % 360

        # 8-fold flower symmetry
        num_petals = 8
        petal_angle = 2 * math.pi / num_petals

        # Multiple flower layers
        for layer in range(3):
            layer_size = 1.0 - layer * 0.3
            layer_rotation = current_time * (0.5 + layer * 0.2)

            for petal in range(num_petals):
                petal_rotation = petal * petal_angle + layer_rotation

                # Create organic petal shape with curves
                petal_points = []
                for t in np.linspace(0, 1, 20):
                    # Petal shape using sine curves for organic feel
                    petal_radius = (80 + enhanced_amplitude * 60) * layer_size
                    petal_width = 30 * layer_size

                    # Create petal curve
                    curve_x = petal_radius * t
                    curve_y = (
                        petal_width
                        * math.sin(t * math.pi)
                        * (1 + 0.3 * math.sin(t * 4 * math.pi + current_time * 2))
                    )

                    # Rotate petal
                    rot_x = curve_x * math.cos(petal_rotation) - curve_y * math.sin(
                        petal_rotation
                    )
                    rot_y = curve_x * math.sin(petal_rotation) + curve_y * math.cos(
                        petal_rotation
                    )

                    final_x = int(center_x + rot_x)
                    final_y = int(center_y + rot_y)

                    if 0 <= final_x < self.width and 0 <= final_y < self.height:
                        petal_points.append((final_x, final_y))

                # Draw petal
                if len(petal_points) > 1:
                    petal_color = self._get_particle_color(
                        petal * 100 + layer * 10,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    # Draw smooth petal lines
                    for i in range(len(petal_points) - 1):
                        thickness = max(1, int(3 * layer_size + enhanced_amplitude * 2))
                        cv2.line(
                            frame,
                            petal_points[i],
                            petal_points[i + 1],
                            petal_color,
                            thickness,
                        )

                    # Draw petal center line
                    center_points = []
                    for t in np.linspace(0, 1, 10):
                        curve_x = (petal_radius * t) * 0.7
                        rot_x = curve_x * math.cos(petal_rotation)
                        rot_y = curve_x * math.sin(petal_rotation)
                        final_x = int(center_x + rot_x)
                        final_y = int(center_y + rot_y)
                        if 0 <= final_x < self.width and 0 <= final_y < self.height:
                            center_points.append((final_x, final_y))

                    for i in range(len(center_points) - 1):
                        cv2.line(
                            frame,
                            center_points[i],
                            center_points[i + 1],
                            petal_color,
                            1,
                        )

        # Flower center with stamens
        center_radius = int(15 + enhanced_amplitude * 20)
        center_color = self._get_particle_color(
            7777,
            base_hue,
            enhanced_amplitude,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        cv2.circle(frame, (center_x, center_y), center_radius, center_color, -1)

        # Stamens
        for stamen in range(12):
            stamen_angle = stamen * math.pi / 6 + current_time * 3
            stamen_x = int(center_x + (center_radius - 5) * math.cos(stamen_angle))
            stamen_y = int(center_y + (center_radius - 5) * math.sin(stamen_angle))
            stamen_color = self._get_particle_color(
                7777 + stamen,
                base_hue,
                enhanced_amplitude,
                current_time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
            cv2.circle(frame, (stamen_x, stamen_y), 2, stamen_color, -1)

    def _draw_k_sacred(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw sacred geometry patterns: flower of life, merkaba, etc."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 0.6 * np.sin(current_time * 2))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 10) % 360

        # Sacred geometry: Flower of Life pattern
        sacred_radius = 40 + enhanced_amplitude * 30

        # 6-fold symmetry
        for ring in range(3):
            ring_distance = ring * sacred_radius * 1.2

            if ring == 0:
                # Central circle
                circle_color = self._get_particle_color(
                    0,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )
                cv2.circle(
                    frame, (center_x, center_y), int(sacred_radius), circle_color, 2
                )
            else:
                # Surrounding circles
                for circle in range(6 * ring):
                    circle_angle = circle * 2 * math.pi / (6 * ring)
                    circle_x = int(center_x + ring_distance * math.cos(circle_angle))
                    circle_y = int(center_y + ring_distance * math.sin(circle_angle))

                    circle_color = self._get_particle_color(
                        ring * 1000 + circle,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )
                    cv2.circle(
                        frame, (circle_x, circle_y), int(sacred_radius), circle_color, 2
                    )

        # Add merkaba (star tetrahedron)
        merkaba_size = 80 + enhanced_amplitude * 40
        for direction in [1, -1]:  # Upward and downward triangles
            triangle_points = []
            for vertex in range(3):
                vertex_angle = vertex * 2 * math.pi / 3 + current_time * direction * 0.5
                vertex_x = int(center_x + merkaba_size * math.cos(vertex_angle))
                vertex_y = int(
                    center_y + merkaba_size * math.sin(vertex_angle) * direction
                )
                triangle_points.append((vertex_x, vertex_y))

            merkaba_color = self._get_particle_color(
                6666 + direction,
                base_hue,
                enhanced_amplitude,
                current_time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )

            # Draw triangle
            for i in range(3):
                next_i = (i + 1) % 3
                cv2.line(
                    frame, triangle_points[i], triangle_points[next_i], merkaba_color, 3
                )

        # Sacred spiral
        spiral_points = []
        for t in np.linspace(0, 4 * math.pi, 100):
            spiral_radius = 5 + t * (10 + enhanced_amplitude * 5)
            spiral_x = int(center_x + spiral_radius * math.cos(t + current_time))
            spiral_y = int(center_y + spiral_radius * math.sin(t + current_time))
            if 0 <= spiral_x < self.width and 0 <= spiral_y < self.height:
                spiral_points.append((spiral_x, spiral_y))

        for i in range(len(spiral_points) - 1):
            spiral_color = self._get_particle_color(
                i,
                base_hue,
                enhanced_amplitude,
                current_time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
            cv2.line(frame, spiral_points[i], spiral_points[i + 1], spiral_color, 2)

    def _draw_k_tribal(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw tribal/aztec patterns with angular bold shapes."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 1.0 * np.sin(current_time * 4))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 30) % 360

        # 4-fold symmetry for tribal patterns
        num_segments = 4
        segment_angle = 2 * math.pi / num_segments

        # Draw tribal patterns
        for segment in range(num_segments):
            segment_rotation = segment * segment_angle + current_time * 0.4

            # Create bold angular tribal shapes
            for layer in range(3):
                layer_distance = 60 + layer * (40 + enhanced_amplitude * 30)

                # Tribal zigzag patterns
                tribal_points = []
                for step in range(8):
                    step_distance = layer_distance + step * 15
                    zigzag_offset = (step % 2) * 20 - 10  # Zigzag pattern

                    step_angle = step * math.pi / 16
                    rel_x = step_distance * math.cos(step_angle) + zigzag_offset
                    rel_y = step_distance * math.sin(step_angle)

                    # Rotate
                    rot_x = rel_x * math.cos(segment_rotation) - rel_y * math.sin(
                        segment_rotation
                    )
                    rot_y = rel_x * math.sin(segment_rotation) + rel_y * math.cos(
                        segment_rotation
                    )

                    final_x = int(center_x + rot_x)
                    final_y = int(center_y + rot_y)

                    if 0 <= final_x < self.width and 0 <= final_y < self.height:
                        tribal_points.append((final_x, final_y))

                # Draw tribal patterns
                if len(tribal_points) > 1:
                    tribal_color = self._get_particle_color(
                        segment * 1000 + layer * 100,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    # Bold tribal lines
                    for i in range(len(tribal_points) - 1):
                        cv2.line(
                            frame,
                            tribal_points[i],
                            tribal_points[i + 1],
                            tribal_color,
                            4,
                        )

                    # Tribal diamonds/rhombs
                    for i in range(0, len(tribal_points) - 2, 2):
                        diamond_points = [
                            tribal_points[i],
                            (tribal_points[i][0] + 10, tribal_points[i][1] + 10),
                            tribal_points[i + 1],
                            (tribal_points[i][0] - 10, tribal_points[i][1] - 10),
                        ]
                        cv2.fillPoly(
                            frame, [np.array(diamond_points, np.int32)], tribal_color
                        )

        # Central tribal totem
        totem_height = int(60 + enhanced_amplitude * 40)
        totem_color = self._get_particle_color(
            5555,
            base_hue,
            enhanced_amplitude,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        cv2.rectangle(
            frame,
            (center_x - 8, center_y - totem_height // 2),
            (center_x + 8, center_y + totem_height // 2),
            totem_color,
            -1,
        )

    def _draw_k_laser(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw laser beam patterns with intense light rays."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 1.2 * np.sin(current_time * 8))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 50) % 360

        # Multiple laser beams
        num_lasers = int(16 + enhanced_amplitude * 16)

        for laser in range(num_lasers):
            laser_angle = laser * 2 * math.pi / num_lasers + current_time * 2
            laser_length = 200 + enhanced_amplitude * 150

            # Laser beam end point
            end_x = int(center_x + laser_length * math.cos(laser_angle))
            end_y = int(center_y + laser_length * math.sin(laser_angle))

            # Ensure within bounds
            if 0 <= end_x < self.width and 0 <= end_y < self.height:
                laser_color = self._get_particle_color(
                    laser,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )

                # Main laser beam
                laser_thickness = max(1, int(2 + enhanced_amplitude * 6))
                cv2.line(
                    frame,
                    (center_x, center_y),
                    (end_x, end_y),
                    laser_color,
                    laser_thickness,
                )

                # Laser glow effect
                glow_color = self._get_particle_color(
                    laser + 10000,
                    base_hue,
                    enhanced_amplitude * 0.3,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )
                cv2.line(
                    frame,
                    (center_x, center_y),
                    (end_x, end_y),
                    glow_color,
                    max(1, laser_thickness + 4),
                )

                # Laser reflections (shorter beams)
                for reflection in range(3):
                    refl_angle = laser_angle + (reflection - 1) * 0.1
                    refl_length = laser_length * 0.3
                    refl_end_x = int(center_x + refl_length * math.cos(refl_angle))
                    refl_end_y = int(center_y + refl_length * math.sin(refl_angle))

                    if 0 <= refl_end_x < self.width and 0 <= refl_end_y < self.height:
                        cv2.line(
                            frame,
                            (center_x, center_y),
                            (refl_end_x, refl_end_y),
                            glow_color,
                            1,
                        )

        # Central laser core
        core_radius = int(8 + enhanced_amplitude * 20)
        core_color = (255, 255, 255)  # Bright white core
        cv2.circle(frame, (center_x, center_y), core_radius, core_color, -1)

        # Core rings
        for ring in range(3):
            ring_radius = core_radius + ring * 8
            ring_color = self._get_particle_color(
                4444 + ring,
                base_hue,
                enhanced_amplitude,
                current_time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )
            cv2.circle(frame, (center_x, center_y), ring_radius, ring_color, 2)

    def _draw_k_web(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw intricate spider web patterns with radial symmetry."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 0.8 * np.sin(current_time * 3))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 20) % 360

        # Web parameters
        num_radials = 16  # Radial threads
        num_rings = 8  # Concentric rings

        # Draw radial threads
        for radial in range(num_radials):
            radial_angle = radial * 2 * math.pi / num_radials + current_time * 0.1
            thread_length = 200 + enhanced_amplitude * 100

            end_x = int(center_x + thread_length * math.cos(radial_angle))
            end_y = int(center_y + thread_length * math.sin(radial_angle))

            if 0 <= end_x < self.width and 0 <= end_y < self.height:
                thread_color = self._get_particle_color(
                    radial,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )
                cv2.line(frame, (center_x, center_y), (end_x, end_y), thread_color, 1)

        # Draw concentric web rings
        for ring in range(1, num_rings + 1):
            ring_radius = 25 * ring + enhanced_amplitude * 20
            ring_points = []

            for radial in range(num_radials):
                radial_angle = radial * 2 * math.pi / num_radials + current_time * 0.1

                # Add web irregularities for organic feel
                irregularity = 0.8 + 0.4 * math.sin(radial * 0.5 + current_time + ring)
                actual_radius = ring_radius * irregularity

                point_x = int(center_x + actual_radius * math.cos(radial_angle))
                point_y = int(center_y + actual_radius * math.sin(radial_angle))

                if 0 <= point_x < self.width and 0 <= point_y < self.height:
                    ring_points.append((point_x, point_y))

            # Connect ring points
            if len(ring_points) > 1:
                ring_color = self._get_particle_color(
                    ring * 1000,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )

                for i in range(len(ring_points)):
                    next_i = (i + 1) % len(ring_points)
                    cv2.line(frame, ring_points[i], ring_points[next_i], ring_color, 1)

        # Add web dewdrops
        for drop in range(int(10 + enhanced_amplitude * 15)):
            # Random position along web threads
            drop_angle = (drop * 2.7) % (2 * math.pi)
            drop_distance = 30 + (drop * 23) % 150

            drop_x = int(center_x + drop_distance * math.cos(drop_angle))
            drop_y = int(center_y + drop_distance * math.sin(drop_angle))

            if 0 <= drop_x < self.width and 0 <= drop_y < self.height:
                drop_size = max(1, int(2 + enhanced_amplitude * 4))
                drop_color = self._get_particle_color(
                    drop + 20000,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )
                cv2.circle(frame, (drop_x, drop_y), drop_size, drop_color, -1)
                # Dewdrop shine
                cv2.circle(frame, (drop_x - 1, drop_y - 1), 1, (255, 255, 255), -1)

    def _draw_k_spiral(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw multiple interweaving spiral patterns."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 0.9 * np.sin(current_time * 4))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 25) % 360

        # Multiple spiral arms
        num_spirals = 6

        for spiral_id in range(num_spirals):
            spiral_offset = spiral_id * 2 * math.pi / num_spirals
            spiral_direction = 1 if spiral_id % 2 == 0 else -1  # Alternate directions

            spiral_points = []
            for t in np.linspace(0, 6 * math.pi, 150):
                # Logarithmic spiral
                spiral_radius = 5 + t * (8 + enhanced_amplitude * 5)
                spiral_angle = t * spiral_direction + spiral_offset + current_time * 0.5

                spiral_x = int(center_x + spiral_radius * math.cos(spiral_angle))
                spiral_y = int(center_y + spiral_radius * math.sin(spiral_angle))

                if 0 <= spiral_x < self.width and 0 <= spiral_y < self.height:
                    spiral_points.append((spiral_x, spiral_y))

            # Draw spiral
            if len(spiral_points) > 1:
                for i in range(len(spiral_points) - 1):
                    spiral_color = self._get_particle_color(
                        spiral_id * 1000 + i,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    thickness = max(1, int(2 + enhanced_amplitude * 3))
                    cv2.line(
                        frame,
                        spiral_points[i],
                        spiral_points[i + 1],
                        spiral_color,
                        thickness,
                    )

                    # Add spiral particles
                    if i % 8 == 0:  # Every 8th point gets a particle
                        particle_size = max(1, int(3 + enhanced_amplitude * 4))
                        cv2.circle(
                            frame, spiral_points[i], particle_size, spiral_color, -1
                        )

        # Central spiral core
        core_radius = int(12 + enhanced_amplitude * 18)
        core_color = self._get_particle_color(
            3333,
            base_hue,
            enhanced_amplitude,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        cv2.circle(frame, (center_x, center_y), core_radius, core_color, -1)

    def _draw_k_diamond(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw crystalline diamond patterns with prismatic effects."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 0.8 * np.sin(current_time * 6))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 30) % 360

        # 4-fold diamond symmetry
        num_segments = 4
        segment_angle = 2 * math.pi / num_segments

        # Multiple diamond layers
        for layer in range(4):
            layer_size = 50 + layer * (30 + enhanced_amplitude * 20)
            layer_rotation = current_time * (0.3 + layer * 0.1)

            for segment in range(num_segments):
                segment_rotation = segment * segment_angle + layer_rotation

                # Create diamond facet
                diamond_points = []
                facet_angles = [
                    0,
                    math.pi / 3,
                    2 * math.pi / 3,
                    math.pi,
                    4 * math.pi / 3,
                    5 * math.pi / 3,
                ]

                for facet_angle in facet_angles:
                    facet_distance = layer_size * (
                        0.8 + 0.4 * math.sin(facet_angle * 2 + current_time * 3)
                    )

                    rel_x = facet_distance * math.cos(facet_angle)
                    rel_y = facet_distance * math.sin(facet_angle)

                    # Rotate
                    rot_x = rel_x * math.cos(segment_rotation) - rel_y * math.sin(
                        segment_rotation
                    )
                    rot_y = rel_x * math.sin(segment_rotation) + rel_y * math.cos(
                        segment_rotation
                    )

                    final_x = int(center_x + rot_x)
                    final_y = int(center_y + rot_y)

                    if 0 <= final_x < self.width and 0 <= final_y < self.height:
                        diamond_points.append((final_x, final_y))

                # Draw diamond facets
                if len(diamond_points) > 2:
                    diamond_color = self._get_particle_color(
                        segment * 1000 + layer * 100,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    # Fill diamond facet
                    cv2.fillPoly(
                        frame, [np.array(diamond_points, np.int32)], diamond_color
                    )

                    # Diamond outline
                    for i in range(len(diamond_points)):
                        next_i = (i + 1) % len(diamond_points)
                        cv2.line(
                            frame,
                            diamond_points[i],
                            diamond_points[next_i],
                            (255, 255, 255),
                            1,
                        )

                    # Prismatic light rays
                    for ray in range(3):
                        ray_angle = segment_rotation + ray * math.pi / 6
                        ray_length = layer_size * 0.3
                        ray_end_x = int(center_x + ray_length * math.cos(ray_angle))
                        ray_end_y = int(center_y + ray_length * math.sin(ray_angle))

                        if 0 <= ray_end_x < self.width and 0 <= ray_end_y < self.height:
                            ray_color = self._get_particle_color(
                                segment * 1000 + layer * 100 + ray + 10000,
                                base_hue,
                                enhanced_amplitude * 0.5,
                                current_time,
                                gradient_style,
                                custom_colors,
                                particle_color_scheme,
                                particle_gradient_style,
                                particle_custom_colors,
                            )
                            cv2.line(
                                frame,
                                (center_x, center_y),
                                (ray_end_x, ray_end_y),
                                ray_color,
                                2,
                            )

        # Central diamond core
        core_points = [
            (center_x, center_y - 15),
            (center_x + 15, center_y),
            (center_x, center_y + 15),
            (center_x - 15, center_y),
        ]
        core_color = self._get_particle_color(
            2222,
            base_hue,
            enhanced_amplitude,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        cv2.fillPoly(frame, [np.array(core_points, np.int32)], core_color)
        cv2.polylines(
            frame, [np.array(core_points, np.int32)], True, (255, 255, 255), 2
        )

    def _draw_k_stars(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw multiple layered star patterns with stellar symmetry."""
        center_x = self.width // 2
        center_y = self.height // 2

        enhanced_amplitude = amplitude * (1 + 1.0 * np.sin(current_time * 5))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 40) % 360

        # Multiple star layers with different point counts
        star_configs = [
            (5, 60),  # 5-pointed star, radius 60
            (8, 90),  # 8-pointed star, radius 90
            (12, 120),  # 12-pointed star, radius 120
        ]

        for config_idx, (num_points, base_radius) in enumerate(star_configs):
            star_radius = base_radius + enhanced_amplitude * 40
            rotation = current_time * (0.5 + config_idx * 0.2)

            # Create star points
            star_points = []
            for point in range(num_points * 2):  # Outer and inner points
                point_angle = point * math.pi / num_points + rotation

                if point % 2 == 0:  # Outer points
                    point_distance = star_radius
                else:  # Inner points
                    point_distance = star_radius * 0.4

                point_x = int(center_x + point_distance * math.cos(point_angle))
                point_y = int(center_y + point_distance * math.sin(point_angle))

                if 0 <= point_x < self.width and 0 <= point_y < self.height:
                    star_points.append((point_x, point_y))

            # Draw star
            if len(star_points) > 2:
                star_color = self._get_particle_color(
                    config_idx * 1000 + num_points,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )

                # Fill star
                cv2.fillPoly(frame, [np.array(star_points, np.int32)], star_color)

                # Star outline
                for i in range(len(star_points)):
                    next_i = (i + 1) % len(star_points)
                    cv2.line(
                        frame, star_points[i], star_points[next_i], (255, 255, 255), 1
                    )

                # Star rays (from center to outer points)
                for point in range(0, len(star_points), 2):  # Only outer points
                    ray_color = self._get_particle_color(
                        config_idx * 1000 + num_points + point + 5000,
                        base_hue,
                        enhanced_amplitude * 0.7,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )
                    cv2.line(
                        frame, (center_x, center_y), star_points[point], ray_color, 2
                    )

        # Central stellar core with pulsing
        core_radius = int(8 + enhanced_amplitude * 25)
        core_color = self._get_particle_color(
            1111,
            base_hue,
            enhanced_amplitude,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        cv2.circle(frame, (center_x, center_y), core_radius, core_color, -1)

        # Stellar corona
        corona_radius = core_radius + int(10 + enhanced_amplitude * 15)
        corona_color = self._get_particle_color(
            1111 + 500,
            base_hue,
            enhanced_amplitude * 0.3,
            current_time,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )
        cv2.circle(frame, (center_x, center_y), corona_radius, corona_color, 3)

        # Stellar flares
        for flare in range(int(8 + enhanced_amplitude * 12)):
            flare_angle = (
                flare * 2 * math.pi / (8 + enhanced_amplitude * 12) + current_time * 2
            )
            flare_length = 40 + enhanced_amplitude * 60
            flare_end_x = int(center_x + flare_length * math.cos(flare_angle))
            flare_end_y = int(center_y + flare_length * math.sin(flare_angle))

            if 0 <= flare_end_x < self.width and 0 <= flare_end_y < self.height:
                flare_color = self._get_particle_color(
                    flare + 30000,
                    base_hue,
                    enhanced_amplitude,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )
                cv2.line(
                    frame,
                    (center_x, center_y),
                    (flare_end_x, flare_end_y),
                    flare_color,
                    1,
                )

    def _draw_matrix_rain(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw dense Matrix-style digital rain with hundreds of falling streams."""
        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 0.9 * np.sin(current_time * 7))

        # Color system - Matrix green but can vary with audio
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 10) % 360

        # Create MANY vertical streams (very dense)
        num_streams = int(80 + enhanced_amplitude * 120)  # Lots of streams
        stream_width = max(1, self.width // num_streams)

        # Characters to use for matrix effect
        matrix_chars = (
            "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*(){}[]|\\:;\"'<>,.?/~`"
        )

        for stream in range(num_streams):
            stream_x = stream * stream_width + (stream_width // 2)

            # Each stream has its own speed and character density
            stream_speed = 80 + enhanced_amplitude * 200 + (stream % 7) * 20
            stream_density = (
                0.6 + enhanced_amplitude * 0.4
            )  # How dense the characters are

            # Stream length varies
            stream_length = int(100 + enhanced_amplitude * 300)

            # Calculate stream head position
            stream_phase = (current_time * stream_speed + stream * 50) % (
                self.height + stream_length
            )
            stream_head_y = int(stream_phase - stream_length)

            # Draw characters along this stream
            char_spacing = 20  # Pixels between characters
            for char_pos in range(0, stream_length, char_spacing):
                char_y = stream_head_y + char_pos

                if 0 <= char_y < self.height:
                    # Character brightness fades from head to tail
                    brightness_factor = 1.0 - (char_pos / stream_length)
                    char_brightness = int(
                        255 * brightness_factor * (0.5 + 0.5 * enhanced_amplitude)
                    )

                    # Character color using new scheme
                    char_color = self._get_particle_color(
                        stream * 1000 + char_pos,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    # Pick a random character (but consistent for this position)
                    char_index = (
                        stream * 7 + char_pos // char_spacing + int(current_time * 10)
                    ) % len(matrix_chars)
                    matrix_char = matrix_chars[char_index]

                    # Draw character (using simple rectangle for performance)
                    char_size = max(2, int(4 + enhanced_amplitude * 6))
                    cv2.rectangle(
                        frame,
                        (stream_x - char_size // 2, char_y - char_size // 2),
                        (stream_x + char_size // 2, char_y + char_size // 2),
                        char_color,
                        -1,
                    )

                    # Add extra brightness to stream head
                    if char_pos < char_spacing * 3:  # First 3 characters are brightest
                        head_brightness = int(255 * (1 + enhanced_amplitude))
                        head_color = self._get_particle_color(
                            stream * 1000 + char_pos + 50000,
                            base_hue,
                            enhanced_amplitude,
                            current_time,
                            gradient_style,
                            custom_colors,
                            particle_color_scheme,
                            particle_gradient_style,
                            particle_custom_colors,
                        )
                        cv2.rectangle(
                            frame,
                            (stream_x - 1, char_y - 1),
                            (stream_x + 1, char_y + 1),
                            head_color,
                            -1,
                        )

        # Add horizontal glitch lines occasionally
        if enhanced_amplitude > 0.7:
            self._draw_matrix_glitches(
                frame,
                enhanced_amplitude,
                current_time,
                base_hue,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )

    def _draw_matrix_glitches(
        self,
        frame,
        amplitude,
        time,
        base_hue,
        gradient_style="default",
        custom_colors=None,
        particle_color_scheme="multicolor",
        particle_gradient_style=None,
        particle_custom_colors=None,
    ):
        """Add horizontal glitch lines to the matrix effect."""
        num_glitches = int(3 + amplitude * 8)

        for glitch in range(num_glitches):
            glitch_y = int(
                (glitch * 347 + time * 100) % self.height
            )  # Pseudo-random but smooth
            glitch_width = int(50 + amplitude * 200)
            glitch_x = int((time * 80 + glitch * 123) % (self.width - glitch_width))

            # Glitch color using new scheme
            glitch_color = self._get_particle_color(
                glitch,
                base_hue,
                amplitude,
                time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )

            # Draw glitch line
            cv2.rectangle(
                frame,
                (glitch_x, glitch_y),
                (glitch_x + glitch_width, glitch_y + 2),
                glitch_color,
                -1,
            )

    def _draw_starfield(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw dense starfield with hundreds of moving stars and space particles."""
        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 0.8 * np.sin(current_time * 5))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 15) % 360

        # MASSIVE number of stars
        star_count = int(400 + enhanced_amplitude * 600)  # Very dense starfield

        # Multiple layers of stars moving at different speeds
        for layer in range(4):  # 4 depth layers
            layer_speed = (layer + 1) * (20 + enhanced_amplitude * 80)
            layer_star_count = star_count // (layer + 1)  # More stars in closer layers

            for star in range(layer_star_count):
                # Star position with movement
                star_seed = star * 7.91 + layer * 1000  # Pseudo-random but consistent

                # Star moves from center outward (warp speed effect)
                center_x = self.width // 2
                center_y = self.height // 2

                # Initial position (when star was "born")
                initial_angle = (star_seed * 0.01) % (2 * math.pi)

                # Current distance from center based on time
                current_distance = (current_time * layer_speed + star_seed * 10) % 1000

                star_x = center_x + current_distance * math.cos(initial_angle)
                star_y = center_y + current_distance * math.sin(initial_angle)

                # Only draw if star is on screen
                if 0 <= star_x < self.width and 0 <= star_y < self.height:
                    # Star size based on layer and audio
                    star_size = max(1, int(1 + layer + enhanced_amplitude * 4))

                    # Star brightness based on distance and audio
                    distance_factor = min(1.0, current_distance / 300)
                    star_brightness = int(
                        100 + 155 * distance_factor * (0.5 + 0.5 * enhanced_amplitude)
                    )

                    # Star color using new scheme
                    star_color = self._get_particle_color(
                        star + layer * 1000,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    cv2.circle(
                        frame, (int(star_x), int(star_y)), star_size, star_color, -1
                    )

                    # Add star trails for faster moving stars
                    if layer >= 2 and current_distance > 100:
                        trail_length = min(20, int(current_distance * 0.1))
                        trail_x = star_x - trail_length * math.cos(initial_angle)
                        trail_y = star_y - trail_length * math.sin(initial_angle)

                        if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                            trail_color = self._get_particle_color(
                                star + layer * 1000 + 10000,
                                base_hue,
                                enhanced_amplitude * 0.3,
                                current_time,
                                gradient_style,
                                custom_colors,
                                particle_color_scheme,
                                particle_gradient_style,
                                particle_custom_colors,
                            )
                            cv2.line(
                                frame,
                                (int(trail_x), int(trail_y)),
                                (int(star_x), int(star_y)),
                                trail_color,
                                1,
                            )

        # Add space debris/particles
        self._draw_space_debris(
            frame,
            enhanced_amplitude,
            current_time,
            base_hue,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )

        # Add occasional comets
        self._draw_comets(
            frame,
            enhanced_amplitude,
            current_time,
            base_hue,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )

    def _draw_space_debris(
        self,
        frame,
        amplitude,
        time,
        base_hue,
        gradient_style="default",
        custom_colors=None,
        particle_color_scheme="multicolor",
        particle_gradient_style=None,
        particle_custom_colors=None,
    ):
        """Draw space debris and floating particles."""
        debris_count = int(50 + amplitude * 100)

        for debris in range(debris_count):
            # Debris floating in different directions
            debris_angle = (debris * 0.17 + time * 0.3) % (2 * math.pi)
            debris_speed = 20 + debris % 40

            debris_x = int(
                (debris * 53 + time * debris_speed) % (self.width + 100) - 50
            )
            debris_y = int(
                (debris * 71 + time * debris_speed * 0.7) % (self.height + 100) - 50
            )

            if 0 <= debris_x < self.width and 0 <= debris_y < self.height:
                debris_size = max(1, int(2 + amplitude * 5))
                debris_color = self._get_particle_color(
                    debris,
                    base_hue,
                    amplitude,
                    time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )

                cv2.circle(frame, (debris_x, debris_y), debris_size, debris_color, -1)

    def _draw_comets(
        self,
        frame,
        amplitude,
        time,
        base_hue,
        gradient_style="default",
        custom_colors=None,
        particle_color_scheme="multicolor",
        particle_gradient_style=None,
        particle_custom_colors=None,
    ):
        """Draw occasional comets streaking across the screen."""
        if amplitude > 0.6:  # Only when there's significant audio
            num_comets = int(2 + amplitude * 4)

            for comet in range(num_comets):
                comet_phase = (
                    time * (1 + comet * 0.3) + comet * 2
                ) % 8  # 8 second cycle

                # Comet path across screen
                comet_progress = comet_phase / 8
                comet_x = int(-50 + (self.width + 100) * comet_progress)
                comet_y = int(50 + (self.height - 100) * ((comet * 0.37) % 1))

                if 0 <= comet_x < self.width and 0 <= comet_y < self.height:
                    # Comet head
                    comet_size = int(4 + amplitude * 8)
                    comet_color = self._get_particle_color(
                        comet,
                        base_hue,
                        amplitude,
                        time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    cv2.circle(frame, (comet_x, comet_y), comet_size, comet_color, -1)

                    # Comet tail
                    tail_length = 40 + int(amplitude * 60)
                    for tail_seg in range(tail_length):
                        tail_x = comet_x - tail_seg * 2
                        tail_y = comet_y + tail_seg // 2

                        if 0 <= tail_x < self.width and 0 <= tail_y < self.height:
                            tail_color = self._get_particle_color(
                                comet + tail_seg * 100,
                                base_hue,
                                amplitude * (1 - tail_seg / tail_length),
                                time,
                                gradient_style,
                                custom_colors,
                                particle_color_scheme,
                                particle_gradient_style,
                                particle_custom_colors,
                            )
                            cv2.circle(
                                frame,
                                (tail_x, tail_y),
                                max(1, comet_size - tail_seg // 8),
                                tail_color,
                                -1,
                            )

    def _draw_network_web(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw dense network/web with many nodes and dynamic connections."""
        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 1.0 * np.sin(current_time * 6))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 20) % 360

        # LOTS of network nodes
        node_count = int(80 + enhanced_amplitude * 120)
        connection_distance = 120 + enhanced_amplitude * 80  # How far nodes can connect

        # Generate node positions
        nodes = []
        for node in range(node_count):
            # Nodes move slowly around the screen
            node_phase_x = (node * 0.13 + current_time * 0.2) % (2 * math.pi)
            node_phase_y = (node * 0.17 + current_time * 0.15) % (2 * math.pi)

            base_x = (node * 37) % self.width
            base_y = (node * 71) % self.height

            # Add movement
            movement_radius = 30 + enhanced_amplitude * 50
            node_x = base_x + movement_radius * math.cos(node_phase_x)
            node_y = base_y + movement_radius * math.sin(node_phase_y)

            # Keep nodes on screen
            node_x = max(20, min(self.width - 20, node_x))
            node_y = max(20, min(self.height - 20, node_y))

            nodes.append((int(node_x), int(node_y), node))

        # Draw connections between nearby nodes
        for i, (x1, y1, id1) in enumerate(nodes):
            for j, (x2, y2, id2) in enumerate(nodes[i + 1 :], i + 1):
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                if distance < connection_distance:
                    # Connection strength based on distance and audio
                    connection_strength = 1.0 - (distance / connection_distance)
                    connection_brightness = int(
                        100 + 155 * connection_strength * enhanced_amplitude
                    )

                    # Connection color using new scheme
                    connection_color = self._get_particle_color(
                        id1 + id2,
                        base_hue,
                        enhanced_amplitude * connection_strength,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    # Line thickness based on connection strength
                    line_thickness = max(
                        1, int(1 + 3 * connection_strength * enhanced_amplitude)
                    )

                    cv2.line(
                        frame, (x1, y1), (x2, y2), connection_color, line_thickness
                    )

                    # Add data packets moving along connections
                    if (
                        connection_strength > 0.7
                        and enhanced_amplitude > 0.5
                        and distance > 1
                    ):
                        packet_progress = (current_time * 100 + id1 * 50) % int(
                            distance
                        )
                        packet_ratio = packet_progress / distance

                        packet_x = int(x1 + (x2 - x1) * packet_ratio)
                        packet_y = int(y1 + (y2 - y1) * packet_ratio)

                        packet_color = self._get_particle_color(
                            id1 + id2 + 10000,
                            base_hue,
                            enhanced_amplitude,
                            current_time,
                            gradient_style,
                            custom_colors,
                            particle_color_scheme,
                            particle_gradient_style,
                            particle_custom_colors,
                        )
                        cv2.circle(frame, (packet_x, packet_y), 3, packet_color, -1)

        # Draw nodes
        for x, y, node_id in nodes:
            # Node size based on how many connections it has
            node_connections = sum(
                1
                for x2, y2, _ in nodes
                if math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2) < connection_distance
            )

            node_size = max(3, int(4 + node_connections * 2 + enhanced_amplitude * 5))

            # Node color using new scheme
            node_color = self._get_particle_color(
                node_id,
                base_hue,
                enhanced_amplitude,
                current_time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )

            cv2.circle(frame, (x, y), node_size, node_color, -1)

            # Node pulse effect
            if enhanced_amplitude > 0.6:
                pulse_size = node_size + int(
                    5 * enhanced_amplitude * math.sin(current_time * 8 + node_id)
                )
                pulse_color = self._get_particle_color(
                    node_id + 5000,
                    base_hue,
                    enhanced_amplitude * 0.5,
                    current_time,
                    gradient_style,
                    custom_colors,
                    particle_color_scheme,
                    particle_gradient_style,
                    particle_custom_colors,
                )
                cv2.circle(frame, (x, y), pulse_size, pulse_color, 1)

    def _draw_particle_swarm(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw massive swarm of particles that move like flocking birds."""
        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 0.9 * np.sin(current_time * 8))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 25) % 360

        # MASSIVE swarm
        swarm_count = int(300 + enhanced_amplitude * 500)

        # Multiple swarms with different behaviors
        num_swarms = 3
        swarm_size = swarm_count // num_swarms

        for swarm_id in range(num_swarms):
            # Each swarm has a different movement pattern
            swarm_speed = 30 + swarm_id * 20 + enhanced_amplitude * 40
            swarm_radius = 150 + swarm_id * 100

            # Swarm center moves around
            center_x = self.width // 2 + 200 * math.cos(
                current_time * 0.5 + swarm_id * 2
            )
            center_y = self.height // 2 + 100 * math.sin(
                current_time * 0.3 + swarm_id * 1.5
            )

            # Draw particles in this swarm
            for particle in range(swarm_size):
                particle_id = swarm_id * swarm_size + particle

                # Particle orbits around swarm center with some chaos
                base_angle = (particle * 0.1 + current_time * swarm_speed * 0.01) % (
                    2 * math.pi
                )
                chaos_angle = 0.5 * math.sin(current_time * 3 + particle * 0.2)
                final_angle = base_angle + chaos_angle

                # Distance from center varies
                base_distance = swarm_radius * (
                    0.3 + 0.7 * ((particle * 7) % 100) / 100
                )
                distance_variation = (
                    enhanced_amplitude
                    * 50
                    * math.sin(current_time * 4 + particle * 0.3)
                )
                final_distance = base_distance + distance_variation

                particle_x = int(center_x + final_distance * math.cos(final_angle))
                particle_y = int(center_y + final_distance * math.sin(final_angle))

                # Only draw if on screen
                if 0 <= particle_x < self.width and 0 <= particle_y < self.height:
                    # Particle size varies
                    particle_size = max(
                        1,
                        int(
                            2
                            + enhanced_amplitude * 4
                            + math.sin(particle * 0.1 + current_time * 6)
                        ),
                    )

                    # Particle color using new scheme
                    particle_color = self._get_particle_color(
                        particle_id,
                        base_hue,
                        enhanced_amplitude,
                        current_time,
                        gradient_style,
                        custom_colors,
                        particle_color_scheme,
                        particle_gradient_style,
                        particle_custom_colors,
                    )

                    cv2.circle(
                        frame,
                        (particle_x, particle_y),
                        particle_size,
                        particle_color,
                        -1,
                    )

                    # Add motion trails for some particles
                    if particle % 5 == 0:  # Every 5th particle gets a trail
                        trail_angle = final_angle - 0.2
                        trail_x = int(
                            center_x + (final_distance - 20) * math.cos(trail_angle)
                        )
                        trail_y = int(
                            center_y + (final_distance - 20) * math.sin(trail_angle)
                        )

                        if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                            trail_color = self._get_particle_color(
                                particle_id + 10000,
                                base_hue,
                                enhanced_amplitude * 0.5,
                                current_time,
                                gradient_style,
                                custom_colors,
                                particle_color_scheme,
                                particle_gradient_style,
                                particle_custom_colors,
                            )
                            cv2.line(
                                frame,
                                (trail_x, trail_y),
                                (particle_x, particle_y),
                                trail_color,
                                1,
                            )

        # Add inter-swarm connections
        self._draw_swarm_connections(
            frame, enhanced_amplitude, current_time, base_hue, num_swarms
        )

    def _draw_swarm_connections(self, frame, amplitude, time, base_hue, num_swarms):
        """Draw connections between different swarms."""
        if amplitude > 0.7:  # Only when audio is strong
            for swarm1 in range(num_swarms):
                for swarm2 in range(swarm1 + 1, num_swarms):
                    # Connection between swarm centers
                    center1_x = self.width // 2 + 200 * math.cos(
                        time * 0.5 + swarm1 * 2
                    )
                    center1_y = self.height // 2 + 100 * math.sin(
                        time * 0.3 + swarm1 * 1.5
                    )

                    center2_x = self.width // 2 + 200 * math.cos(
                        time * 0.5 + swarm2 * 2
                    )
                    center2_y = self.height // 2 + 100 * math.sin(
                        time * 0.3 + swarm2 * 1.5
                    )

                    # Energy beam between swarms
                    beam_hue = (base_hue + (swarm1 + swarm2) * 40) % 360
                    beam_color = self._hsv_to_bgr(
                        beam_hue, 255, int(100 + 100 * amplitude)
                    )

                    cv2.line(
                        frame,
                        (int(center1_x), int(center1_y)),
                        (int(center2_x), int(center2_y)),
                        beam_color,
                        2,
                    )

    def _draw_fireworks_explosion(
        self,
        frame: np.ndarray,
        amplitude: float,
        current_time: float,
        audio_features: dict,
        frame_idx: int,
        total_frames: int,
        gradient_style: str = "default",
        custom_colors: list = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ):
        """Draw multiple fireworks explosions with hundreds of particles."""
        # Enhanced amplitude
        enhanced_amplitude = amplitude * (1 + 1.1 * np.sin(current_time * 9))

        # Color system
        spectral_idx = min(
            int(
                current_time
                * len(audio_features["spectral_centroids"])
                / audio_features["duration"]
            ),
            len(audio_features["spectral_centroids"]) - 1,
        )
        spectral_value = audio_features["spectral_centroids"][spectral_idx]
        base_hue = int((spectral_value / 4000) * 360 + current_time * 30) % 360

        # Multiple simultaneous fireworks
        num_fireworks = int(4 + enhanced_amplitude * 8)

        for firework_id in range(num_fireworks):
            # Each firework has its own lifecycle (3 second cycle)
            firework_cycle = 3
            firework_phase = (
                (current_time + firework_id * 0.7) % firework_cycle
            ) / firework_cycle

            # Firework center position
            fw_x = int((firework_id * 313 + current_time * 20) % self.width)
            fw_y = int(
                (firework_id * 271 + current_time * 15) % (self.height * 0.7)
                + self.height * 0.15
            )

            # Explosion characteristics change through the cycle
            if firework_phase < 0.8:  # Explosion phase
                explosion_age = firework_phase / 0.8
                explosion_radius = int(
                    150 * explosion_age * (1 + enhanced_amplitude * 0.5)
                )

                # LOTS of explosion particles
                particles_per_firework = int(80 + enhanced_amplitude * 120)

                for particle in range(particles_per_firework):
                    # Particle direction (random but consistent)
                    particle_angle = (particle * 0.1 + firework_id * 2) % (2 * math.pi)

                    # Particle speed varies
                    particle_speed = 0.5 + (particle % 10) * 0.1

                    # Current particle position
                    particle_distance = explosion_radius * particle_speed
                    particle_x = int(
                        fw_x + particle_distance * math.cos(particle_angle)
                    )
                    particle_y = int(
                        fw_y
                        + particle_distance * math.sin(particle_angle)
                        + explosion_age * 50
                    )  # Gravity

                    if 0 <= particle_x < self.width and 0 <= particle_y < self.height:
                        # Particle fades as explosion ages
                        particle_brightness = int(
                            255 * (1 - explosion_age) * (0.5 + 0.5 * enhanced_amplitude)
                        )

                        # Particle color using new scheme
                        particle_color = self._get_particle_color(
                            firework_id * 1000 + particle,
                            base_hue,
                            enhanced_amplitude,
                            current_time,
                            gradient_style,
                            custom_colors,
                            particle_color_scheme,
                            particle_gradient_style,
                            particle_custom_colors,
                        )

                        # Particle size decreases over time
                        particle_size = max(
                            1, int(4 * (1 - explosion_age) + enhanced_amplitude * 3)
                        )

                        cv2.circle(
                            frame,
                            (particle_x, particle_y),
                            particle_size,
                            particle_color,
                            -1,
                        )

                        # Add sparkle effect to some particles
                        if particle % 8 == 0 and explosion_age < 0.5:
                            sparkle_size = particle_size + 2
                            sparkle_color = (255, 255, 255)
                            cv2.circle(
                                frame,
                                (particle_x, particle_y),
                                sparkle_size,
                                sparkle_color,
                                1,
                            )

                # Central explosion flash
                if explosion_age < 0.3:
                    flash_radius = int(
                        20 * (1 - explosion_age * 3) * (1 + enhanced_amplitude)
                    )
                    flash_color = self._hsv_to_bgr(
                        (base_hue + firework_id * 45) % 360,
                        100,
                        int(255 * (1 - explosion_age * 3)),
                    )
                    cv2.circle(frame, (fw_x, fw_y), flash_radius, flash_color, -1)

        # Add background sparkles/embers
        self._draw_firework_embers(
            frame,
            enhanced_amplitude,
            current_time,
            base_hue,
            gradient_style,
            custom_colors,
            particle_color_scheme,
            particle_gradient_style,
            particle_custom_colors,
        )

    def _draw_firework_embers(
        self,
        frame,
        amplitude,
        time,
        base_hue,
        gradient_style="default",
        custom_colors=None,
        particle_color_scheme="multicolor",
        particle_gradient_style=None,
        particle_custom_colors=None,
    ):
        """Draw floating embers and sparkles in the background."""
        ember_count = int(50 + amplitude * 100)

        for ember in range(ember_count):
            # Embers float down slowly
            ember_x = int((ember * 43 + time * 20) % self.width)
            ember_y = int((ember * 67 + time * 30) % self.height)

            # Ember flicker
            flicker = 0.5 + 0.5 * math.sin(time * 10 + ember * 0.5)

            # Ember color using new scheme
            ember_color = self._get_particle_color(
                ember,
                base_hue,
                amplitude * flicker,
                time,
                gradient_style,
                custom_colors,
                particle_color_scheme,
                particle_gradient_style,
                particle_custom_colors,
            )

            ember_size = max(1, int(1 + amplitude * 3 * flicker))
            cv2.circle(frame, (ember_x, ember_y), ember_size, ember_color, -1)

    def create_video(
        self,
        audio_path: Path,
        output_path: Path,
        background_keywords: str = "abstract,gradient,minimal",
        waveform_style: str = "circular",
        gradient_style: str = "default",
        custom_colors: list = None,
        no_unsplash: bool = False,
        dynamic_background: str = "none",
        preview_duration: float = None,
        particle_color_scheme: str = "multicolor",
        particle_gradient_style: str = None,
        particle_custom_colors: list = None,
    ) -> bool:
        """Create vertical video with waveform animation.

        Args:
            preview_duration: If provided, limits video to this duration in seconds for preview mode
        """
        try:
            print("🎬 Starting video creation...")

            # Get background image
            # Prepare background - static or dynamic
            bg_image = None
            bg_path = None
            use_dynamic_bg = dynamic_background != "none"

            if use_dynamic_bg:
                print(f"🌊 Using dynamic background: {dynamic_background}")
                # Create a dummy background for the first frame
                bg_image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                bg_path = None
            else:
                if no_unsplash:
                    print(f"🌈 Using gradient background: {gradient_style}...")
                    bg_path = self.create_fallback_background(
                        gradient_style, custom_colors
                    )
                else:
                    print("🖼️  Downloading background image...")
                    bg_path = self.get_random_unsplash_image(background_keywords)
                    if not bg_path:
                        print(f"📸 Using gradient background: {gradient_style}...")
                        bg_path = self.create_fallback_background(
                            gradient_style, custom_colors
                        )

                # Load and resize background
                bg_image = cv2.imread(str(bg_path))
                bg_image = cv2.resize(bg_image, (self.width, self.height))

                # Add slight blur and darken for better contrast
                bg_image = cv2.GaussianBlur(bg_image, (15, 15), 0)
                bg_image = cv2.addWeighted(
                    bg_image, 0.7, np.zeros_like(bg_image), 0.3, 0
                )

            print("🎵 Extracting audio features...")
            audio_features = self.extract_audio_features(audio_path, preview_duration)

            if not audio_features:
                print("❌ Failed to extract audio features")
                return False

            # Calculate video parameters
            duration = audio_features["duration"]

            # Limit duration for preview mode
            if preview_duration is not None and duration > preview_duration:
                duration = preview_duration
                print(f"🎞️  Preview mode: limiting to {preview_duration} seconds")

            total_frames = int(duration * self.fps)

            print(f"🎥 Creating video: {duration:.1f}s, {total_frames} frames")

            # Create temporary video file
            temp_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            temp_video_path = temp_video.name
            temp_video.close()

            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(
                temp_video_path, fourcc, self.fps, (self.width, self.height)
            )

            # Generate frames
            for frame_idx in range(total_frames):
                if frame_idx % 30 == 0:  # Progress every second
                    print(
                        f"🎬 Progress: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)"
                    )

                # Generate dynamic background if needed
                current_bg = bg_image
                if use_dynamic_bg:
                    # Calculate current time and amplitude for dynamic background
                    current_time = (frame_idx / total_frames) * duration
                    rms_idx = min(
                        int(
                            current_time
                            * len(audio_features["rms"])
                            / audio_features["duration"]
                        ),
                        len(audio_features["rms"]) - 1,
                    )
                    current_amplitude = audio_features["rms"][rms_idx]
                    max_amplitude = np.max(audio_features["rms"])
                    normalized_amplitude = (
                        current_amplitude / max_amplitude if max_amplitude > 0 else 0
                    )

                    current_bg = self.create_dynamic_background(
                        dynamic_background,
                        normalized_amplitude,
                        current_time,
                        frame_idx,
                        total_frames,
                        gradient_style,
                        custom_colors,
                    )

                frame = self.create_waveform_frame(
                    current_bg,
                    audio_features,
                    frame_idx,
                    total_frames,
                    style=waveform_style,
                    gradient_style=gradient_style,
                    custom_colors=custom_colors,
                    particle_color_scheme=particle_color_scheme,
                    particle_gradient_style=particle_gradient_style,
                    particle_custom_colors=particle_custom_colors,
                )
                out.write(frame)

            out.release()

            print("🎵 Adding audio to video...")
            # Use ffmpeg to add audio
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                temp_video_path,
                "-i",
                str(audio_path),
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-strict",
                "experimental",
                "-shortest",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ FFmpeg error: {result.stderr}")
                return False

            # Cleanup
            os.unlink(temp_video_path)
            if bg_path and bg_path.exists():
                os.unlink(bg_path)

            print(f"✅ Video created successfully: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Error creating video: {e}")
            return False


def create_vertical_video(
    audio_path: Path,
    output_path: Path,
    background_keywords: str = "abstract,gradient,minimal",
    waveform_style: str = "circular",
    gradient_style: str = "default",
    custom_colors: list = None,
    no_unsplash: bool = False,
    dynamic_background: str = "none",
    orientation: str = "vertical",
    preview_duration: float = None,
    particle_color_scheme: str = "multicolor",
    particle_gradient_style: str = None,
    particle_custom_colors: list = None,
) -> bool:
    """Convenience function to create vertical or horizontal video.

    Args:
        audio_path: Path to the audio file
        output_path: Path for the output video
        background_keywords: Keywords for background image from Unsplash
        waveform_style: Style of visualization:
            - "circular": Circular waveform with bars
            - "sine": Sine wave patterns
            - "mathematical" or "fractal": Mathematical forms (Fibonacci spirals,
              Lissajous curves, polar roses, interference patterns, fractals)
            - "julia" or "mandelbrot": Julia set with infinite zoom (más rápido que Mandelbrot)
            - "psychedelic" or "circles": Zoom psicodélico de círculos concéntricos
            - "fluid" or "liquid": Ondas fluidas suaves con burbujas flotantes
            - "particles" or "sand": Partículas cayendo como arena o nieve
            - "morph" or "shapes": Formas geométricas que se transforman suavemente
            - "kaleidoscope" or "mirror": Patrones caleidoscópicos simétricos
            - "breathing" or "zen": Patrones que respiran y pulsan zen
            - "matrix" or "rain": Lluvia digital tipo Matrix con muchos streams
            - "starfield" or "space": Campo de estrellas denso con efecto warp
            - "network" or "web": Red densa de conexiones con paquetes de datos
            - "swarm" or "flock": Enjambre masivo de partículas tipo bandada
            - "explosion" or "fireworks": Múltiples explosiones de fuegos artificiales
        gradient_style: Background gradient style when Unsplash fails:
            - "default": Deep blue to purple (original)
            - "dark_teal_orange": Dark teal to vibrant orange
            - "sunset": Warm sunset colors
            - "ocean": Ocean blues
            - "purple_pink": Deep purple to pink
            - "forest": Forest green to gold
            - "midnight": Midnight blues and purples
            - "fire": Dark red to orange to gold
            - "arctic": Arctic blues
            - "cosmic": Deep space colors
        custom_colors: List of RGB tuples for custom gradient, overrides gradient_style
        no_unsplash: Skip Unsplash download and use only gradient background
        orientation: "vertical" for 1080x1920, "horizontal" for 1920x1080
                preview_duration: Maximum duration in seconds for preview mode (None for full video)
        particle_color_scheme: Color scheme for particles:
            - "multicolor": Rainbow colors (default)
            - "background": Colors similar to background gradient
            - "dissonant": Contrasting/clashing colors
            - "triadic": Triadic complementary color scheme
            - "monochrome": All particles use exact background gradient colors
    """
    creator = VerticalVideoCreator(orientation=orientation)
    return creator.create_video(
        audio_path,
        output_path,
        background_keywords,
        waveform_style,
        gradient_style,
        custom_colors,
        no_unsplash,
        dynamic_background,
        preview_duration,
        particle_color_scheme,
        particle_gradient_style,
        particle_custom_colors,
    )


def create_horizontal_video(
    audio_path: Path,
    output_path: Path,
    background_keywords: str = "abstract,gradient,minimal",
    waveform_style: str = "circular",
    gradient_style: str = "default",
    custom_colors: list = None,
    no_unsplash: bool = False,
    dynamic_background: str = "none",
    preview_duration: float = None,
    particle_color_scheme: str = "multicolor",
    particle_gradient_style: str = None,
    particle_custom_colors: list = None,
) -> bool:
    """Convenience function to create horizontal video (1920x1080).

    Args:
        audio_path: Path to the audio file
        output_path: Path for the output video
        background_keywords: Keywords for background image from Unsplash
        waveform_style: Style of visualization:
            - "circular": Circular waveform with bars
            - "sine": Sine wave patterns
            - "mathematical" or "fractal": Mathematical forms
            - "julia" or "mandelbrot": Julia set with infinite zoom (más rápido que Mandelbrot)
            - "psychedelic" or "circles": Zoom psicodélico de círculos concéntricos
            - "fluid" or "liquid": Ondas fluidas suaves con burbujas flotantes
            - "particles" or "sand": Partículas cayendo como arena o nieve
            - "morph" or "shapes": Formas geométricas que se transforman suavemente
            - "kaleidoscope" or "mirror": Patrones caleidoscópicos simétricos
            - "breathing" or "zen": Patrones que respiran y pulsan zen
            - "matrix" or "rain": Lluvia digital tipo Matrix con muchos streams
            - "starfield" or "space": Campo de estrellas denso con efecto warp
            - "network" or "web": Red densa de conexiones con paquetes de datos
            - "swarm" or "flock": Enjambre masivo de partículas tipo bandada
            - "explosion" or "fireworks": Múltiples explosiones de fuegos artificiales
        gradient_style: Background gradient style when Unsplash fails
        custom_colors: List of RGB tuples for custom gradient, overrides gradient_style
        no_unsplash: Skip Unsplash download and use only gradient background
        dynamic_background: Dynamic animated background style:
            - "none": Static background (default)
            - "flowing-gradient": Flowing gradient that responds to audio
            - "aurora": Aurora borealis effect
            - "plasma": Plasma energy effect
            - "liquid-metal": Liquid metal effect
            - "nebula": Space nebula effect
            - "cosmic-dust": Cosmic dust field effect
            - "energy-waves": Energy waves effect
            - "particle-field": Particle field effect
            - "morphing-shapes": Morphing geometric shapes
            - "breathing-colors": Breathing colors effect
        preview_duration: Maximum duration in seconds for preview mode (None for full video)
        particle_color_scheme: Color scheme for particles:
            - "multicolor": Rainbow colors (default)
            - "background": Colors similar to background gradient
            - "dissonant": Contrasting/clashing colors
            - "triadic": Triadic complementary color scheme
            - "monochrome": All particles use exact background gradient colors
        particle_gradient_style: Specific gradient style for particles (overrides gradient_style)
        particle_custom_colors: Custom colors specific for particles (overrides custom_colors)
    """
    return create_vertical_video(
        audio_path,
        output_path,
        background_keywords,
        waveform_style,
        gradient_style,
        custom_colors,
        no_unsplash,
        dynamic_background,
        orientation="horizontal",
        preview_duration=preview_duration,
        particle_color_scheme=particle_color_scheme,
        particle_gradient_style=particle_gradient_style,
        particle_custom_colors=particle_custom_colors,
    )
