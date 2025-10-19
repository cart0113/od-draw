"""
Base shape classes for od-draw.
"""

from typing import Optional, Union, Tuple, List
from ..colors import Color, ColorInput, parse_color


# Type aliases for per-side properties
SideValue = Union[float, Tuple[float, float, float, float]]  # top, right, bottom, left
SideColor = Union[ColorInput, Tuple[ColorInput, ColorInput, ColorInput, ColorInput]]
SideStyle = Union[str, Tuple[str, str, str, str]]


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Size:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height


class Shape:
    """Base shape class with common properties."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        border_thickness: SideValue = 1,
        border_style: SideStyle = "solid",
        border_color: Optional[SideColor] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation

        # Handle per-side border thickness
        if isinstance(border_thickness, (int, float)):
            self.border_thickness = (border_thickness,) * 4
        else:
            self.border_thickness = border_thickness

        # Handle per-side border style
        if isinstance(border_style, str):
            self.border_style = (border_style,) * 4
        else:
            self.border_style = border_style

        # Handle per-side border color
        if border_color is None:
            self.border_color = (Color("#000000"),) * 4
        elif not isinstance(border_color, tuple) or len(border_color) != 4:
            color = parse_color(border_color) if border_color else Color("#000000")
            self.border_color = (color,) * 4
        else:
            self.border_color = tuple(parse_color(c) for c in border_color)

        # Handle background color
        if background_color is None:
            self.background_color = None
        else:
            self.background_color = parse_color(background_color)

    @property
    def position(self):
        return Point(self.x, self.y)

    @property
    def size(self):
        return Size(self.width, self.height)


class Rectangle(Shape):
    """Rectangle shape."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        border_thickness: SideValue = 1,
        border_style: SideStyle = "solid",
        border_color: Optional[SideColor] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
    ):
        super().__init__(
            x, y, width, height,
            border_thickness, border_style, border_color, background_color, rotation
        )


class Square(Shape):
    """Square shape (equal width and height)."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        size: float = 100,
        border_thickness: SideValue = 1,
        border_style: SideStyle = "solid",
        border_color: Optional[SideColor] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
    ):
        super().__init__(
            x, y, size, size,
            border_thickness, border_style, border_color, background_color, rotation
        )


class Triangle(Shape):
    """Triangle shape (defined by bounding box)."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        border_thickness: SideValue = 1,
        border_style: SideStyle = "solid",
        border_color: Optional[SideColor] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
    ):
        super().__init__(
            x, y, width, height,
            border_thickness, border_style, border_color, background_color, rotation
        )

    def get_points(self) -> List[Tuple[float, float]]:
        """Get triangle points (top center, bottom left, bottom right)."""
        return [
            (self.x + self.width / 2, self.y),  # top center
            (self.x, self.y + self.height),  # bottom left
            (self.x + self.width, self.y + self.height),  # bottom right
        ]


class Polygon(Shape):
    """Generic polygon shape defined by points."""

    def __init__(
        self,
        points: List[Tuple[float, float]],
        border_thickness: SideValue = 1,
        border_style: SideStyle = "solid",
        border_color: Optional[SideColor] = None,
        background_color: Optional[ColorInput] = None,
        rotation: float = 0,
    ):
        # Calculate bounding box
        if not points:
            raise ValueError("Polygon must have at least one point")

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        x = min(xs)
        y = min(ys)
        width = max(xs) - x
        height = max(ys) - y

        super().__init__(
            x, y, width, height,
            border_thickness, border_style, border_color, background_color, rotation
        )
        self.points = points


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


class Circle(Shape):
    """Circle shape."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        radius: float = 50,
        border_thickness: float = 1,
        border_color: Optional[ColorInput] = None,
        background_color: Optional[ColorInput] = None,
    ):
        # For circles, we don't support per-side borders
        super().__init__(
            x, y, radius * 2, radius * 2,
            border_thickness, "solid", border_color, background_color, 0
        )
        self.radius = radius


class Block(Rectangle):
    """Alias for Rectangle."""
    pass
