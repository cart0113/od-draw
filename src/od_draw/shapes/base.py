"""
Base shape classes for od-draw.
"""

from typing import Optional
from ..colors import Color, ColorInput, parse_color


class Line:
    """Line shape with start and end points."""

    def __init__(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        thickness: float = 1,
        color: Optional[ColorInput] = None,
        style: str = "solid",
        left_end_style: str = "none",
        right_end_style: str = "none",
        diagram=None,
    ):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.thickness = thickness
        self.color = parse_color(color) if color else Color("#000000")
        self.style = style
        self.left_end_style = left_end_style  # none, square, circle, arrow-in, arrow-out
        self.right_end_style = right_end_style

        # Auto-register with diagram if provided
        if diagram is not None:
            diagram.add_shape(self)


class Circle:
    """Circle shape."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        radius: float = 50,
        border_thickness: float = 1,
        border_style: str = "solid",
        border_color: Optional[ColorInput] = None,
        background_color: Optional[ColorInput] = None,
        diagram=None,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = radius * 2
        self.height = radius * 2
        self.rotation = 0  # Circles don't rotate visually

        self.border_thickness = border_thickness
        self.border_style = border_style
        self.border_color = parse_color(border_color) if border_color else Color("#000000")
        self.background_color = parse_color(background_color) if background_color else None

        # Auto-register with diagram if provided
        if diagram is not None:
            diagram.add_shape(self)
