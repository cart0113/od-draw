"""
PNG backend for od-draw.

Generates PNG by first rendering to SVG, then converting to PNG using cairosvg.
"""

import tempfile
from typing import List
from .base import Backend
from ...shapes.base import Shape
from .svg import SVGBackend


class PNGBackend(Backend):
    """PNG backend that converts from SVG."""

    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        """
        Render shapes to PNG by converting from SVG.

        Args:
            shapes: List of shapes to render
            output_path: Path to write PNG file
            **kwargs: Additional rendering options passed to SVG backend
        """
        try:
            import cairosvg
        except ImportError:
            raise ImportError(
                "cairosvg is required for PNG rendering. "
                "Install it with: pip install cairosvg"
            )

        # Generate SVG first
        svg_backend = SVGBackend()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
            svg_path = f.name
            svg_backend.render(shapes, svg_path, **kwargs)

        # Convert SVG to PNG
        try:
            cairosvg.svg2png(url=svg_path, write_to=output_path)
        finally:
            # Clean up temporary SVG file
            import os
            os.unlink(svg_path)

    def show(self, shapes: List[Shape], **kwargs):
        """
        Display shapes in the configured PNG viewer.

        Args:
            shapes: List of shapes to display
            **kwargs: Additional rendering options
        """
        import tempfile
        import subprocess
        from ...config import get_config

        config = get_config()
        viewer = config["png_viewer"]

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.png', delete=False) as f:
            self.render(shapes, f.name, **kwargs)
            subprocess.run([viewer, f.name])
