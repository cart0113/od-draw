"""
SVG backend for od-draw.
"""

import math
from typing import List, Optional
from .base import Backend
from ...shapes.base import Shape, Rectangle, Circle, Triangle, Polygon, Line, Square


class SVGBackend(Backend):
    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        width = kwargs.get("width", 800)
        height = kwargs.get("height", 600)
        show_rulers = kwargs.get("show_rulers", False)
        show_grid = kwargs.get("show_grid", False)
        margin = kwargs.get("margin", 0)
        margin_top = kwargs.get("margin_top", margin)
        margin_bottom = kwargs.get("margin_bottom", margin)
        margin_left = kwargs.get("margin_left", margin)
        margin_right = kwargs.get("margin_right", margin)

        # Calculate effective canvas size
        canvas_width = width + margin_left + margin_right
        canvas_height = height + margin_top + margin_bottom

        svg_content = (
            f'<svg width="{canvas_width}" height="{canvas_height}" '
            f'xmlns="http://www.w3.org/2000/svg">\n'
        )

        # Add definitions for arrow markers
        svg_content += self._create_marker_defs()

        # Add grid if requested
        if show_grid:
            svg_content += self._create_grid(canvas_width, canvas_height, margin_left, margin_top)

        # Create a group for the main content with margins
        svg_content += f'  <g transform="translate({margin_left}, {margin_top})">\n'

        # Render shapes
        for shape in shapes:
            svg_content += self._shape_to_svg(shape)

        svg_content += "  </g>\n"

        # Add rulers if requested
        if show_rulers:
            svg_content += self._create_rulers(width, height, margin_left, margin_top)

        svg_content += "</svg>"

        with open(output_path, "w") as f:
            f.write(svg_content)

    def show(self, shapes: List[Shape], **kwargs):
        import tempfile
        import subprocess
        from ...config import get_config

        config = get_config()
        viewer = config["svg_viewer"]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False) as f:
            self.render(shapes, f.name, **kwargs)
            subprocess.run([viewer, f.name])

    def _create_marker_defs(self) -> str:
        """Create SVG marker definitions for line end styles."""
        return """  <defs>
    <marker id="arrow-out" markerWidth="10" markerHeight="10" refX="9" refY="3"
            orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="context-stroke" />
    </marker>
    <marker id="arrow-in" markerWidth="10" markerHeight="10" refX="0" refY="3"
            orient="auto" markerUnits="strokeWidth">
      <path d="M9,0 L9,6 L0,3 z" fill="context-stroke" />
    </marker>
    <marker id="circle-marker" markerWidth="8" markerHeight="8" refX="4" refY="4"
            orient="auto" markerUnits="strokeWidth">
      <circle cx="4" cy="4" r="3" fill="context-stroke" />
    </marker>
    <marker id="square-marker" markerWidth="8" markerHeight="8" refX="4" refY="4"
            orient="auto" markerUnits="strokeWidth">
      <rect x="1" y="1" width="6" height="6" fill="context-stroke" />
    </marker>
  </defs>
"""

    def _create_grid(self, width: float, height: float, offset_x: float, offset_y: float) -> str:
        """Create a grid pattern."""
        grid_svg = '  <g id="grid" opacity="0.2">\n'
        grid_size = 20

        # Vertical lines
        for x in range(0, int(width) + 1, grid_size):
            grid_svg += f'    <line x1="{x + offset_x}" y1="{offset_y}" x2="{x + offset_x}" y2="{height + offset_y}" stroke="#cccccc" stroke-width="0.5"/>\n'

        # Horizontal lines
        for y in range(0, int(height) + 1, grid_size):
            grid_svg += f'    <line x1="{offset_x}" y1="{y + offset_y}" x2="{width + offset_x}" y2="{y + offset_y}" stroke="#cccccc" stroke-width="0.5"/>\n'

        grid_svg += '  </g>\n'
        return grid_svg

    def _create_rulers(self, width: float, height: float, offset_x: float, offset_y: float) -> str:
        """Create rulers along the edges."""
        ruler_svg = '  <g id="rulers">\n'

        # Top ruler
        ruler_svg += f'    <rect x="{offset_x}" y="0" width="{width}" height="{offset_y}" fill="#f0f0f0"/>\n'

        # Left ruler
        ruler_svg += f'    <rect x="0" y="{offset_y}" width="{offset_x}" height="{height}" fill="#f0f0f0"/>\n'

        # Add tick marks (every 50 pixels)
        for i in range(0, int(width) + 1, 50):
            ruler_svg += f'    <line x1="{i + offset_x}" y1="{offset_y - 5}" x2="{i + offset_x}" y2="{offset_y}" stroke="#000" stroke-width="1"/>\n'
            ruler_svg += f'    <text x="{i + offset_x}" y="{offset_y - 8}" font-size="10" text-anchor="middle">{i}</text>\n'

        for i in range(0, int(height) + 1, 50):
            ruler_svg += f'    <line x1="{offset_x - 5}" y1="{i + offset_y}" x2="{offset_x}" y2="{i + offset_y}" stroke="#000" stroke-width="1"/>\n'
            ruler_svg += f'    <text x="{offset_x - 8}" y="{i + offset_y + 4}" font-size="10" text-anchor="end">{i}</text>\n'

        ruler_svg += '  </g>\n'
        return ruler_svg

    def _shape_to_svg(self, shape) -> str:
        """Convert a shape to SVG."""
        if isinstance(shape, Line):
            return self._line_to_svg(shape)
        elif isinstance(shape, Circle):
            return self._circle_to_svg(shape)
        elif isinstance(shape, Triangle):
            return self._triangle_to_svg(shape)
        elif isinstance(shape, Polygon):
            return self._polygon_to_svg(shape)
        elif isinstance(shape, (Rectangle, Square)):
            return self._rectangle_to_svg(shape)
        return ""

    def _get_transform(self, shape: Shape) -> str:
        """Get transform attribute for rotation."""
        if shape.rotation != 0:
            cx = shape.x + shape.width / 2
            cy = shape.y + shape.height / 2
            return f' transform="rotate({shape.rotation} {cx} {cy})"'
        return ""

    def _color_to_svg(self, color) -> str:
        """Convert Color object to SVG color string."""
        if color is None:
            return "none"
        hex_color = color.to_hex(include_alpha=False)
        if color.alpha < 1.0:
            return f"{hex_color};opacity:{color.alpha}"
        return hex_color

    def _get_fill_opacity(self, color) -> str:
        """Get fill-opacity attribute if needed."""
        if color and color.alpha < 1.0:
            return f' fill-opacity="{color.alpha}"'
        return ""

    def _get_stroke_opacity(self, color) -> str:
        """Get stroke-opacity attribute if needed."""
        if color and color.alpha < 1.0:
            return f' stroke-opacity="{color.alpha}"'
        return ""

    def _rectangle_to_svg(self, rect: Shape) -> str:
        """Convert rectangle to SVG."""
        fill = self._color_to_svg(rect.background_color) if rect.background_color else "none"
        transform = self._get_transform(rect)
        fill_opacity = self._get_fill_opacity(rect.background_color) if rect.background_color else ""

        # For simplicity, use the first border values if they're all the same
        # Otherwise, we'd need to draw 4 separate lines for each side
        stroke = self._color_to_svg(rect.border_color[0])
        stroke_width = rect.border_thickness[0]
        stroke_opacity = self._get_stroke_opacity(rect.border_color[0])

        # Handle stroke style
        stroke_dasharray = ""
        if rect.border_style[0] == "dashed":
            stroke_dasharray = ' stroke-dasharray="5,5"'
        elif rect.border_style[0] == "dotted":
            stroke_dasharray = ' stroke-dasharray="1,3"'

        return (
            f'    <rect x="{rect.x}" y="{rect.y}" width="{rect.width}" height="{rect.height}" '
            f'fill="{fill}"{fill_opacity} stroke="{stroke}" stroke-width="{stroke_width}"'
            f'{stroke_opacity}{stroke_dasharray}{transform}/>\n'
        )

    def _circle_to_svg(self, circle: Circle) -> str:
        """Convert circle to SVG."""
        fill = self._color_to_svg(circle.background_color) if circle.background_color else "none"
        stroke = self._color_to_svg(circle.border_color[0])
        stroke_width = circle.border_thickness[0]
        cx = circle.x + circle.radius
        cy = circle.y + circle.radius
        fill_opacity = self._get_fill_opacity(circle.background_color) if circle.background_color else ""
        stroke_opacity = self._get_stroke_opacity(circle.border_color[0])

        return (
            f'    <circle cx="{cx}" cy="{cy}" r="{circle.radius}" '
            f'fill="{fill}"{fill_opacity} stroke="{stroke}" stroke-width="{stroke_width}"'
            f'{stroke_opacity}/>\n'
        )

    def _triangle_to_svg(self, triangle: Triangle) -> str:
        """Convert triangle to SVG."""
        points = triangle.get_points()
        points_str = " ".join(f"{x},{y}" for x, y in points)

        fill = self._color_to_svg(triangle.background_color) if triangle.background_color else "none"
        stroke = self._color_to_svg(triangle.border_color[0])
        stroke_width = triangle.border_thickness[0]
        transform = self._get_transform(triangle)
        fill_opacity = self._get_fill_opacity(triangle.background_color) if triangle.background_color else ""
        stroke_opacity = self._get_stroke_opacity(triangle.border_color[0])

        return (
            f'    <polygon points="{points_str}" '
            f'fill="{fill}"{fill_opacity} stroke="{stroke}" stroke-width="{stroke_width}"'
            f'{stroke_opacity}{transform}/>\n'
        )

    def _polygon_to_svg(self, polygon: Polygon) -> str:
        """Convert polygon to SVG."""
        points_str = " ".join(f"{x},{y}" for x, y in polygon.points)

        fill = self._color_to_svg(polygon.background_color) if polygon.background_color else "none"
        stroke = self._color_to_svg(polygon.border_color[0])
        stroke_width = polygon.border_thickness[0]
        transform = self._get_transform(polygon)
        fill_opacity = self._get_fill_opacity(polygon.background_color) if polygon.background_color else ""
        stroke_opacity = self._get_stroke_opacity(polygon.border_color[0])

        return (
            f'    <polygon points="{points_str}" '
            f'fill="{fill}"{fill_opacity} stroke="{stroke}" stroke-width="{stroke_width}"'
            f'{stroke_opacity}{transform}/>\n'
        )

    def _line_to_svg(self, line: Line) -> str:
        """Convert line to SVG."""
        stroke = self._color_to_svg(line.color)
        stroke_opacity = self._get_stroke_opacity(line.color)

        # Handle stroke style
        stroke_dasharray = ""
        if line.style == "dashed":
            stroke_dasharray = ' stroke-dasharray="5,5"'
        elif line.style == "dotted":
            stroke_dasharray = ' stroke-dasharray="1,3"'

        # Handle end markers
        marker_start = ""
        marker_end = ""

        if line.left_end_style == "arrow-out":
            marker_start = ' marker-start="url(#arrow-out)"'
        elif line.left_end_style == "arrow-in":
            marker_start = ' marker-start="url(#arrow-in)"'
        elif line.left_end_style == "circle":
            marker_start = ' marker-start="url(#circle-marker)"'
        elif line.left_end_style == "square":
            marker_start = ' marker-start="url(#square-marker)"'

        if line.right_end_style == "arrow-out":
            marker_end = ' marker-end="url(#arrow-out)"'
        elif line.right_end_style == "arrow-in":
            marker_end = ' marker-end="url(#arrow-in)"'
        elif line.right_end_style == "circle":
            marker_end = ' marker-end="url(#circle-marker)"'
        elif line.right_end_style == "square":
            marker_end = ' marker-end="url(#square-marker)"'

        return (
            f'    <line x1="{line.x0}" y1="{line.y0}" x2="{line.x1}" y2="{line.y1}" '
            f'stroke="{stroke}" stroke-width="{line.thickness}"'
            f'{stroke_opacity}{stroke_dasharray}{marker_start}{marker_end}/>\n'
        )
