"""
od-draw: A Python library for creating diagrams with multiple backend support.
"""

__version__ = "0.1.0"

from .cli import cli
from .diagram.base import Diagram
from . import colors
from . import shapes

# Export commonly used items
from .shapes import (
    Rectangle,
    Square,
    Triangle,
    Polygon,
    Line,
    Circle,
)

__all__ = [
    "cli",
    "Diagram",
    "colors",
    "shapes",
    "Rectangle",
    "Square",
    "Triangle",
    "Polygon",
    "Line",
    "Circle",
]
