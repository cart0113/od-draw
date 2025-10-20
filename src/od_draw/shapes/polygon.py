"""
Polygon shapes for od-draw.
"""

from typing import List, Tuple, Optional
from ..colors import Color, ColorInput, parse_color


class Polygon:
    """Base polygon shape defined by points."""

    def __init__(
        self,
        points: List[Tuple[float, float]],
        border_thickness: float = 1,
        border_style: str = "solid",
        border_color: Optional[ColorInput] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
        diagram=None,
    ):
        if not points:
            raise ValueError("Polygon must have at least 3 points")
        if len(points) < 3:
            raise ValueError("Polygon must have at least 3 points")

        self.points = points
        self.rotation = rotation

        # Calculate bounding box for compatibility
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        self.x = min(xs)
        self.y = min(ys)
        self.width = max(xs) - self.x
        self.height = max(ys) - self.y

        # Border properties (single value, not per-side)
        self.border_thickness = border_thickness
        self.border_style = border_style
        self.border_color = parse_color(border_color) if border_color else Color("#000000")

        # Background color
        self.background_color = parse_color(background_color) if background_color else None

        # Auto-register with diagram if provided
        if diagram is not None:
            diagram.add_shape(self)


class Triangle(Polygon):
    """Triangle shape defined by bounding box."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        border_thickness: float = 1,
        border_style: str = "solid",
        border_color: Optional[ColorInput] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
        diagram=None,
    ):
        # Calculate triangle points (top center, bottom left, bottom right)
        points = [
            (x + width / 2, y),  # top center
            (x, y + height),  # bottom left
            (x + width, y + height),  # bottom right
        ]

        super().__init__(
            points=points,
            border_thickness=border_thickness,
            border_style=border_style,
            border_color=border_color,
            background_color=background_color,
            rotation=rotation,
            diagram=diagram,
        )


class Rectangle(Polygon):
    """Rectangle shape defined by position and size."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        border_thickness: float = 1,
        border_style: str = "solid",
        border_color: Optional[ColorInput] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
        diagram=None,
    ):
        # Calculate rectangle points (top-left, top-right, bottom-right, bottom-left)
        points = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
        ]

        super().__init__(
            points=points,
            border_thickness=border_thickness,
            border_style=border_style,
            border_color=border_color,
            background_color=background_color,
            rotation=rotation,
            diagram=diagram,
        )


class Square(Polygon):
    """Square shape (equal width and height)."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        size: float = 100,
        border_thickness: float = 1,
        border_style: str = "solid",
        border_color: Optional[ColorInput] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
        diagram=None,
    ):
        # Calculate square points
        points = [
            (x, y),
            (x + size, y),
            (x + size, y + size),
            (x, y + size),
        ]

        super().__init__(
            points=points,
            border_thickness=border_thickness,
            border_style=border_style,
            border_color=border_color,
            background_color=background_color,
            rotation=rotation,
            diagram=diagram,
        )
