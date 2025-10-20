"""
Base shape class for od-draw.
"""


class Shape:
    """Base class for all shapes."""

    def __init__(self, diagram=None):
        # Auto-register with diagram if provided
        if diagram is not None:
            diagram.add_shape(self)
