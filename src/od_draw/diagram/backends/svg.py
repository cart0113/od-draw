"""
SVG backend for od-draw.
"""

from typing import List
from .base import Backend
from ...shapes.base import Shape, Rectangle, Circle


class SVGBackend(Backend):
    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        width = kwargs.get("width", 800)
        height = kwargs.get("height", 600)

        svg_content = (
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
        )

        for shape in shapes:
            svg_content += self._shape_to_svg(shape)

        svg_content += "</svg>"

        with open(output_path, "w") as f:
            f.write(svg_content)

    def show(self, shapes: List[Shape], **kwargs):
        import tempfile
        import subprocess
        from ...config import get_config

        config = get_config()
        viewer = config["svg_viewer"]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False) as f:
            self.render(shapes, f.name, **kwargs)
            subprocess.run([viewer, f.name])

    def _shape_to_svg(self, shape: Shape):
        if isinstance(shape, Circle):
            return self._circle_to_svg(shape)
        elif isinstance(shape, Rectangle):
            return self._rectangle_to_svg(shape)
        return ""

    def _rectangle_to_svg(self, rect: Rectangle):
        fill = rect.fill or "none"
        stroke = rect.stroke or "black"
        stroke_width = rect.stroke_width

        return f'  <rect x="{rect.x}" y="{rect.y}" width="{rect.width}" height="{rect.height}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'

    def _circle_to_svg(self, circle: Circle):
        fill = circle.fill or "none"
        stroke = circle.stroke or "black"
        stroke_width = circle.stroke_width
        cx = circle.x + circle.radius
        cy = circle.y + circle.radius

        return f'  <circle cx="{cx}" cy="{cy}" r="{circle.radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
