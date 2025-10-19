"""
Draw.io backend for od-draw.

Uses the od_draw.drawio package (adapted from drawpyo) to generate
Draw.io compatible XML files.
"""

import os
import tempfile
import subprocess
from typing import List

from .base import Backend
from ...shapes.base import Shape, Rectangle, Circle, Triangle, Polygon, Line, Square
from ...drawio import File, Page, Object


class DrawIOBackend(Backend):
    """
    Backend for rendering diagrams to Draw.io format.

    Converts od-draw shapes to Draw.io XML using the internal drawio package.
    """

    def render(self, shapes: List[Shape], output_path: str, **kwargs) -> None:
        """
        Render shapes to a Draw.io file.

        Args:
            shapes: List of shapes to render
            output_path: Path where the .drawio file should be saved
            **kwargs: Additional rendering options
        """
        # Extract directory and filename from output_path
        file_dir = os.path.dirname(output_path) or "."
        file_name = os.path.basename(output_path)

        # Create Draw.io file and page
        file = File(file_name=file_name, file_path=file_dir)
        page = Page(file=file)

        # Add shapes to page
        for shape in shapes:
            self._add_shape_to_page(page, shape)

        # Write to disk
        file.write()

    def show(self, shapes: List[Shape], **kwargs) -> None:
        """
        Display shapes in the configured Draw.io viewer.

        Args:
            shapes: List of shapes to display
            **kwargs: Additional display options
        """
        from ...config import get_config

        config = get_config()
        viewer = config["drawio_viewer"]

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".drawio", delete=False) as f:
            temp_path = f.name

        # Render to temporary file
        self.render(shapes, temp_path, **kwargs)

        # Open in viewer
        subprocess.run([viewer, temp_path])

    def _normalize_polygon_points(
        self, points: list, x: float, y: float, width: float, height: float
    ) -> str:
        """
        Normalize polygon points to 0-1 coordinates relative to bounding box.

        Args:
            points: List of (x, y) tuples
            x, y: Top-left corner of bounding box
            width, height: Dimensions of bounding box

        Returns:
            polyCoords string like [[0,0],[0.5,1],[1,0]]
        """
        normalized = []
        for px, py in points:
            nx = (px - x) / width if width > 0 else 0
            ny = (py - y) / height if height > 0 else 0
            normalized.append([nx, ny])
        return str(normalized)

    def _add_shape_to_page(self, page: Page, shape: Shape) -> None:
        """
        Convert an od-draw shape to a Draw.io object and add to page.

        Args:
            page: Draw.io page to add object to
            shape: od-draw shape to convert
        """
        # Skip lines for now - they need edge handling
        if isinstance(shape, Line):
            return

        # Determine shape type and get position/size
        custom_style = {}

        if isinstance(shape, Circle):
            shape_type = "ellipse"
            x, y = shape.x, shape.y
            width, height = shape.width, shape.height
        elif isinstance(shape, Triangle):
            # Use custom polygon for triangle
            points = shape.get_points()
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            x, y = min(xs), min(ys)
            width = max(xs) - x
            height = max(ys) - y
            # Use mxgraph.basic.polygon with custom points
            shape_type = "mxgraph.basic.polygon"
            custom_style["polyCoords"] = self._normalize_polygon_points(points, x, y, width, height)
        elif isinstance(shape, (Rectangle, Square)):
            shape_type = "rectangle"
            x, y = shape.x, shape.y
            width, height = shape.width, shape.height
        elif isinstance(shape, Polygon):
            # Use mxgraph.basic.polygon for arbitrary polygons
            xs = [p[0] for p in shape.points]
            ys = [p[1] for p in shape.points]
            x, y = min(xs), min(ys)
            width = max(xs) - x
            height = max(ys) - y
            shape_type = "mxgraph.basic.polygon"
            custom_style["polyCoords"] = self._normalize_polygon_points(
                shape.points, x, y, width, height
            )
        else:
            shape_type = "rectangle"  # Default
            x, y = getattr(shape, "x", 0), getattr(shape, "y", 0)
            width = getattr(shape, "width", 100)
            height = getattr(shape, "height", 100)

        # Add rotation if present
        if hasattr(shape, "rotation") and shape.rotation != 0:
            custom_style["rotation"] = int(shape.rotation)

        # Add border style (dashed/dotted)
        if hasattr(shape, "border_style"):
            if isinstance(shape.border_style, tuple):
                style = shape.border_style[0]  # Use first style
            else:
                style = shape.border_style

            if style == "dashed":
                custom_style["dashed"] = 1
            elif style == "dotted":
                custom_style["dashPattern"] = "1 3"

        # Convert background color to hex
        fill_color = None
        if shape.background_color:
            fill_color = shape.background_color.to_hex(include_alpha=False)

        # Convert border color to hex (use first border color)
        stroke_color = None
        if shape.border_color and shape.border_color[0]:
            stroke_color = shape.border_color[0].to_hex(include_alpha=False)

        # Get border thickness (use first value)
        stroke_width = None
        if shape.border_thickness:
            stroke_width = int(shape.border_thickness[0])

        # Create Draw.io object with custom style attributes
        obj = Object(
            page=page,
            value="",
            shape=shape_type,
            position=(x, y),
            width=width,
            height=height,
            fillColor=fill_color,
            strokeColor=stroke_color,
            strokeWidth=stroke_width,
            **custom_style,
        )
