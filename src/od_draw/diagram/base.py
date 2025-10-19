"""
Base diagram class for od-draw.
"""

from typing import List, Optional
from ..shapes.base import Shape
from .backends.base import Backend
from .backends.svg import SVGBackend
from .backends.png import PNGBackend
from .backends.drawio import DrawIOBackend


class Diagram:
    def __init__(self, width: int = 800, height: int = 600, units: str = "px"):
        self.width = width
        self.height = height
        self.units = units
        self.shapes: List[Shape] = []
        self._backend: Optional[Backend] = None
        self._explicit_dimensions = False

    def set_dimensions(self, width: int, height: int):
        """Explicitly set diagram dimensions."""
        self.width = width
        self.height = height
        self._explicit_dimensions = True

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)

    def set_backend(self, backend: Backend):
        self._backend = backend

    def render(self, output_path: str, backend: Optional[str] = None, **kwargs):
        if backend == "svg" or output_path.endswith(".svg"):
            self._backend = SVGBackend()
        elif backend == "png" or output_path.endswith(".png"):
            self._backend = PNGBackend()
        elif backend == "drawio" or output_path.endswith(".drawio"):
            self._backend = DrawIOBackend()
        elif self._backend is None:
            self._backend = SVGBackend()

        render_kwargs = {
            "width": self.width,
            "height": self.height,
            "explicit_dimensions": self._explicit_dimensions,
            **kwargs,
        }

        self._backend.render(self.shapes, output_path, **render_kwargs)

    def show(self, backend: str = "svg", **kwargs):
        if backend == "svg":
            self._backend = SVGBackend()
        elif backend == "png":
            self._backend = PNGBackend()
        elif backend == "drawio":
            self._backend = DrawIOBackend()
        elif self._backend is None:
            self._backend = SVGBackend()

        show_kwargs = {"width": self.width, "height": self.height, **kwargs}

        self._backend.show(self.shapes, **show_kwargs)
