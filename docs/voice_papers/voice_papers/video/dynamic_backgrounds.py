"""
Dynamic background methods for video creation.
"""

import numpy as np
import cv2


class DynamicBackgrounds:
    """Mixin class for dynamic background methods."""

    def _create_flowing_gradient(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create a flowing gradient background that changes with time and audio."""
        height, width = frame.shape[:2]

        # Get gradient colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [(20, 20, 50), (100, 20, 150)]  # Default colors

        # Create flowing effect with time and amplitude
        time_offset = current_time * 0.3
        audio_offset = amplitude * 50

        for y in range(height):
            for x in range(width):
                # Create flowing pattern
                wave1 = np.sin((x + y) * 0.01 + time_offset) * 0.3
                wave2 = np.sin((x - y) * 0.008 + time_offset * 1.2) * 0.3
                wave3 = np.sin(np.sqrt(x * x + y * y) * 0.005 + time_offset * 0.8) * 0.2

                # Combine waves with audio influence
                flow_factor = (wave1 + wave2 + wave3 + audio_offset * 0.01) * 0.5 + 0.5
                flow_factor = np.clip(flow_factor, 0, 1)

                # Interpolate between colors
                if len(colors) == 2:
                    r = int(
                        colors[0][0] * (1 - flow_factor) + colors[1][0] * flow_factor
                    )
                    g = int(
                        colors[0][1] * (1 - flow_factor) + colors[1][1] * flow_factor
                    )
                    b = int(
                        colors[0][2] * (1 - flow_factor) + colors[1][2] * flow_factor
                    )
                else:
                    # Multi-color gradient
                    color_index = flow_factor * (len(colors) - 1)
                    idx1 = int(color_index)
                    idx2 = min(idx1 + 1, len(colors) - 1)
                    t = color_index - idx1

                    r = int(colors[idx1][0] * (1 - t) + colors[idx2][0] * t)
                    g = int(colors[idx1][1] * (1 - t) + colors[idx2][1] * t)
                    b = int(colors[idx1][2] * (1 - t) + colors[idx2][2] * t)

                frame[y, x] = [b, g, r]  # BGR format

        return frame

    def _create_aurora_background(self, frame, amplitude, current_time):
        """Create aurora borealis effect."""
        height, width = frame.shape[:2]

        # Aurora colors (green, blue, purple)
        aurora_colors = [
            (0, 255, 100),  # Green
            (100, 255, 0),  # Blue-green
            (255, 0, 100),  # Purple-blue
            (200, 50, 255),  # Purple
        ]

        for y in range(height):
            for x in range(width):
                # Create flowing aurora waves
                wave1 = np.sin(x * 0.02 + current_time * 2 + y * 0.01) * 0.5
                wave2 = np.sin(x * 0.015 + current_time * 1.5 + y * 0.008) * 0.3
                wave3 = np.sin(x * 0.01 + current_time + y * 0.005) * 0.2

                # Combine waves with amplitude
                intensity = (wave1 + wave2 + wave3 + amplitude * 0.5) * 0.3 + 0.1
                intensity = np.clip(intensity, 0, 1)

                # Vertical gradient effect (stronger at top)
                vertical_factor = 1.0 - (y / height) * 0.7
                intensity *= vertical_factor

                # Choose color based on position and time
                color_idx = int(
                    (x / width + current_time * 0.1) * len(aurora_colors)
                ) % len(aurora_colors)
                base_color = aurora_colors[color_idx]

                r = int(base_color[0] * intensity)
                g = int(base_color[1] * intensity)
                b = int(base_color[2] * intensity)

                frame[y, x] = [b, g, r]

        return frame

    def _create_plasma_background(self, frame, amplitude, current_time):
        """Create plasma energy effect."""
        height, width = frame.shape[:2]

        for y in range(height):
            for x in range(width):
                # Create plasma effect with multiple sine waves
                dx = x - width / 2
                dy = y - height / 2
                dist = np.sqrt(dx * dx + dy * dy)

                plasma1 = np.sin(dist * 0.02 + current_time * 3)
                plasma2 = np.sin((x + y) * 0.01 + current_time * 2)
                plasma3 = np.sin((x - y) * 0.008 + current_time * 1.5)
                plasma4 = np.sin(np.sqrt(x * y) * 0.01 + current_time * 2.5)

                # Combine with amplitude
                plasma_value = (
                    plasma1 + plasma2 + plasma3 + plasma4 + amplitude
                ) * 0.2 + 0.5
                plasma_value = np.clip(plasma_value, 0, 1)

                # Map to electric colors
                if plasma_value < 0.33:
                    # Deep blue to cyan
                    t = plasma_value * 3
                    r, g, b = (
                        int(20 * (1 - t) + 0 * t),
                        int(20 * (1 - t) + 255 * t),
                        int(100 * (1 - t) + 255 * t),
                    )
                elif plasma_value < 0.66:
                    # Cyan to magenta
                    t = (plasma_value - 0.33) * 3
                    r, g, b = (
                        int(0 * (1 - t) + 255 * t),
                        int(255 * (1 - t) + 0 * t),
                        255,
                    )
                else:
                    # Magenta to white
                    t = (plasma_value - 0.66) * 3
                    r, g, b = 255, int(0 * (1 - t) + 255 * t), 255

                frame[y, x] = [b, g, r]

        return frame

    def _create_breathing_colors_background(
        self,
        frame,
        amplitude,
        current_time,
        gradient_style="default",
        custom_colors=None,
    ):
        """Create breathing color effect that pulses with audio."""
        height, width = frame.shape[:2]

        # Get base colors
        colors = self._get_current_gradient_colors(gradient_style, custom_colors)
        if len(colors) < 2:
            colors = [(50, 0, 100), (100, 50, 200)]

        # Create breathing effect
        breath_cycle = np.sin(current_time * 1.5) * 0.3 + 0.7
        audio_pulse = amplitude * 0.5 + 0.5
        combined_pulse = (breath_cycle + audio_pulse) * 0.5

        center_x, center_y = width // 2, height // 2

        for y in range(height):
            for x in range(width):
                # Distance from center
                dx = x - center_x
                dy = y - center_y
                dist = np.sqrt(dx * dx + dy * dy) / max(width, height)

                # Create breathing gradient
                intensity = np.sin(dist * np.pi + combined_pulse * np.pi) * 0.5 + 0.5

                # Interpolate colors
                r = int(colors[0][0] * (1 - intensity) + colors[1][0] * intensity)
                g = int(colors[0][1] * (1 - intensity) + colors[1][1] * intensity)
                b = int(colors[0][2] * (1 - intensity) + colors[1][2] * intensity)

                frame[y, x] = [b, g, r]

        return frame

    def _create_nebula_background(
        self, frame, amplitude, current_time, frame_idx, total_frames
    ):
        """Create space nebula effect."""
        height, width = frame.shape[:2]

        # Nebula colors
        nebula_colors = [
            (20, 20, 80),  # Deep blue
            (80, 20, 120),  # Purple
            (120, 60, 200),  # Light purple
            (200, 100, 255),  # Pink
            (255, 150, 100),  # Orange
        ]

        for y in range(height):
            for x in range(width):
                # Create nebula clouds with Perlin-like noise
                noise1 = np.sin(x * 0.005 + current_time * 0.5) * np.cos(
                    y * 0.008 + current_time * 0.3
                )
                noise2 = np.sin(x * 0.008 + y * 0.006 + current_time * 0.8)
                noise3 = np.sin((x + y) * 0.003 + current_time * 0.2)

                # Combine noises
                cloud_density = (
                    noise1 + noise2 + noise3 + amplitude * 0.3
                ) * 0.25 + 0.5
                cloud_density = np.clip(cloud_density, 0, 1)

                # Add swirling effect
                dx = x - width / 2
                dy = y - height / 2
                angle = np.arctan2(dy, dx) + current_time * 0.1
                swirl = np.sin(angle * 3) * 0.1
                cloud_density += swirl
                cloud_density = np.clip(cloud_density, 0, 1)

                # Map to nebula colors
                color_idx = int(cloud_density * (len(nebula_colors) - 1))
                color_t = (cloud_density * (len(nebula_colors) - 1)) - color_idx

                if color_idx < len(nebula_colors) - 1:
                    color1 = nebula_colors[color_idx]
                    color2 = nebula_colors[color_idx + 1]
                    r = int(color1[0] * (1 - color_t) + color2[0] * color_t)
                    g = int(color1[1] * (1 - color_t) + color2[1] * color_t)
                    b = int(color1[2] * (1 - color_t) + color2[2] * color_t)
                else:
                    r, g, b = nebula_colors[-1]

                frame[y, x] = [b, g, r]

        return frame

    def _create_energy_waves_background(self, frame, amplitude, current_time):
        """Create energy waves background."""
        height, width = frame.shape[:2]

        center_x, center_y = width // 2, height // 2

        for y in range(height):
            for x in range(width):
                dx = x - center_x
                dy = y - center_y
                dist = np.sqrt(dx * dx + dy * dy)
                angle = np.arctan2(dy, dx)

                # Create concentric energy waves
                wave1 = np.sin(dist * 0.02 - current_time * 5) * 0.5
                wave2 = np.sin(dist * 0.015 - current_time * 3) * 0.3
                wave3 = np.sin(angle * 4 + current_time * 2) * 0.2

                # Combine with amplitude
                energy = (wave1 + wave2 + wave3 + amplitude * 0.8) * 0.3 + 0.1
                energy = np.clip(energy, 0, 1)

                # Electric blue/cyan energy colors
                if energy < 0.5:
                    t = energy * 2
                    r, g, b = (
                        int(0 * t),
                        int(50 * (1 - t) + 150 * t),
                        int(50 * (1 - t) + 255 * t),
                    )
                else:
                    t = (energy - 0.5) * 2
                    r, g, b = (
                        int(0 * (1 - t) + 255 * t),
                        int(150 * (1 - t) + 255 * t),
                        255,
                    )

                frame[y, x] = [b, g, r]

        return frame

    def _create_liquid_metal_background(self, frame, amplitude, current_time):
        """Create liquid metal effect."""
        height, width = frame.shape[:2]

        for y in range(height):
            for x in range(width):
                # Create flowing metal effect
                flow1 = np.sin(x * 0.01 + current_time * 2) * 0.4
                flow2 = np.sin(y * 0.008 + current_time * 1.5) * 0.3
                flow3 = np.sin((x + y) * 0.005 + current_time * 1.2) * 0.3

                # Metallic ripples
                dx = x - width / 2
                dy = y - height / 2
                dist = np.sqrt(dx * dx + dy * dy)
                ripple = np.sin(dist * 0.03 + current_time * 4) * 0.2

                # Combine with amplitude
                metal_value = (
                    flow1 + flow2 + flow3 + ripple + amplitude * 0.4
                ) * 0.3 + 0.3
                metal_value = np.clip(metal_value, 0, 1)

                # Metallic silver/gold colors
                base_color = int(metal_value * 200 + 55)
                highlight = (
                    int(metal_value * 100 + 155) if metal_value > 0.7 else base_color
                )

                r = min(255, int(base_color * 0.9 + highlight * 0.1))
                g = min(255, int(base_color * 0.95 + highlight * 0.05))
                b = base_color

                frame[y, x] = [b, g, r]

        return frame

    def _create_cosmic_dust_background(self, frame, amplitude, current_time, frame_idx):
        """Create cosmic dust field effect."""
        height, width = frame.shape[:2]

        # Base dark space color
        frame.fill(10)  # Very dark

        # Add dust particles
        num_particles = int(300 + amplitude * 200)

        for i in range(num_particles):
            # Pseudo-random positions based on frame and particle index
            seed = (frame_idx * 1000 + i) % 10000
            np.random.seed(seed)

            x = int((np.sin(seed * 0.01) * 0.5 + 0.5) * width)
            y = int((np.cos(seed * 0.013) * 0.5 + 0.5) * height)

            # Dust particle movement
            drift_x = int(x + np.sin(current_time * 0.1 + seed) * 50) % width
            drift_y = int(y + np.cos(current_time * 0.08 + seed) * 30) % height

            # Particle brightness
            brightness = int((np.sin(current_time + seed * 0.1) * 0.5 + 0.5) * 100 + 50)

            # Draw dust particle
            if 0 <= drift_x < width and 0 <= drift_y < height:
                # Cosmic dust colors (blues, purples, whites)
                if brightness > 120:
                    color = [brightness, brightness, 255]  # White-blue
                elif brightness > 80:
                    color = [brightness // 2, brightness // 2, brightness]  # Blue
                else:
                    color = [
                        brightness // 3,
                        brightness // 4,
                        brightness // 2,
                    ]  # Dark blue

                frame[drift_y, drift_x] = color

        return frame

    def _create_particle_field_background(
        self, frame, amplitude, current_time, frame_idx
    ):
        """Create particle field background."""
        height, width = frame.shape[:2]

        # Dark base
        frame[:] = [20, 20, 40]

        # Particle field
        num_particles = int(400 + amplitude * 300)

        for i in range(num_particles):
            seed = (frame_idx * 777 + i) % 10000
            np.random.seed(seed)

            # Particle position with flow
            base_x = (np.sin(seed * 0.01) * 0.5 + 0.5) * width
            base_y = (np.cos(seed * 0.011) * 0.5 + 0.5) * height

            # Flow effect
            flow_x = base_x + np.sin(current_time * 0.5 + seed * 0.1) * 100
            flow_y = base_y + np.cos(current_time * 0.3 + seed * 0.12) * 80

            x = int(flow_x) % width
            y = int(flow_y) % height

            # Particle properties
            size = int(amplitude * 3 + 1)
            brightness = int((np.sin(current_time * 2 + seed) * 0.5 + 0.5) * 200 + 55)

            # Particle color (energy field colors)
            if brightness > 150:
                color = [brightness // 3, brightness // 2, brightness]  # Blue-white
            else:
                color = [brightness // 4, brightness // 3, brightness // 2]  # Dim blue

            # Draw particle with size
            for dx in range(-size, size + 1):
                for dy in range(-size, size + 1):
                    px, py = x + dx, y + dy
                    if 0 <= px < width and 0 <= py < height:
                        dist = np.sqrt(dx * dx + dy * dy)
                        if dist <= size:
                            alpha = max(0, 1 - dist / (size + 1))
                            for c in range(3):
                                frame[py, px, c] = min(
                                    255, int(frame[py, px, c] + color[c] * alpha)
                                )

        return frame

    def _create_morphing_shapes_background(
        self, frame, amplitude, current_time, frame_idx
    ):
        """Create morphing geometric shapes background."""
        height, width = frame.shape[:2]

        # Gradient base
        for y in range(height):
            intensity = y / height
            r = int(30 * (1 - intensity) + 80 * intensity)
            g = int(20 * (1 - intensity) + 40 * intensity)
            b = int(60 * (1 - intensity) + 120 * intensity)
            frame[y, :] = [b, g, r]

        # Morphing shapes
        center_x, center_y = width // 2, height // 2

        # Shape morphing based on time and amplitude
        shape_time = current_time * 0.5
        morph_factor = np.sin(shape_time) * 0.5 + 0.5
        size_factor = amplitude * 50 + 100

        # Draw morphing polygon
        num_sides = int(3 + morph_factor * 5)  # 3 to 8 sides
        radius = size_factor * (1 + morph_factor * 0.5)

        # Create polygon points
        points = []
        for i in range(num_sides):
            angle = (i / num_sides) * 2 * np.pi + shape_time
            x = center_x + int(np.cos(angle) * radius)
            y = center_y + int(np.sin(angle) * radius)
            points.append((x, y))

        # Fill polygon (simple fill)
        if len(points) >= 3:
            # Simple polygon fill using scanline
            min_y = max(0, min(p[1] for p in points))
            max_y = min(height - 1, max(p[1] for p in points))

            shape_color = [
                int(100 + amplitude * 100),
                int(50 + amplitude * 50),
                int(150 + amplitude * 100),
            ]

            for y in range(min_y, max_y + 1):
                intersections = []
                for i in range(len(points)):
                    p1 = points[i]
                    p2 = points[(i + 1) % len(points)]

                    if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                        if p2[1] != p1[1]:
                            x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                            intersections.append(int(x))

                intersections.sort()
                for i in range(0, len(intersections), 2):
                    if i + 1 < len(intersections):
                        x1 = max(0, intersections[i])
                        x2 = min(width - 1, intersections[i + 1])
                        for x in range(x1, x2 + 1):
                            frame[y, x] = shape_color

        return frame
