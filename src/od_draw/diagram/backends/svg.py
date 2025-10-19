"""
SVG backend for od-draw.
"""

import math
from typing import List, Optional
from .base import Backend
from ...shapes.base import Shape, Rectangle, Circle, Triangle, Polygon, Line, Square


class SVGBackend(Backend):
    def _calculate_bounding_box(self, shapes: List[Shape]) -> tuple:
        """Calculate the bounding box of all shapes, accounting for rotation."""
        if not shapes:
            return 0, 0, 800, 600

        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        for shape in shapes:
            if isinstance(shape, Line):
                min_x = min(min_x, shape.x0, shape.x1)
                min_y = min(min_y, shape.y0, shape.y1)
                max_x = max(max_x, shape.x0, shape.x1)
                max_y = max(max_y, shape.y0, shape.y1)
            elif isinstance(shape, Polygon):
                # Polygons with rotation need special handling
                if shape.rotation != 0:
                    # Calculate centroid for rotation
                    cx = sum(x for x, y in shape.points) / len(shape.points)
                    cy = sum(y for x, y in shape.points) / len(shape.points)
                    # Rotate each point
                    angle_rad = math.radians(shape.rotation)
                    for x, y in shape.points:
                        rx = cx + (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad)
                        ry = cy + (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad)
                        min_x = min(min_x, rx)
                        min_y = min(min_y, ry)
                        max_x = max(max_x, rx)
                        max_y = max(max_y, ry)
                else:
                    for x, y in shape.points:
                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)
            else:
                # Rectangle-like shapes with rotation
                if shape.rotation != 0:
                    # Calculate the four corners
                    cx = shape.x + shape.width / 2
                    cy = shape.y + shape.height / 2
                    angle_rad = math.radians(shape.rotation)

                    corners = [
                        (shape.x, shape.y),
                        (shape.x + shape.width, shape.y),
                        (shape.x + shape.width, shape.y + shape.height),
                        (shape.x, shape.y + shape.height),
                    ]

                    for x, y in corners:
                        rx = cx + (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad)
                        ry = cy + (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad)
                        min_x = min(min_x, rx)
                        min_y = min(min_y, ry)
                        max_x = max(max_x, rx)
                        max_y = max(max_y, ry)
                else:
                    min_x = min(min_x, shape.x)
                    min_y = min(min_y, shape.y)
                    max_x = max(max_x, shape.x + shape.width)
                    max_y = max(max_y, shape.y + shape.height)

        return min_x, min_y, max_x, max_y

    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        explicit_dimensions = kwargs.get("explicit_dimensions", False)

        show_rulers = kwargs.get("show_rulers", False)
        show_grid = kwargs.get("show_grid", False)
        margin = kwargs.get("margin", 0)
        margin_top = kwargs.get("margin_top", margin)
        margin_bottom = kwargs.get("margin_bottom", margin)
        margin_left = kwargs.get("margin_left", margin)
        margin_right = kwargs.get("margin_right", margin)

        # Add space for rulers if requested
        ruler_size = 30 if show_rulers else 0
        ruler_left = ruler_size
        ruler_top = ruler_size

        if explicit_dimensions:
            # Use explicitly set dimensions (already includes any desired margins)
            content_width = kwargs.get("width", 800)
            content_height = kwargs.get("height", 600)
            min_x = 0
            min_y = 0
            max_x = content_width
            max_y = content_height
        else:
            # Auto-calculate from bounding box
            min_x, min_y, max_x, max_y = self._calculate_bounding_box(shapes)
            # The content area is the shape bounds PLUS margins on all sides
            # Margins are PART OF the drawing
            content_width = (max_x - min_x) + margin_left + margin_right
            content_height = (max_y - min_y) + margin_top + margin_bottom

        # Calculate effective canvas size
        # Canvas needs to fit: ruler + content (which already includes margins)
        canvas_width = ruler_left + content_width
        canvas_height = ruler_top + content_height

        svg_content = (
            f'<svg width="{canvas_width}" height="{canvas_height}" '
            f'xmlns="http://www.w3.org/2000/svg">\n'
            f"  <style>\n"
            f'    text {{ font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif; }}\n'
            f"  </style>\n"
        )

        # Add definitions for arrow markers
        svg_content += self._create_marker_defs()

        # The drawing area starts right after the ruler
        # Ruler is at 0,0 and measures the full content (including margins)
        drawing_start_x = ruler_left
        drawing_start_y = ruler_top

        # Add grid if requested (covers the full drawing area)
        if show_grid:
            svg_content += self._create_grid(
                content_width, content_height, drawing_start_x, drawing_start_y
            )

        # Shapes are offset within the drawing area by the left/top margins
        # and normalized by subtracting min_x, min_y so the leftmost/topmost shape
        # starts at margin_left, margin_top
        shape_offset_x = drawing_start_x + margin_left - min_x
        shape_offset_y = drawing_start_y + margin_top - min_y
        svg_content += f'  <g transform="translate({shape_offset_x}, {shape_offset_y})">\n'

        # Render shapes
        for shape in shapes:
            svg_content += self._shape_to_svg(shape)

        svg_content += "  </g>\n"

        # Add rulers if requested (always at top-left origin)
        if show_rulers:
            svg_content += self._create_rulers(
                content_width, content_height, margin_left, margin_top, ruler_left, ruler_top
            )

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
        """Create a grid pattern with minor grid every 50px and major grid every 100px."""
        grid_svg = '  <g id="grid">\n'

        # Minor grid lines (every 50 pixels)
        grid_svg += '    <g opacity="0.3">\n'
        for x in range(0, int(width) + 1, 50):
            if x % 100 != 0:
                grid_svg += f'      <line x1="{x + offset_x}" y1="{offset_y}" x2="{x + offset_x}" y2="{height + offset_y}" stroke="#999999" stroke-width="0.5"/>\n'

        for y in range(0, int(height) + 1, 50):
            if y % 100 != 0:
                grid_svg += f'      <line x1="{offset_x}" y1="{y + offset_y}" x2="{width + offset_x}" y2="{y + offset_y}" stroke="#999999" stroke-width="0.5"/>\n'
        grid_svg += "    </g>\n"

        # Major grid lines (every 100 pixels)
        grid_svg += '    <g opacity="0.25">\n'
        for x in range(0, int(width) + 1, 100):
            grid_svg += f'      <line x1="{x + offset_x}" y1="{offset_y}" x2="{x + offset_x}" y2="{height + offset_y}" stroke="#666666" stroke-width="1"/>\n'

        for y in range(0, int(height) + 1, 100):
            grid_svg += f'      <line x1="{offset_x}" y1="{y + offset_y}" x2="{width + offset_x}" y2="{y + offset_y}" stroke="#666666" stroke-width="1"/>\n'
        grid_svg += "    </g>\n"

        grid_svg += "  </g>\n"
        return grid_svg

    def _create_rulers(
        self,
        content_width: float,
        content_height: float,
        margin_left: float,
        margin_top: float,
        ruler_left: float,
        ruler_top: float,
    ) -> str:
        """Create rulers along the edges, always starting at (0,0)."""
        ruler_svg = '  <g id="rulers">\n'

        # Drawing area starts right after the ruler
        drawing_start_x = ruler_left
        drawing_start_y = ruler_top

        # Top ruler background (spans the full width)
        ruler_svg += f'    <rect x="0" y="0" width="{ruler_left + content_width}" height="{ruler_top}" fill="#e0e0e0"/>\n'

        # Left ruler background (spans the full height)
        ruler_svg += f'    <rect x="0" y="{ruler_top}" width="{ruler_left}" height="{content_height}" fill="#e0e0e0"/>\n'

        # Add tick marks (every 50 pixels) measuring the full content width
        for i in range(0, int(content_width) + 1, 50):
            ruler_svg += f'    <line x1="{i + drawing_start_x}" y1="{ruler_top - 5}" x2="{i + drawing_start_x}" y2="{ruler_top}" stroke="#000" stroke-width="1"/>\n'
            # Skip text for the last tick mark
            if i < int(content_width):
                ruler_svg += f'    <text x="{i + drawing_start_x}" y="{ruler_top - 8}" font-size="10" text-anchor="middle">{i}</text>\n'

        # Add tick marks (every 50 pixels) measuring the full content height
        for i in range(0, int(content_height) + 1, 50):
            ruler_svg += f'    <line x1="{ruler_left - 5}" y1="{i + drawing_start_y}" x2="{ruler_left}" y2="{i + drawing_start_y}" stroke="#000" stroke-width="1"/>\n'
            # Skip text for the last tick mark
            if i < int(content_height):
                ruler_svg += f'    <text x="{ruler_left - 8}" y="{i + drawing_start_y + 4}" font-size="10" text-anchor="end">{i}</text>\n'

        # Add dimensions text in bottom right corner
        dim_x = drawing_start_x + content_width - 5
        dim_y = drawing_start_y + content_height - 5
        ruler_svg += f'    <text x="{dim_x}" y="{dim_y}" font-size="11" text-anchor="end" fill="#666">{int(content_width)}×{int(content_height)}</text>\n'

        ruler_svg += "  </g>\n"
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
        fill_opacity = (
            self._get_fill_opacity(rect.background_color) if rect.background_color else ""
        )

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
            f"{stroke_opacity}{stroke_dasharray}{transform}/>\n"
        )

    def _circle_to_svg(self, circle: Circle) -> str:
        """Convert circle to SVG."""
        fill = self._color_to_svg(circle.background_color) if circle.background_color else "none"
        stroke = self._color_to_svg(circle.border_color[0])
        stroke_width = circle.border_thickness[0]
        cx = circle.x + circle.radius
        cy = circle.y + circle.radius
        fill_opacity = (
            self._get_fill_opacity(circle.background_color) if circle.background_color else ""
        )
        stroke_opacity = self._get_stroke_opacity(circle.border_color[0])

        return (
            f'    <circle cx="{cx}" cy="{cy}" r="{circle.radius}" '
            f'fill="{fill}"{fill_opacity} stroke="{stroke}" stroke-width="{stroke_width}"'
            f"{stroke_opacity}/>\n"
        )

    def _triangle_to_svg(self, triangle: Triangle) -> str:
        """Convert triangle to SVG."""
        points = triangle.get_points()
        points_str = " ".join(f"{x},{y}" for x, y in points)

        fill = (
            self._color_to_svg(triangle.background_color) if triangle.background_color else "none"
        )
        stroke = self._color_to_svg(triangle.border_color[0])
        stroke_width = triangle.border_thickness[0]
        transform = self._get_transform(triangle)
        fill_opacity = (
            self._get_fill_opacity(triangle.background_color) if triangle.background_color else ""
        )
        stroke_opacity = self._get_stroke_opacity(triangle.border_color[0])

        return (
            f'    <polygon points="{points_str}" '
            f'fill="{fill}"{fill_opacity} stroke="{stroke}" stroke-width="{stroke_width}"'
            f"{stroke_opacity}{transform}/>\n"
        )

    def _polygon_to_svg(self, polygon: Polygon) -> str:
        """Convert polygon to SVG."""
        points_str = " ".join(f"{x},{y}" for x, y in polygon.points)

        fill = self._color_to_svg(polygon.background_color) if polygon.background_color else "none"
        stroke = self._color_to_svg(polygon.border_color[0])
        stroke_width = polygon.border_thickness[0]
        transform = self._get_transform(polygon)
        fill_opacity = (
            self._get_fill_opacity(polygon.background_color) if polygon.background_color else ""
        )
        stroke_opacity = self._get_stroke_opacity(polygon.border_color[0])

        return (
            f'    <polygon points="{points_str}" '
            f'fill="{fill}"{fill_opacity} stroke="{stroke}" stroke-width="{stroke_width}"'
            f"{stroke_opacity}{transform}/>\n"
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
            f"{stroke_opacity}{stroke_dasharray}{marker_start}{marker_end}/>\n"
        )
