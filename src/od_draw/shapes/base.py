"""
Base shape classes for od-draw.
"""

from typing import Optional


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Size:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height


class Shape:
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        fill: Optional[str] = None,
        stroke: Optional[str] = None,
        stroke_width: float = 1,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width

    @property
    def position(self):
        return Point(self.x, self.y)

    @property
    def size(self):
        return Size(self.width, self.height)


class Rectangle(Shape):
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
        fill: Optional[str] = None,
        stroke: Optional[str] = None,
        stroke_width: float = 1,
    ):
        super().__init__(x, y, width, height, fill, stroke, stroke_width)


class Circle(Shape):
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        radius: float = 50,
        fill: Optional[str] = None,
        stroke: Optional[str] = None,
        stroke_width: float = 1,
    ):
        super().__init__(x, y, radius * 2, radius * 2, fill, stroke, stroke_width)
        self.radius = radius


class Block(Rectangle):
    pass
