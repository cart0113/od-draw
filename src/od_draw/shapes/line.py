"""
Line shape for od-draw.
"""

from typing import Optional
from .base import Shape
from ..colors import Color, ColorInput, parse_color


class Line(Shape):
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
        super().__init__(diagram)
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.thickness = thickness
        self.color = parse_color(color) if color else Color("#000000")
        self.style = style
        self.left_end_style = left_end_style  # none, square, circle, arrow-in, arrow-out
        self.right_end_style = right_end_style
