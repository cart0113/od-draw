"""
PNG backend for od-draw.
"""

import math
from typing import List, Tuple
from .base import Backend
from ...shapes.base import Shape, Rectangle, Circle, Triangle, Polygon, Line, Square


class PNGBackend(Backend):
    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        from PIL import Image, ImageDraw

        width = kwargs.get("width", 800)
        height = kwargs.get("height", 600)
        show_rulers = kwargs.get("show_rulers", False)
        show_grid = kwargs.get("show_grid", False)
        margin = kwargs.get("margin", 0)
        margin_top = kwargs.get("margin_top", margin)
        margin_bottom = kwargs.get("margin_bottom", margin)
        margin_left = kwargs.get("margin_left", margin)
        margin_right = kwargs.get("margin_right", margin)
        background = kwargs.get("background", "white")

        # Calculate effective canvas size
        canvas_width = width + margin_left + margin_right
        canvas_height = height + margin_top + margin_bottom

        img = Image.new("RGBA", (canvas_width, canvas_height), background)
        draw = ImageDraw.Draw(img)

        # Draw grid if requested
        if show_grid:
            self._draw_grid(draw, canvas_width, canvas_height, margin_left, margin_top)

        # Draw rulers if requested
        if show_rulers:
            self._draw_rulers(draw, width, height, margin_left, margin_top)

        # Draw shapes with margin offset
        for shape in shapes:
            self._draw_shape(draw, shape, margin_left, margin_top)

        img.save(output_path)

    def show(self, shapes: List[Shape], **kwargs):
        from PIL import Image, ImageDraw
        import tempfile
        import subprocess
        from ...config import get_config

        config = get_config()
        viewer = config["png_viewer"]

        width = kwargs.get("width", 800)
        height = kwargs.get("height", 600)
        background = kwargs.get("background", "white")

        img = Image.new("RGBA", (width, height), background)
        draw = ImageDraw.Draw(img)

        for shape in shapes:
            self._draw_shape(draw, shape, 0, 0)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".png", delete=False) as f:
            img.save(f.name)
            subprocess.run([viewer, f.name])

    def _draw_grid(self, draw, width: int, height: int, offset_x: int, offset_y: int):
        """Draw a grid pattern."""
        grid_size = 20
        color = (200, 200, 200, 100)  # Light gray with transparency

        # Vertical lines
        for x in range(0, int(width) + 1, grid_size):
            draw.line([(x + offset_x, offset_y), (x + offset_x, height + offset_y)], fill=color, width=1)

        # Horizontal lines
        for y in range(0, int(height) + 1, grid_size):
            draw.line([(offset_x, y + offset_y), (width + offset_x, y + offset_y)], fill=color, width=1)

    def _draw_rulers(self, draw, width: int, height: int, offset_x: int, offset_y: int):
        """Draw rulers along the edges."""
        from PIL import ImageFont

        ruler_color = (240, 240, 240)
        text_color = (0, 0, 0)

        # Top ruler background
        draw.rectangle([(offset_x, 0), (offset_x + width, offset_y)], fill=ruler_color)

        # Left ruler background
        draw.rectangle([(0, offset_y), (offset_x, offset_y + height)], fill=ruler_color)

        # Try to use a default font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            font = None

        # Add tick marks (every 50 pixels)
        for i in range(0, int(width) + 1, 50):
            draw.line([(i + offset_x, offset_y - 5), (i + offset_x, offset_y)], fill=text_color, width=1)
            draw.text((i + offset_x, offset_y - 18), str(i), fill=text_color, font=font)

        for i in range(0, int(height) + 1, 50):
            draw.line([(offset_x - 5, i + offset_y), (offset_x, i + offset_y)], fill=text_color, width=1)
            draw.text((offset_x - 30, i + offset_y - 5), str(i), fill=text_color, font=font)

    def _color_to_rgba(self, color) -> Tuple[int, int, int, int]:
        """Convert Color object to RGBA tuple."""
        if color is None:
            return (0, 0, 0, 0)
        r, g, b = color.rgb
        a = int(color.alpha * 255)
        return (r, g, b, a)

    def _draw_shape(self, draw, shape, offset_x: int = 0, offset_y: int = 0):
        """Draw a shape with offset."""
        if isinstance(shape, Line):
            self._draw_line(draw, shape, offset_x, offset_y)
        elif isinstance(shape, Circle):
            self._draw_circle(draw, shape, offset_x, offset_y)
        elif isinstance(shape, Triangle):
            self._draw_triangle(draw, shape, offset_x, offset_y)
        elif isinstance(shape, Polygon):
            self._draw_polygon(draw, shape, offset_x, offset_y)
        elif isinstance(shape, (Rectangle, Square)):
            self._draw_rectangle(draw, shape, offset_x, offset_y)

    def _draw_rectangle(self, draw, rect: Shape, offset_x: int, offset_y: int):
        """Draw a rectangle with optional rotation."""
        from PIL import Image, ImageDraw

        x1 = rect.x + offset_x
        y1 = rect.y + offset_y
        x2 = x1 + rect.width
        y2 = y1 + rect.height

        fill = self._color_to_rgba(rect.background_color) if rect.background_color else None
        outline = self._color_to_rgba(rect.border_color[0])
        width = int(rect.border_thickness[0])

        if rect.rotation != 0:
            # For rotated rectangles, we need to create a temporary image and rotate it
            temp_img = Image.new("RGBA", (int(rect.width + width * 2), int(rect.height + width * 2)), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            temp_draw.rectangle(
                [width, width, rect.width + width, rect.height + width],
                fill=fill,
                outline=outline,
                width=width
            )
            rotated = temp_img.rotate(-rect.rotation, expand=True)
            # Paste at the center position
            paste_x = int(x1 - (rotated.width - rect.width) / 2)
            paste_y = int(y1 - (rotated.height - rect.height) / 2)
            draw._image.paste(rotated, (paste_x, paste_y), rotated)
        else:
            draw.rectangle([x1, y1, x2, y2], fill=fill, outline=outline, width=width)

    def _draw_circle(self, draw, circle: Circle, offset_x: int, offset_y: int):
        """Draw a circle."""
        x1 = circle.x + offset_x
        y1 = circle.y + offset_y
        x2 = x1 + circle.radius * 2
        y2 = y1 + circle.radius * 2

        fill = self._color_to_rgba(circle.background_color) if circle.background_color else None
        outline = self._color_to_rgba(circle.border_color[0])
        width = int(circle.border_thickness[0])

        draw.ellipse([x1, y1, x2, y2], fill=fill, outline=outline, width=width)

    def _draw_triangle(self, draw, triangle: Triangle, offset_x: int, offset_y: int):
        """Draw a triangle."""
        points = triangle.get_points()
        points = [(x + offset_x, y + offset_y) for x, y in points]

        fill = self._color_to_rgba(triangle.background_color) if triangle.background_color else None
        outline = self._color_to_rgba(triangle.border_color[0])
        width = int(triangle.border_thickness[0])

        if triangle.rotation != 0:
            # Apply rotation to points
            cx = triangle.x + triangle.width / 2 + offset_x
            cy = triangle.y + triangle.height / 2 + offset_y
            angle_rad = math.radians(triangle.rotation)
            rotated_points = []
            for x, y in points:
                # Translate to origin
                tx = x - cx
                ty = y - cy
                # Rotate
                rx = tx * math.cos(angle_rad) - ty * math.sin(angle_rad)
                ry = tx * math.sin(angle_rad) + ty * math.cos(angle_rad)
                # Translate back
                rotated_points.append((rx + cx, ry + cy))
            points = rotated_points

        draw.polygon(points, fill=fill, outline=outline, width=width)

    def _draw_polygon(self, draw, polygon: Polygon, offset_x: int, offset_y: int):
        """Draw a polygon."""
        points = [(x + offset_x, y + offset_y) for x, y in polygon.points]

        fill = self._color_to_rgba(polygon.background_color) if polygon.background_color else None
        outline = self._color_to_rgba(polygon.border_color[0])
        width = int(polygon.border_thickness[0])

        if polygon.rotation != 0:
            # Apply rotation to points
            cx = polygon.x + polygon.width / 2 + offset_x
            cy = polygon.y + polygon.height / 2 + offset_y
            angle_rad = math.radians(polygon.rotation)
            rotated_points = []
            for x, y in points:
                tx = x - cx
                ty = y - cy
                rx = tx * math.cos(angle_rad) - ty * math.sin(angle_rad)
                ry = tx * math.sin(angle_rad) + ty * math.cos(angle_rad)
                rotated_points.append((rx + cx, ry + cy))
            points = rotated_points

        draw.polygon(points, fill=fill, outline=outline, width=width)

    def _draw_line(self, draw, line: Line, offset_x: int, offset_y: int):
        """Draw a line with optional end markers."""
        x0 = line.x0 + offset_x
        y0 = line.y0 + offset_y
        x1 = line.x1 + offset_x
        y1 = line.y1 + offset_y

        color = self._color_to_rgba(line.color)
        width = int(line.thickness)

        # Draw the main line
        draw.line([(x0, y0), (x1, y1)], fill=color, width=width)

        # Draw end markers
        if line.left_end_style != "none":
            self._draw_line_marker(draw, x0, y0, x1, y1, line.left_end_style, color, width, start=True)
        if line.right_end_style != "none":
            self._draw_line_marker(draw, x1, y1, x0, y0, line.right_end_style, color, width, start=False)

    def _draw_line_marker(self, draw, x: float, y: float, other_x: float, other_y: float,
                          style: str, color: Tuple[int, int, int, int], width: int, start: bool):
        """Draw a line end marker."""
        # Calculate angle
        dx = other_x - x
        dy = other_y - y
        angle = math.atan2(dy, dx)

        marker_size = width * 3

        if style == "arrow-out":
            # Arrow pointing away from line
            angle_offset = math.pi if start else 0
            tip_x = x + math.cos(angle + angle_offset) * marker_size
            tip_y = y + math.sin(angle + angle_offset) * marker_size
            left_x = x + math.cos(angle + angle_offset + 2.5) * marker_size * 0.5
            left_y = y + math.sin(angle + angle_offset + 2.5) * marker_size * 0.5
            right_x = x + math.cos(angle + angle_offset - 2.5) * marker_size * 0.5
            right_y = y + math.sin(angle + angle_offset - 2.5) * marker_size * 0.5
            draw.polygon([(tip_x, tip_y), (left_x, left_y), (right_x, right_y)], fill=color)

        elif style == "arrow-in":
            # Arrow pointing into line
            angle_offset = 0 if start else math.pi
            tip_x = x + math.cos(angle + angle_offset) * marker_size
            tip_y = y + math.sin(angle + angle_offset) * marker_size
            left_x = x + math.cos(angle + angle_offset + 2.5) * marker_size * 0.5
            left_y = y + math.sin(angle + angle_offset + 2.5) * marker_size * 0.5
            right_x = x + math.cos(angle + angle_offset - 2.5) * marker_size * 0.5
            right_y = y + math.sin(angle + angle_offset - 2.5) * marker_size * 0.5
            draw.polygon([(tip_x, tip_y), (left_x, left_y), (right_x, right_y)], fill=color)

        elif style == "circle":
            radius = marker_size / 2
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)

        elif style == "square":
            half_size = marker_size / 2
            draw.rectangle([x - half_size, y - half_size, x + half_size, y + half_size], fill=color)
