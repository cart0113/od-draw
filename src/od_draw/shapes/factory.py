"""
Factory functions for creating shapes.
"""

from typing import Optional
from .base import Block, Circle, Rectangle


def block(
    x0: float = 0,
    y0: float = 0,
    width: float = 100,
    height: float = 100,
    fill: Optional[str] = None,
    stroke: Optional[str] = None,
    stroke_width: float = 1,
):
    return Block(
        x=x0, y=y0, width=width, height=height, fill=fill, stroke=stroke, stroke_width=stroke_width
    )


def rectangle(
    x0: float = 0,
    y0: float = 0,
    width: float = 100,
    height: float = 100,
    fill: Optional[str] = None,
    stroke: Optional[str] = None,
    stroke_width: float = 1,
):
    return Rectangle(
        x=x0, y=y0, width=width, height=height, fill=fill, stroke=stroke, stroke_width=stroke_width
    )


def circle(
    x0: float = 0,
    y0: float = 0,
    radius: float = 50,
    fill: Optional[str] = None,
    stroke: Optional[str] = None,
    stroke_width: float = 1,
):
    return Circle(x=x0, y=y0, radius=radius, fill=fill, stroke=stroke, stroke_width=stroke_width)
