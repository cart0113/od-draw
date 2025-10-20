"""
Circle shape for od-draw.
"""

from typing import Optional
from .base import Shape
from ..colors import Color, ColorInput, parse_color


class Circle(Shape):
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
        super().__init__(diagram)
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
