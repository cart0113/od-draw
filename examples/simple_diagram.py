"""
Simple example diagram using od-draw.
"""

from od_draw.diagram.base import Diagram
from od_draw.shapes.base import Rectangle, Circle
from od_draw.cli import cli


class MyDiagram(Diagram):
    def __init__(self, text="hi", width=800, height=600, units="px"):
        super().__init__(width=int(width), height=int(height), units=units)

        Rectangle(
            diagram=self,
            x=100,
            y=100,
            width=200,
            height=100,
            background_color="#ff6b6b",
            border_color="#000000",
            border_thickness=2,
        )

        Circle(
            diagram=self,
            x=400,
            y=150,
            radius=50,
            background_color="#4ecdc4",
            border_color="#000000",
            border_thickness=2,
        )

        Rectangle(
            diagram=self,
            x=500,
            y=300,
            width=150,
            height=80,
            background_color="#ffe66d",
            border_color="#000000",
            border_thickness=2,
        )
