"""
Simple example diagram using od-draw.
"""

from od_draw import shapes, diagram, cli


class MyDiagram(diagram.Diagram):
    def __init__(self, text="hi", width=800, height=600, units="px"):
        super().__init__(width=int(width), height=int(height), units=units)

        rect = shapes.block(
            x0=100, y0=100, width=200, height=100, fill="#ff6b6b", stroke="#000000", stroke_width=2
        )
        self.add_shape(rect)

        circ = shapes.circle(
            x0=400, y0=150, radius=50, fill="#4ecdc4", stroke="#000000", stroke_width=2
        )
        self.add_shape(circ)

        rect2 = shapes.rectangle(
            x0=500, y0=300, width=150, height=80, fill="#ffe66d", stroke="#000000", stroke_width=2
        )
        self.add_shape(rect2)
